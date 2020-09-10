#!/bin/bash

for i in {kess-python,kess-python-runtime}; do
    . docker/tools/build.sh amd64 $i 3.8 $@
done
