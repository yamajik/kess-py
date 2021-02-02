IMAGE ?= yamajik/kess-python
VERSION ?= $(shell poetry version -s)

pypi-build:
	poetry build

pypi-publish:
	poetry publish

pypi: pypi-build pypi-publish

images-build:
	docker build . -f docker/kess-python/Dockerfile \
		-t ${IMAGE}:${VERSION} \
		-t ${IMAGE}:latest

images-push:
	docker push ${IMAGE}:${VERSION}
	docker push ${IMAGE}:latest

images: images-build images-push

dev:
	KESS_FUNCTIONS_FOLDER=examples/functions poetry run uvicorn examples.main:app --reload
