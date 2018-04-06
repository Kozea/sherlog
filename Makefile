include config.Makefile
-include config.custom.Makefile

BASEVERSION ?= v1
BASEROOT ?= https://raw.githubusercontent.com/Kozea/MakeCitron/$(BASEVERSION)/
BASENAME := base.Makefile
ifeq ($(MAKELEVEL), 0)
RV := $(shell wget -q -O $(BASENAME) $(BASEROOT)$(BASENAME) || echo 'FAIL')
ifeq (,$(RV))
include $(BASENAME)
else
$(error Unable to download $(BASEROOT)$(BASENAME))
endif
$(info $(INFO))
else
include $(BASENAME)
endif


all: install serve
	$(LOG)

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
	$(LOG)

deploy-prod:
	$(LOG)
	@echo "Communicating with Junkrat..."
	@wget --no-verbose --content-on-error -O- --header="Content-Type:application/json" --post-data=$(subst $(newline),,$(JUNKRAT_PARAMETERS)) $(JUNKRAT) | tee $(JUNKRAT_RESPONSE)
	if [[ $$(tail -n1 $(JUNKRAT_RESPONSE)) != "Success" ]]; then exit 9; fi
	wget --no-verbose --content-on-error -O- $(URL_PROD)
