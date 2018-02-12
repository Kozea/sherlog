include Makefile.config
-include Makefile.custom.config

all: install serve

install:
	test -d $(VENV) || virtualenv -p python3.6 $(VENV)
	$(PIP) install --upgrade --no-cache pip setuptools -e .[test]

install-dev:
	$(PIP) install --upgrade devcore

update-db:
	$(VENV)/bin/alembic upgrade head

install-db:
	$(FLASK) drop_db
	$(VENV)/bin/alembic upgrade head

clean:
	rm -fr dist

clean-install: clean
	rm -fr $(VENV)
	rm -fr *.egg-info

lint:
	$(PYTEST) --flake8 --isort -m "flake8 or isort" $(PROJECT_NAME)

check-python:
	FLASK_CONFIG=$(FLASK_CONFIG) $(PYTEST) $(PROJECT_NAME) $(PYTEST_ARGS)

check-outdated:
	$(PIP) list --outdated --format=columns

check: check-python check-outdated

build:

env:
	$(RUN)

run:
	env FLASK_DEBUG=1 $(VENV)/bin/flask run

serve: run
