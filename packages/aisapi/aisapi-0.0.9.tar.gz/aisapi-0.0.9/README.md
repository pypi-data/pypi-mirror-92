# AIS-api [![Build Status][travis_status]][travis] [![PyPI version][pypi_badge]][pypi]

_Python wrapper package for the AIS API._

## Install

```bash
pip install aisapi
```

Look at the file `example.py` for a usage example.

[travis_status]: https://travis-ci.org/sviete/AIS-api.svg?branch=master
[travis]: https://travis-ci.org/sviete/ais-api
[pypi]:https://pypi.org/project/aisapi/
[pypi_badge]: https://badge.fury.io/py/aisapi.svg


## Develop

```bash
git clone https://github.com/sviete/AIS-api.git

```


## Publish the new version to pip

```bash
rm -rf dist
python3 setup.py sdist bdist_wheel
twine upload dist/*
```
