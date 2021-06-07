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
	python setup.py install

clean:
	python setup.py clean
	rm -rf build dist

deploy: build
	twine upload --repository papery dist/*
