#!/usr/bin/env python
"""
Fake uWSGI
=============
A Python module that attempts to fake out the uwsgi module exposed to uWSGI application. When testing applications outside uWSGI, for example Flask, this module can provide some functionality of the uwsgi module

See README.md for more information.
"""
import re

from setuptools import setup

with open("src/fake_uwsgi/__init__.py", encoding="utf8") as fp:
    version = re.search(r'__version__ = "(.*?)"', fp.read()).group(1)

extra_requires = {
    "dev": ["pre-commit"],
    "lint": ["black", "flake8", "pylint", "yamllint"],
    "test": ["coverage", "pytest", "pytest-cov", "pytest-xdist", "safety"],
}

setup(
    version=version,
    install_requires=[""],
    extras_require=extra_requires,
    zip_safe=False,
    platforms="any",
)
