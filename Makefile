# Makefile

.PHONY: egg install clean

all: egg

egg:
	python setup.py sdist

install:
	python setup.py install

clean:
	python setup.py clean
	rm -rf build dist *.egg-info

deploy:
	python setup.py register
	python setup.py sdist upload
