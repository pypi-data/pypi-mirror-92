import io
import os
import sys
from shutil import rmtree

from setuptools import find_packages, setup, Command

import nacos

#  just run `python setup.py upload`
here = os.path.abspath(os.path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="hypers_nacos",
    version=nacos.__version__,
    packages=find_packages(exclude=["test", "*.tests", "*.tests.*", "tests.*", "tests"]),
    url="https://github.com/nacos-group/nacos-sdk-python",
    license="Apache License 2.0",
    author="nacos",
    author_email="755063194@qq.com",
    description="Python client for Nacos.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],
)
