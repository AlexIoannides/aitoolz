"""Tests for the make_project.py module."""
import shutil
from collections.abc import Iterable
from pathlib import Path
from subprocess import CalledProcessError, run

from pytest import fixture, mark, raises

from aitoolz.make_project import create_python_pkg_project


@fixture(scope="module")
def test_project_name() -> str:
    return "my_new_project"


@fixture(scope="module")
def setup_and_teardown(test_project_name: str) -> Iterable[None]:
    try:
        create_python_pkg_project(test_project_name)
        yield None
    except Exception as e:
        raise e
    finally:
        shutil.rmtree(test_project_name, ignore_errors=True)


@mark.usefixtures("setup_and_teardown")
def test_create_python_pkg_project_creates_buildable_package_that_passes_tests(
    test_project_name: str,
):
    try:
        run(["nox", "-s", "run_tests"], check=True, cwd=test_project_name)
        assert True
    except CalledProcessError:
        assert False


@mark.usefixtures("setup_and_teardown")
def test_create_python_pkg_project_configured_static_code_checks_that_pass(
    test_project_name: str,
):
    try:
        run(["nox", "-s", "check_code_formatting"], check=True, cwd=test_project_name)
        assert True
    except CalledProcessError:
        assert False


@mark.usefixtures("setup_and_teardown")
def test_create_python_pkg_project_raises_exception_with_repeated_calls(
    test_project_name: str,
):
    with raises(RuntimeError, match="directory already exists"):
        create_python_pkg_project(test_project_name)


def test_cli_command():
    try:
        pkg_name = "foo"
        run(["mep", pkg_name], check=True)
        readme = Path(".") / pkg_name / "README.md"
        if readme.exists():
            assert True
        else:
            assert False
    except CalledProcessError:
        assert False
    finally:
        shutil.rmtree(pkg_name, ignore_errors=True)
