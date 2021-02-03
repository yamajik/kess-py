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
		-t ${IMAGE}:latest \
		--build-arg VERSION=${VERSION}

images-push:
	docker push ${IMAGE}:${VERSION}
	docker push ${IMAGE}:latest

images: images-build images-push

upgrade:
	VERSION=$(shell poetry version ${UPGRADE} -q && poetry version -s)
	git commit -a -m "ver: ${VERSION}"
	git tag ${VERSION}

release:
	git checkout master
	git merge develop
	git push --all && git push --tags
	git checkout develop

dev:
	KESS_FN_FOLDER=examples/fn poetry run uvicorn examples.main:app --reload
