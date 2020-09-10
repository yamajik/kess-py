#!/bin/bash

export GIT_MERGE_AUTOEDIT=no

CURRENT_VERSION=$1
UPGRADE_VERSION=$2

set -e

git flow release start ${UPGRADE_VERSION}
sed -i "" "s/${CURRENT_VERSION}/${UPGRADE_VERSION}/g" kess/__init__.py || sed -i "s/${CURRENT_VERSION}/${UPGRADE_VERSION}/g" kess/__init__.py
git commit -a -m "Ver: ${UPGRADE_VERSION}"
git flow release finish -m "${UPGRADE_VERSION}" ${UPGRADE_VERSION}
git push --all && git push --tags
