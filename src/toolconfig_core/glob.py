# Part of toolconfig-core-py
# Copyright (c) 2011-2023 EditorConfig Team, including Hong Xu, Trey Hunner, and Christopher White
# SPDX-License-Identifier: PSF-2.0

"""
Glob-related routines.

Modified from editorconfig-core-py.
"""

import posixpath
from os import sep
from os.path import dirname, normpath

from toolconfig_core.ecpy.fnmatch import fnmatch


def matches_filename(config_path, glob, target_path):
    """Check if a target matches a glob in a config file.

    Args:
        config_path (str): absolute path to the config file
        glob (str): glob
        target_path (str): absolute path to the target file

    Returns:
        True if ``target_path`` matches ``glob``, anchored in the same
        directory as ``config_path``.

    """
    config_dirname = normpath(dirname(config_path)).replace(sep, "/")
    glob = glob.replace("\\#", "#")
    glob = glob.replace("\\;", ";")
    if "/" in glob:
        if glob.find("/") == 0:
            glob = glob[1:]
        glob = posixpath.join(config_dirname, glob)
    else:
        glob = posixpath.join("**/", glob)
    return fnmatch(target_path, glob)
