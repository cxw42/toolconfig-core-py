# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause
"""Tests of toolconfig_core.ecpy.ini.EditorConfigFile"""

import pytest

from toolconfig_core.ecpy.ini import EditorConfigFile


def test_nonexistent_ecfile(tmp_path):
    with pytest.raises(OSError):
        EditorConfigFile(tmp_path / "nonexistent")


def test_empty_ecfile(tmp_path):
    p = tmp_path / "file"
    p.touch()
    EditorConfigFile(p)
    assert "EditorConfigFile did not throw"


def test_nonempty_ecfile(tmp_path):
    p = tmp_path / ".editorconfig"
    with open(p, "w") as f:
        print(
            """
root=true
[*]
answer = 42
""",
            file=f,
        )

    ec = EditorConfigFile(p)
    assert "EditorConfigFile did not throw"

    config = ec.settings_for(tmp_path / "some_file")
    assert config == {"answer": "42"}
