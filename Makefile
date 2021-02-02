IMAGE ?= yamajik/kess-python
VERSION ?= $(shell poetry version -s)

docker-build:
	docker build docker/kess-python \
		-t ${IMAGE}:${VERSION} \
		-t ${IMAGE}:latest

docker-push:
	docker push ${IMAGE}:${VERSION}
	docker push ${IMAGE}:latest

images: docker-build docker-push

dev:
	KESS_FUNCTIONS_FOLDER=examples/functions poetry run uvicorn examples.main:app --reload
