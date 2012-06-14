SHELL := /bin/bash

# these files should pass pyflakes
# exclude ./env/, which may contain virtualenv packages
PYFLAKES_WHITELIST=$(shell find . -name "*.py" ! -path "./docs/*" \
                    ! -path "./.tox/*" ! -path "./pylink/__init__.py" \
                    ! -path "./pylink/compat.py")

test:
	tox

pyflakes:
	pyflakes ${PYFLAKES_WHITELIST}

pep:
	pep8 --first pylink

clean:
	git clean -Xfd

dist:
	python setup.py sdist

upload:
	python setup.py sdist upload
