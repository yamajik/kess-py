#!/bin/bash

set -e

git checkout master
rm -rf build dist
python setup.py sdist bdist_wheel
twine upload dist/*
rm -rf build dist
git checkout develop
