![Logo of the project](./docs/logo.png)

# Trading212-API
> API for Trading212 broker service

[![Build Status](https://travis-ci.org/federico123579/trading-bot.svg?branch=master)](https://travis-ci.org/federico123579/trading-bot) [![Github All Releases](https://img.shields.io/github/downloads/federico123579/Trading212-API/total.svg)](https://github.com/federico123579/Trading212-API/releases) [![PyPI](https://img.shields.io/pypi/v/trading212api.svg)](https://pypi.python.org/pypi/trading212api) [![Coverage Status](https://coveralls.io/repos/github/federico123579/Trading212-API/badge.svg?branch=master)](https://coveralls.io/github/federico123579/Trading212-API?branch=master)

A python user-interface for Trading 212 using browser automation.

## Installing / Getting started

To install the API, just install it with pip.

```shell
pip install trading212api
python trading212api
```

## Developing

### Built With

- python _v.3.6_

#### Libraries

- splinter _v.0.7.6_

Built with *splinter* for a better browser automation.

### Prerequisites

The dependencies for dev instances are:
- splinter _v.0.7.6_
- geckodriver _(for Firefox)_
- chromedrive _(for Chrome)_

### Setting up Dev

Here's a brief intro about what a developer must do in order to start developing
the project further:

```shell
git clone https://github.com/federico123579/Trading212-API.git
cd Trading212-API/
python3.6 -m venv env
. env/bin//activate
pip install splinter bs4
```

### To-do

[ ] add real account login
[ ] fix test.py
[ ] fix addPrefs and clearPrefs
[ ] add closure time

## Versioning

The Semantic Versioning is used in this repository in this format:

    [major].[minor].[patch]-{status}

* **major** indicates incopatible changes
* **minor** indicates new features
* **patch** indicates bug fixies
* **status** show the status (alpha, beta, rc, etc.)

for more information see [Semantic Versioning](http://semver.org/)

## Configuration

As soon the program is launched it requires some user data:
- username
- password

## Api Reference

REQUIRED - **SOON**

## Licensing

This software is under the MIT license.
