# Statick Planning Plugins

![Unit Tests](https://github.com/tdenewiler/statick-planning/workflows/Unit%20Tests/badge.svg)
[![PyPI version](https://badge.fury.io/py/statick-planning.svg)](https://badge.fury.io/py/statick-planning)
[![Codecov](https://codecov.io/gh/tdenewiler/statick-planning/branch/master/graphs/badge.svg)](https://codecov.io/gh/tdenewiler/statick-planning/)
![Python Versions](https://img.shields.io/pypi/pyversions/statick-planning.svg)
![License](https://img.shields.io/pypi/l/statick-planning.svg)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
![Daily Downloads](https://img.shields.io/pypi/dd/statick-planning.svg)
![Weekly Downloads](https://img.shields.io/pypi/dw/statick-planning.svg)
![Monthly Downloads](https://img.shields.io/pypi/dm/statick-planning.svg)

This is a set of plugins for [Statick](https://github.com/sscpac/statick) that will discover planning files and perform
static analysis on those files.

The current plugins will discover planning files in a project and can be configured to check those files using
[Validate](https://github.com/KCL-Planning/VAL).
Custom exceptions can be applied the same way they are with
[Statick exceptions](https://github.com/sscpac/statick#exceptions).

## Installation

The recommended method to install these Statick plugins is via pip:

    python3 -m pip install statick-planning

You can also clone the repository and use it locally.

The [Validate](https://github.com/KCL-Planning/VAL) tool has compilation instructions on their
[Github repository](https://github.com/KCL-Planning/VAL#how-to-compile-val).
The way this tool has been used and tested with Statick is by obtaining the binaries via zip file and putting the
binaries at `/opt/val/`.
The important part is to get the path to the `Validate` binary.
In our typical setup this binary is at `/opt/val/bin/Validate`.
If you have that binary in a different location you will have to update the commands in the rest of this documentation.
An example of where to obtain the zip file is
<https://dev.azure.com/schlumberger/4e6bcb11-cd68-40fe-98a2-e3777bfec0a6/_apis/build/builds/52/artifacts?artifactName=linux64&api-version=6.0&%24format=zip>.

## Usage

### Pip Install

The most common usage is to use statick and statick-planning from pip.
In that case your directory structure will look like the following:

- project
- output

To run with the default configuration for the statick-planning tools use:

```shell <!-- markdownlint-disable MD046 -->
statick project/ --output-directory output/ --profile planning-profile.yaml --validate-bin /opt/val/bin/Validate
```

### Pip Install and Custom Configuration

There are times when you will want to have a custom Statick configuration.
This is usually done to run a different set of tools than are called out in the default profile, or to add exceptions.
For this case you will have to add the new Statick configuration somewhere.
This example will have custom exceptions in the project, such that the directory structure is:

- project
  - statick-config
    - rsc
      - exceptions.yaml
- output

For this setup you will run the following:

```shell <!-- markdownlint-disable MD046 -->
statick project/ --output-directory output/ --user-paths project/statick-config/ --profile planning-profile.yaml --config planning-config.yaml --validate-bin /opt/val/bin/Validate <!-- markdownlint-disable MD013 -->
```

### Source Install and Custom Configuration

The last type of setup will be to have all of the tools available from cloning repositories, not installing from pip.
The directory structure will look like:

- /home/user
  - package
  - output
  - statick
  - statick-planning

Using the example where we want to override the default exceptions with custom ones in the project, the command
to run would be:

```shell <!-- markdownlint-disable MD046 -->
/home/user/statick/statick /home/user/package --output-directory output --user-paths /home/user/statick-planning/,/home/user/statick-planning/src/statick_planning/ --profile planning-profile.yaml --config planning-config.yaml --validate-bin /opt/val/bin/Validate <!-- markdownlint-disable MD013 -->
```

## Tests and Contributing

If you write a new feature for Statick or are fixing a bug, you are strongly encouraged to add unit tests for your contribution.
In particular, it is much easier to test whether a bug is fixed (and identify future regressions) if you can add a small
unit test which replicates the bug.

Before submitting a change, please run tox to check that you have not introduced any regressions or violated any code
style guidelines.

### Mypy

Statick uses [mypy](http://mypy-lang.org/) to check that type hints are being followed properly.
Type hints are described in [PEP 484](https://www.python.org/dev/peps/pep-0484/) and allow for static typing in Python.
To determine if proper types are being used in Statick plugins the following command will show any errors, and create several
types of reports that can be viewed with a text editor or web browser.

    python3 -m pip install mypy
    mkdir report
    mypy --ignore-missing-imports --strict src/

### Formatting

Statick code is formatted using [black](https://github.com/psf/black).
To fix locally use

    python3 -m pip install black
    black src
