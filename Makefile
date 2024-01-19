# Makefile
#
# prerequisite
# `pip install -U build twine`
#

.PHONY: build install clean deploy

all: build

build:
	python -m build

install: build
	pip install .

clean:
	rm -rf dist papery.egg-info

deploy: build
	twine upload --repository papery dist/*
