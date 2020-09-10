#!/bin/bash

set -e

rm -rf build dist
python setup.py sdist bdist_wheel
twine upload dist/*
rm -rf build dist
