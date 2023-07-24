# Makefile - convenience commands
# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-3-clause

.PHONY: init
init:
	pip3 install -r requirements.txt -r requirements_dev.txt

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
	git ls-files | grep -E '\.py$$' | xargs black
