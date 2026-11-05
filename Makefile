# Makefile
#
# prerequisite
# uv (https://docs.astral.sh/uv/)
#

.PHONY: build install test clean deploy

all: build

build:
	uv build

install:
	uv tool install --force .

test:
	uv run pytest

clean:
	rm -rf build dist *.egg-info

deploy: clean build
	uvx twine upload --repository papery dist/*
