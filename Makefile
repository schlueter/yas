DOCKER_REPOSITORY := schlueter
CONTAINER_NAME := yas
VERSION := $(shell sed -En "s/.*version='([^']+)'.*/\1/p" setup.py)
CONTAINER_TAG := ${DOCKER_REPOSITORY}/${CONTAINER_NAME}:${VERSION}
CONTAINER_LATEST_TAG := ${DOCKER_REPOSITORY}/${CONTAINER_NAME}:latest


noop:
	@echo 'Doing nothing. Have a look at the Makefile if you want to find something to do.'

dist: dist/${PACKAGE}-${VERSION}.tar.gz
dist/${PACKAGE}-${VERSION}.tar.gz:
	python setup.py sdist bdist_wheel

test-pypi: update-on-test-pypi
update-on-test-pypi: dist
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi: update-on-pypi
update-on-pypi: dist
	python -m twine upload dist/*

git-tag:
	git tag -s ${VERSION}
	git push --tags

clean:
	rm -rf dist build *.egg-info
	find . -name __pycache__ -exec rm -rf {} +

distribute: | clean git-tag pypi

.PHONY: \
	clean \
	dist \
	distribute \
	git-tag \
	noop \
	pypi update-on-pypi \
	test-pypi update-on-test-pypi \
