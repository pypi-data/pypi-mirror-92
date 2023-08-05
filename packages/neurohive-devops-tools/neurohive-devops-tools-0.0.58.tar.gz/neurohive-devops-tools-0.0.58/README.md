# Info

Set of various scripts which were used in '19-'20 to operate some integrations in CI pipelines.

It previously was distributed via PIP package, now it's a python-based Docker container.

# Installation

## Handy

Just use a docker container, e.g.:

```
docker build . -t devops-integration-tools
docker run --rm -ti devops-integration-tools
```

## Manual

Build a package:

```
pip install setuptools wheel
python ./setup.py  sdist bdist_wheel
```

Then upload to PyPI:

```
twine upload ./dist/*
```

Then install it somewhere:

```
pip install devops-integration-tools
```
