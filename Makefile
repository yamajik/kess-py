REGISTRY ?= ""
IMAGE ?= yamajik/kess-python
VERSION ?= $(poetry version -s)

docker-build:
	docker build docker/kess-python \
		-t ${REGISTRY}/${IMAGE}:${VERSION} \
		-t ${REGISTRY}/${IMAGE}:latest

docker-push:
	docker push ${REGISTRY}/${IMAGE}:${VERSION}
	docker push ${REGISTRY}/${IMAGE}:latest

images: docker-build docker-push

dev:
	KESS_FUNCTIONS_FOLDER=examples/functions poetry run uvicorn examples.main:app --reload
