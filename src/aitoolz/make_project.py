"""Create a skeleton Python package project ready for development."""
import argparse
from importlib.resources import files
from pathlib import Path
from string import Template
from sys import argv


PROJECT_DIRS: tuple[str] = (
    "src",
    "src/${pkg_name}",
    "tests",
    ".github",
    ".github/workflows"
)

FILE_TEMPLATES_AND_TARGET_DIRS: dict[str, str] = {
    "README.md": ".",
    "pyproject.toml": ".",
    "noxfile.py": ".",
    "__init__.py": "src/${pkg_name}",
    "hello_world.py": "src/${pkg_name}",
    "test_hello_world.py": "tests",
    "python-package.yml": ".github/workflows",
    ".gitignore": "."
}


def _create_directory(
        path_template: str, template_values: dict[str, str], project_root: Path
    ) -> None:
    """Create directory.

    Args:
        path_template: Parent directory path templace.
        template_values: Values to use for rendering path_template.
        project_root: The ultimate parent directory.
    """
    parent_dir = project_root / Template(path_template).safe_substitute(template_values)
    parent_dir.mkdir()


def _create_from_template(
        template_filename: str,
        values: dict[str, str],
        parent_dir_template: str,
        project_root: Path,
    ) -> None:
    """Render template and save copy in parent directory.

    Args:
        template_filename: The template within `aitoolz.resources.templates`.
        values: The values to use for rendering the template.
        parent_dir_template: Directory in which to create the file, relative to
            project_root. Can contain templated variables for dynamic path creation.
        project_root: The project's ultimate root directory.

    Raises:
        FileNotFoundError: If template_filename or parent_dir can't be found.
    """
    template = files("aitoolz.resources.pkg_templates") / template_filename
    if not template.exists():
        raise FileNotFoundError(f"{template} does not exist")
    template_rendered = Template(template.read_text()).safe_substitute(values)

    parent_dir = Template(parent_dir_template).safe_substitute(values)
    new_file = project_root / parent_dir / template_filename
    if not new_file.parent.exists():
        raise FileNotFoundError(f"{new_file.parent} does not exist")
    new_file.write_text(template_rendered)


def create_python_pkg_project(pkg_name: str) -> None:
    """Create a skeleton Python package project ready for development.

    Args:
        pkg_name: The package's name.
    """
    project_root = Path(".") / pkg_name
    if project_root.exists():
        raise RuntimeError(f"{project_root} directory already exists.")
    project_root.mkdir()

    template_values = {"pkg_name": pkg_name}
    
    for dir in PROJECT_DIRS:
        _create_directory(dir, template_values, project_root)

    for template, target_dir in FILE_TEMPLATES_AND_TARGET_DIRS.items():
        _create_from_template(template, template_values, target_dir, project_root)


def cli() -> None:
    """Entrypoint for use on the CLI."""
    parser = argparse.ArgumentParser(description="Create a Python package project.")
    parser.add_argument("package_name", type=str)
    args = parser.parse_args()
    create_python_pkg_project(args.package_name)
