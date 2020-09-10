#!/bin/bash

VERSION=`. tools/version.sh`

. docker/build.sh ${VERSION} $@
