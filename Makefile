# Makefile - convenience commands
# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause

.PHONY: init
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
	PYTHONPATH=src pytest tests

.PHONY: p prettyprint
p: prettyprint
prettyprint:
	isort src tests
	black src tests

.PHONY: run
run:
	PYTHONPATH=src python -m toolconfig_core
