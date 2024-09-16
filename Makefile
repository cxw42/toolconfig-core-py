# Makefile - convenience commands
# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause

.PHONY: all
all: init test

.PHONY: install-deps init
install-deps: init
init:
	pip3 install -r requirements.txt -r requirements_dev.txt

.PHONY: venv
venv:
	mkdir -p .venv
	python3 -m venv .venv

.PHONY: build dist
dist: build
build:
	python3 -m build

.PHONY: check test
check: test
test:
	pytest

.PHONY: cover coverage
cover: coverage
coverage:
	pytest --cov=src --cov=tests \
		--cov-report html:cover/
	-xdg-open cover/index.html


.PHONY: p prettyprint
p: prettyprint
prettyprint:
	isort src tests
	black src tests

.PHONY: run
run:
	PYTHONPATH=src python -m toolconfig_core

.PHONY: editable
editable:
	-pip uninstall toolconfig_core
	pip install --editable .

.PHONY: lint
lint:
	pylint src tests

.PHONY: doc html
doc: html
html:
	$(MAKE) -C doc apidoc
	$(MAKE) -C doc html
	-xdg-open doc/build/html/index.html
