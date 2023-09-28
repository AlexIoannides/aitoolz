"""Developer task automation."""
import nox

PYTHON = ["3.10"]


@nox.session(python=PYTHON)
def run_tests(session):
    """Run unit tests."""
    session.install(".[dev]")
    session.run("pytest")


@nox.session(python=PYTHON, reuse_venv=True)
def format_code(session):
    """Lint code and re-format where necessary."""
    session.install(".[dev]")
    session.run("black", "--config=pyproject.toml", ".")
    session.run("ruff", "check", ".", "--config=pyproject.toml", "--fix")


@nox.session(python=PYTHON, reuse_venv=True)
def check_code_formatting(session):
    """Check code for formatting errors."""
    session.install(".[dev]")
    session.run("black", "--config=pyproject.toml", "--check", ".")
    session.run("ruff", "check", ".", "--config=pyproject.toml")


@nox.session(python=PYTHON, reuse_venv=True)
def check_types(session):
    """Run static type checking."""
    session.install(".[dev]")
    session.run("mypy", "src", "tests", "noxfile.py")
