IMAGE ?= yamajik/kess-python
VERSION ?= $(shell poetry version -s)
UPGRADE ?= minor

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

upgrade:
	poetry version ${UPGRADE}
	VERSION=$(shell poetry version -s)
	git commit -a -m "ver: ${VERSION}"
	git tag ${VERSION}

release:
	git checkout master
	git merge develop
	git checkout develop

dev:
	KESS_FUNCTIONS_FOLDER=examples/functions poetry run uvicorn examples.main:app --reload
