#!/usr/bin/env python

"""
kess
"""


import itertools
import os
import re

from setuptools import find_packages, setup


def read(path):
    with open(path, "r") as f:
        return f.read()


VERSION_PARRTERN = r"__version__ = \"([\d\w\.]*)\""
VERSION_FILE = os.path.join("kess", "__init__.py")
VERSION = re.findall(VERSION_PARRTERN, read(VERSION_FILE))[0]

REQUIRES = [
    "fastapi==0.61.1",
    "uvicorn==0.11.8",
]
README = read("README.md")

packages = find_packages(exclude=["tests"])

setup(
    name="kess",
    version=VERSION,
    packages=packages,
    license="See License",
    author="majik",
    author_email="me@yamajik.com",
    description="Kess SDK",
    long_description=README,
    long_description_content_type="text/markdown",
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    install_requires=REQUIRES,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
