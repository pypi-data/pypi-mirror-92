from setuptools import setup
import os

VERSION = "0.1"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-base64",
    description="SQL functions to decode and encode base64 strings",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Jose Rodriguez Salinas",
    url="https://github.com/alberto-salinas/datasette-base64",
    project_urls={
        "Issues": "https://github.com/alberto-salinas/datasette-base64/issues",
        "CI": "https://github.com/alberto-salinas/datasette-base64/actions",
        "Changelog": "https://github.com/alberto-salinas/datasette-base64/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_base64"],
    entry_points={"datasette": ["base64 = datasette_base64"]},
    install_requires=["datasette"],
    extras_require={"test": ["pytest", "pytest-asyncio"]},
    tests_require=["datasette-base64[test]"],
    python_requires=">=3.6",
)
