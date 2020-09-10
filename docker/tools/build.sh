#!/bin/bash

ARCH="$1"
TYPE="$2"
PYTHON_VERSION="$3"
IMAGE_VERSION="$4"

IMAGE_URL="yamajik/${TYPE}"
PYTHON_MAJOR_VERSION="$(echo ${PYTHON_VERSION} | cut -f 1 -d '.')"

docker build \
-t ${IMAGE_URL}:${PYTHON_VERSION}-${IMAGE_VERSION} \
-t ${IMAGE_URL}:${PYTHON_VERSION} \
-t ${IMAGE_URL}:${PYTHON_MAJOR_VERSION}-${IMAGE_VERSION} \
-t ${IMAGE_URL}:${PYTHON_MAJOR_VERSION} \
-t ${IMAGE_URL}:latest \
. \
-f ./docker/${ARCH}/${TYPE}/Dockerfile \
${@:5}

docker push ${IMAGE_URL}:${PYTHON_VERSION}-${IMAGE_VERSION}
docker push ${IMAGE_URL}:${PYTHON_VERSION}
docker push ${IMAGE_URL}:${PYTHON_MAJOR_VERSION}-${IMAGE_VERSION}
docker push ${IMAGE_URL}:${PYTHON_MAJOR_VERSION}
docker push ${IMAGE_URL}:latest
