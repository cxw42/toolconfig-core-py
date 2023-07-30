# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause
"""Tests of toolconfig_core.handler"""

import pytest

from toolconfig_core import EC_CONFIG_NAME, TC_CONFIG_NAME
from toolconfig_core.exceptions import PathError
from toolconfig_core.handler import ToolConfigHandler


def test_nonabsolute_target():
    with pytest.raises(PathError):
        ToolConfigHandler("not-an-absolute-path")


def test_handler_tc(tmp_tree):
    tmp_tree.make(
        {
            EC_CONFIG_NAME: "root=true\n",
            TC_CONFIG_NAME: "root=true\n['*']\nkey='value_tc'\n",
            "dir": {"file1": "42\n"},
        }
    )
    c = ToolConfigHandler(tmp_tree.root / "dir" / "file1").get_options()
    assert c == {"key": "value_tc"}


def test_handler_ec(tmp_tree):
    tmp_tree.make(
        {
            EC_CONFIG_NAME: "root=true\n[*]\nkey=value_ec\n",
            "dir": {"file1": "42\n"},
        }
    )
    c = ToolConfigHandler(tmp_tree.root / "dir" / "file1").get_options()
    assert c == {"key": "value_ec"}


def test_handler_tc_hides_ec(tmp_tree):
    tmp_tree.make(
        {
            EC_CONFIG_NAME: "root=true\n['*']\nkey='value_ec'\n",
            TC_CONFIG_NAME: "root=true\n",
            "dir": {"file1": "42\n"},
        }
    )
    c = ToolConfigHandler(tmp_tree.root / "dir" / "file1").get_options()
    # Since there is a TC file, the EC file is not processed
    assert c == {}


def test_handler_tc_hides_ec_root(tmp_tree):
    tmp_tree.make(
        {
            TC_CONFIG_NAME: "root=true\n['*']\nkey='value_tc_top'\n",
            "dir": {TC_CONFIG_NAME: "", EC_CONFIG_NAME: "root=true\n", "file1": "42\n"},
        }
    )
    c = ToolConfigHandler(tmp_tree.root / "dir" / "file1").get_options()
    # Since there is a TC file in dir/, the EC file is not processed
    assert c == {"key": "value_tc_top"}


def test_handler_ec_root_taken_absent_tc(tmp_tree):
    tmp_tree.make(
        {
            TC_CONFIG_NAME: "root=true\n['*']\nkey2='value_tc_top'\n",
            "dir": {
                EC_CONFIG_NAME: "root=true\n[*]\nkey1=value_ec_dir\n",
                "file1": "42\n",
            },
        }
    )
    c = ToolConfigHandler(tmp_tree.root / "dir" / "file1").get_options()
    # Since there is a TC file in dir/, the EC file is not processed
    assert c == {"key1": "value_ec_dir"}


def test_handler_empty_tcfile(tmp_tree):
    tmp_tree.make(
        {
            TC_CONFIG_NAME: "root=true\n",  # isolate us from the environment
            "dir": {TC_CONFIG_NAME: ""},
        }
    )
    c = ToolConfigHandler(tmp_tree.root / "file1").get_options()
    assert c == {}


def test_handler_empty_ecfile(tmp_tree):
    tmp_tree.make(
        {
            EC_CONFIG_NAME: "root=true\n",  # isolate us from the environment
            "dir": {EC_CONFIG_NAME: ""},
        }
    )
    c = ToolConfigHandler(tmp_tree.root / "file1").get_options()
    assert c == {}


# Make sure later matches win in a toolconfig file.
# Out of an abundance of paranoia, run this test several times.
@pytest.mark.parametrize("i", range(10))
def test_tcfile_section_order(i, tmp_tree):
    tmp_tree.make(
        {
            TC_CONFIG_NAME: "root=true\n",
            "dir": {
                TC_CONFIG_NAME: """
['*']
key = "value1"
['*.txt']
key = "value2"
""",
            },
        }
    )

    c = ToolConfigHandler(tmp_tree.root / "dir" / "foo.txt").get_options()
    # The later value should win since both match.
    assert c == {"key": "value2"}
