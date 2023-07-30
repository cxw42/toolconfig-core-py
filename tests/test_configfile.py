# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause
"""Tests of toolconfig_core.config_file.ConfigFile"""

import pytest

from toolconfig_core.config_file import ConfigFile


def test_no_config_files(tmp_path):
    ConfigFile(tmp_path)
    assert "ConfigFile did not throw in the absence of files"


def test_empty_tcfile(tmp_path):
    p = tmp_path / ".toolconfig.toml"
    p.touch()
    c = ConfigFile(tmp_path)
    assert "ConfigFile did not throw"
    assert not c.is_root


def test_empty_ecfile(tmp_path):
    p = tmp_path / ".editorconfig"
    p.touch()
    c = ConfigFile(tmp_path)
    assert "ConfigFile did not throw"
    assert not c.is_root


def test_nonempty_tcfile(tmp_path):
    p = tmp_path / ".toolconfig.toml"
    with open(p, "w") as f:
        print(
            """
root=true
['*']
answer = "tc"
""",
            file=f,
        )

    c = ConfigFile(tmp_path)
    assert "ConfigFile did not throw"

    # Check some internals
    assert c.tc
    assert not c.ec

    config = c.settings_for(tmp_path / "some_file")
    assert config == {"answer": "tc"}


# Make sure later matches win in a toolconfig file.
# Out of an abundance of paranoia, run this test several times.
@pytest.mark.parametrize("i", range(10))
def test_tcfile_section_order(i, tmp_path):
    p = tmp_path / ".toolconfig.toml"
    with open(p, "w") as f:
        print(
            """
root=true
['*']
key = "value1"
['*.txt']
key = "value2"
""",
            file=f,
        )

    c = ConfigFile(tmp_path)

    # The later value should win since both match.
    config = c.settings_for(tmp_path / "foo.txt")
    assert config == {"key": "value2"}


def test_nonempty_ecfile(tmp_path):
    p = tmp_path / ".editorconfig"
    with open(p, "w") as f:
        print(
            """
root=true
[*]
answer = ec
""",
            file=f,
        )

    c = ConfigFile(tmp_path)
    assert "ConfigFile did not throw"

    # Check some internals
    assert not c.tc
    assert c.ec

    config = c.settings_for(tmp_path / "some_file")
    assert config == {"answer": "ec"}
