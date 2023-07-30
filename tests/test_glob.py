# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause
"""Test globbing"""

import pytest

from toolconfig_core.glob import matches_filename


@pytest.mark.parametrize(
    "config_path,glob,target_path",
    (
        ("/.editorconfig", "*", "/foo"),
        ("/.editorconfig", "*.txt", "/.txt"),
        ("/.editorconfig", "*.txt", "/foo.txt"),
        ("/.toolconfig.toml", "*.txt", "/foo.txt"),
        ("/foo/bar/.toolconfig.toml", "*.txt", "/foo/bar/bat.txt"),
        ("/foo/bar/.toolconfig.toml", "*.txt", "/foo/bar/bat/baz.txt"),
    ),
)
def test_matches(config_path, glob, target_path):
    assert matches_filename(config_path, glob, target_path)
