"""Developer task automation."""
import os

import nox
from dotenv import load_dotenv

PYTHON = ["3.10"]


@nox.session(python=PYTHON)
def run_tests(session: nox.Session):
    """Run unit tests."""
    session.install(".[dev]")
    pytest_args = session.posargs if session.posargs else []
    session.run("pytest", "-s", *pytest_args)


@nox.session(python=PYTHON, reuse_venv=True)
def format_code(session: nox.Session):
    """Lint code and re-format where necessary."""
    session.install(".[dev]")
    session.run("black", "--config=pyproject.toml", ".")
    session.run("ruff", "check", ".", "--config=pyproject.toml", "--fix")


@nox.session(python=PYTHON, reuse_venv=True)
def check_code_formatting(session: nox.Session):
    """Check code for formatting errors."""
    session.install(".[dev]")
    session.run("black", "--config=pyproject.toml", "--check", ".")
    session.run("ruff", "check", ".", "--config=pyproject.toml")


@nox.session(python=PYTHON, reuse_venv=True)
def check_types(session: nox.Session):
    """Run static type checking."""
    session.install(".[dev]")
    session.run("mypy", "src", "tests", "noxfile.py")


@nox.session(python=PYTHON, reuse_venv=True)
def build_and_deploy(session: nox.Session):
    """Build wheel and deploy to PyPI."""
    load_dotenv()
    try:
        PYPI_USR = os.environ["PYPI_USR"]
        PYPI_PWD = os.environ["PYPI_PWD"]
    except KeyError as e:
        print(f"ERROR: cannot build wheel and deploy to PyPI - {str(e)}")
    session.install(".[deploy]")
    session.run("rm", "-rf", "dist")
    session.run("python", "-m", "build")
    session.run("twine", "upload", "dist/*", "-u", PYPI_USR, "-p", PYPI_PWD)
