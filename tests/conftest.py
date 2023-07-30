# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause
"""Pytest customization for toolconfig-core-py"""

import pytest


class TempTree(object):
    def __init__(self, path):
        self._root = path

    @property
    def root(self):
        return self._root

    def make(self, conf):
        """Create file(s)/dir(s) per ``conf``.

        Args:
            conf (dict): Tree of files/dirs to create.  Leaf nodes are
                file contents.
        """
        self._make(self.root, conf)

    def _make(self, root, conf):
        for k, v in conf.items():
            if type(v) != dict:
                # Create file
                (root / k).parent.mkdir(parents=True, exist_ok=True)
                (root / k).write_text(str(v))
            else:
                self._make(root / k, v)


@pytest.fixture
def tmp_tree(tmp_path):
    return TempTree(tmp_path)
