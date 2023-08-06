# datasette-base64

[![PyPI](https://img.shields.io/pypi/v/datasette-base64.svg)](https://pypi.org/project/datasette-base64/)
[![Changelog](https://img.shields.io/github/v/release/alberto-salinas/datasette-base64?include_prereleases&label=changelog)](https://github.com/alberto-salinas/datasette-base64/releases)
[![Tests](https://github.com/alberto-salinas/datasette-base64/workflows/Test/badge.svg)](https://github.com/alberto-salinas/datasette-base64/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/alberto-salinas/datasette-base64/blob/main/LICENSE)

SQL functions to decode and encode base64 strings

## Installation

Install this plugin in the same environment as Datasette.

    $ datasette install datasette-base64

## Usage

    select base64decode(
        "QmxhZGUgUnVubmVy"
    )

    select base64encode(
        "Blade Runner"
    )

## Development

To set up this plugin locally, first checkout the code. Then create a new virtual environment:

    cd datasette-base64
    python3 -mvenv venv
    source venv/bin/activate

Or if you are using `pipenv`:

    pipenv shell

Now install the dependencies and tests:

    pip install -e '.[test]'

To run the tests:

    pytest
