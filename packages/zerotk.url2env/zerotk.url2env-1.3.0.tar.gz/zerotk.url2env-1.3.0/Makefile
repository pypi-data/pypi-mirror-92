.RECIPEPREFIX = >
.PHONY: all clean build upload

all: dist

clean:
> git clean -xdf

build:
> python setup.py build sdist

upload:
> twine upload -u $PYPI_USERNAME -p $PYPI_PASSWORD dist/*
