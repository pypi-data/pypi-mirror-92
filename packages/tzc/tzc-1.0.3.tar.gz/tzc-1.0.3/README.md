# tzc - time zone convert

[![PyPI](https://img.shields.io/pypi/v/tzc.svg)](https://pypi.org/project/tzc/)
[![Changelog](https://img.shields.io/github/v/release/rstms/tzc?include_prereleases&label=changelog)](https://github.com/rstms/tzc/releases)
[![Tests](https://github.com/rstms/tzc/workflows/Test/badge.svg)](https://github.com/rstms/tzc/actions?query=workflow%3ATest)
[![License](https://img.shields.io/pypi/l/tzc)](https://github.com/rstms/tzc/blob/master/LICENSE)

copies input to output, converting timezone in any lines beginning with an ISO-8601 timestamp

## Installation

Install this tool using `pip`:

    $ pip install tzc

## Usage

Usage instructions go here.

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd tzc
    python -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
