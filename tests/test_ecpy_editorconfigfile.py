# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause
"""Tests of toolconfig_core.ecpy.ini.EditorConfigFile"""

import pytest

from toolconfig_core.ecpy.ini import EditorConfigFile


def test_throws_nonexistent(tmp_path):
    with pytest.raises(OSError):
        EditorConfigFile(tmp_path / "nonexistent")
