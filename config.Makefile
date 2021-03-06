export PROJECT_NAME = sherlog

export FLASK_APP = $(PROJECT_NAME)
export FLASK_CONFIG ?= application.cfg
export FLASK_DEBUG ?= 1
export PYTEST_ARGS ?= --cov=sherlog --cov=sherlog/tests sherlog/tests --cov-report term-missing

# Python env
VENV = $(PWD)/.env
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python
PYTEST = $(VENV)/bin/py.test
FLASK = $(VENV)/bin/flask

URL_PROD = https://sherlog.kozea.fr/graph/Anne-Laure/ping6
