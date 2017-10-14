Trading API
> API for Trading212 broker service

[![Code Climate](https://img.shields.io/codeclimate/github/federico123579/Trading212-API.svg)](https://codeclimate.com/github/federico123579/Trading212-API) [![PyPI](https://img.shields.io/pypi/v/trading212api.svg)](https://pypi.python.org/pypi/trading212api)

A python based API for Trading 212 using selenium browser automation.

## Installing / Getting started

To install the API, just install it with pip.

```shell
pip install trading212api
```

## Developing
see [contribute](docs/CONTRIBUTE.md) to participate.

### Built With

- python _v.3.6_

#### Libraries

- splinter _v.0.7.6_

Built with *splinter* for a better browser automation.

### Prerequisites

The dependencies for dev instances are:
- Python3.6
- geckodriver _(for Firefox)_
- chromedrive _(for Chrome)_

### Setting up Dev

Here's a brief intro about what a developer must do in order to start developing
the project further:

```shell
git clone https://github.com/federico123579/Trading212-API.git
cd Trading212-API/
python3.6 -m venv env
. env/bin/activate
pip install -r dev-requirements.txt
pip install .
```

#### Docker

Or use a Dockerfile:

```shell
docker build -t tradingapi .
docker run --name tradingapi_instance -it tradingapi
```

### To-do

- [X] add exceptions and optimize logger
- [ ] add real account login
- [ ] fix test.py

## Versioning

The Semantic Versioning is used in this repository in this format:

    [major].[minor].[patch]-{status}

* **major** indicates incopatible changes
* **minor** indicates new features
* **patch** indicates bug fixies
* **status** show the status (alpha, beta, rc, etc.)

for more information see [Semantic Versioning](http://semver.org/)

## Api Reference

REQUIRED - **SOON**

## Licensing

This software is under the MIT license.
