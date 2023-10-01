# aitoolz

Various Python tools, by Alex Ioannides (AI). Some of them might be useful for artificial intelligence, some of them might not.

## Installing

aitoolz has yet to be released to PyPI. In the meantime, the best way to install it is directly from this repo, which you can do via

```text
pip install pip@git+https://github.com/alexioannides/aitoolz
```

## Features

A brief overview of the core tools:

### Template Python Package Projects

The `aitoolz.make_project` module exposes the `create_python_pkg_project` function that can create empty Python package projects to speed-up development. This includes:

- Executable tests via PyTest.
- Fully configured code formatting and checking using Ruff and Black.
- Fully configured static type checking using MyPy.
- Dev task automation using Nox.
- Fully configured CI using GitHub Actions.

This is an opinionated setup that reflects how I like to develop projects. This can also be called from the command line using the Make Empty Project (MEP) command - e.g.,

```text
mep my_package
```

Where `my_package` can be replaced with any valid Python module name. Either of these commands will create a directory structure and skeleton files,

```text
my_package
├── .github
│   └── workflows
│       └── python-package.yml
├── .gitignore
├── README.md
├── noxfile.py
├── pyproject.toml
├── src
│   └── my_package
│       ├── __init__.py
│       └── hello_world.py
└── tests
    └── test_hello_world.py
```

This has been tested to be installable and for all dev tasks automated with Nox to pass - use `nox --list` to see them all.
