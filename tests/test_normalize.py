# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause
"""Tests of toolconfig-normalize"""

import os.path

import pytest
from cli_test_helpers import shell

HERE = os.path.normpath(os.path.dirname(__file__))


def test_version():
    result = shell("toolconfig-normalize --version")
    assert result.exit_code == 0
    assert result.stdout


def test_basic(tmp_path):
    from_filename = os.path.join(HERE, "basic.in.toml")
    result = shell(f"toolconfig-normalize {from_filename}")
    assert result.exit_code == 0
    assert result.stdout

    expected_filename = os.path.join(HERE, "basic.expected.toml")
    with open(expected_filename, "r") as f:
        expected = f.read()

    assert result.stdout == expected


def test_quiet(tmp_path):
    from_filename = os.path.join(HERE, "basic.in.toml")
    result = shell(f"toolconfig-normalize -q {from_filename}")
    assert result.exit_code == 0
    assert result.stdout == ""


def test_invalid(tmp_path):
    filename = os.path.join(HERE, "test_sanity.py")
    result = shell(f"toolconfig-normalize -q {filename}")
    assert result.exit_code != 0
    assert result.stderr != ""


def test_nonexistent(tmp_path):
    result = shell(f"toolconfig-normalize {tmp_path / 'NONEXISTENT'}")
    assert result.exit_code != 0
    assert result.stderr != ""
