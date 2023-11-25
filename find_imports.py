"""Find all explicit 3rd party package imports within a Python file or module."""
import re
import sys
from importlib import metadata
from pathlib import Path

IMPORT_PKG_REGEX = r"^import\s(\w+)[\s\.]*.*$"
FROM_PKG_REGEX = r"^from\s(\w+)[\s\.].*import"


def _extract_imports_from_py_file(file: Path) -> set[str]:
    """Return all valid import from a text file."""
    code_lines = [line.strip() for line in file.read_text().split("\n")]
    import_pkg_imports = [
        re.findall(IMPORT_PKG_REGEX, line)
        for line in code_lines
        if line.startswith("import")
    ]
    from_pkg_imports = [
        re.findall(FROM_PKG_REGEX, line)
        for line in code_lines
        if line.startswith("from")
    ]
    distinct_imports = {
        pkg
        for imports in from_pkg_imports + import_pkg_imports
        for pkg in imports
        if isinstance(imports, list)
    }
    return distinct_imports


def _is_std_lib_pkg(pkg_name: str) -> bool:
    """Is the named package in the Python standard library."""
    def _fallback_test(pkg_name: str) -> bool:
        try:
            metadata.metadata(pkg_name)
            return False
        except metadata.PackageNotFoundError:
            return True

    try:
        pkg = __import__(pkg_name)
    except ModuleNotFoundError:
        return False
    if hasattr(pkg, "__file__"):
        if pkg.__file__ is None:
            return _fallback_test(pkg_name)
        if re.search(f"site-packages/{pkg_name}", pkg.__file__):
            return False
        elif re.search(r"lib/python3.\d+/", pkg.__file__):
            return True
        else:
            return False
    else:
        return _fallback_test(pkg_name)


def find_imports(module_path: str) -> list[str]:
    """Find all explicit imports for a Python module."""
    module = Path(module_path)
    if not module.exists():
        raise FileNotFoundError(f"can't find {module_path}")
    if module.is_dir():
        py_files = list(Path(module_path).glob("**/*.py"))
    else:
        py_files = [module]
    distinct_imports = {
        imports
        for py_file in py_files
        for imports in _extract_imports_from_py_file(py_file)
        if not _is_std_lib_pkg(imports) and imports != module.name
    }
    return list(distinct_imports)


def find_imports_and_installed_versions(module_path: str) -> list[str]:
    """Find all explicit imports and installed version for a Python module."""
    imports = find_imports(module_path)
    dependencies: set[str] = set()
    for pkg in imports:
        try:
            dependency = f"{pkg}=={metadata.version(pkg)}"
        except metadata.PackageNotFoundError:
            dependency = pkg
        dependencies.add(dependency)
    return list(dependencies)


if __name__ == "__main__":
    module_path = sys.argv[1]
    if len(sys.argv) > 2 and sys.argv[1] == "--versions":
        module_path = sys.argv[2]
        for dependency in find_imports_and_installed_versions(module_path):
            print(dependency)
    else:
        module_path = sys.argv[1]
        for dependency in find_imports(module_path):
            print(dependency)
