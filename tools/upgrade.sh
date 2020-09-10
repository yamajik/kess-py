#!/bin/bash

CURRENT_VERSION=`. tools/version.sh`
UPGRADE_VERSION=`. tools/version.sh upgrade $@`

. tools/publish.sh ${CURRENT_VERSION} ${UPGRADE_VERSION}
. tools/release.sh
. tools/jenkins.sh
