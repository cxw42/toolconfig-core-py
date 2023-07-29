# Part of toolconfig-core-py
# Copyright (c) 2011-2023 EditorConfig Team, including Hong Xu, Trey Hunner, and Christopher White
# SPDX-License-Identifier: BSD-2-Clause

"""Finding and processing ToolConfig files"""

import os

import tomli

from toolconfig_core import EC_CONFIG_NAME, TC_CONFIG_NAME
from toolconfig_core.ecpy.ini import EditorConfigFile
from toolconfig_core.exceptions import ParsingError


class ToolConfigFile(object):
    """Load a ToolConfig file.

    Args:
        tc_path (str): the absolute path of the toolconfig file

    Raises:
        OSError: if the toolconfig file for this instance cannot be opened
        toolconfig_core.exceptions.ParsingError: if there is a parsing problem
    """

    def __init__(self, tc_path):
        self.config = None
        self.tc_path = tc_path
        with open(tc_path, "rb") as f:
            try:
                self.config = tomli.load(f)
            except tomli.TOMLDecodeError as e:
                raise ParsingError(f"Could not load {tc_path}") from e

    def settings_for(self, target_path):
        """Get the options applicable to a file.

        Args:
            target_path (str): Absolute path to the file of interest.
        """
        # TODO RESUME HERE: ini.py:matches_filename()
        raise NotImplementedError()

    @property
    def is_root(self):
        return bool(self.config and "root" in self.config and self.config["root"])


class ConfigFile(object):
    """Load the config file in a directory.

    Load the file called TC_CONFIG_NAME if it exists,
    otherwise the file called EC_CONFIG_NAME.

    Args:
        dir_name (str): The directory to look in
    """

    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.tc = None
        self.ec = None

        try:
            self.tc = ToolConfigFile(os.path.join(dir_name, TC_CONFIG_NAME))

            # If there's a TC file, we don't look for an EC file.
            return
        except OSError:
            pass

        try:
            self.ec = EditorConfigFile(os.path.join(dir_name, EC_CONFIG_NAME))
            return
        except OSError:
            pass

    @property
    def is_root(self):
        if self.tc:
            return self.tc.is_root
        elif self.ec:
            return self.ec.root_file
        else:
            return False

    def settings_for(self, target_filename):
        """Return the settings for target_path, which may or may not exist.

        Args:
            target_path (str): Absolute path
        """
        if self.tc:
            return self.tc.settings_for(target_filename)
        elif self.ec:
            return self.ec.settings_for(target_filename)
        else:
            return {}


def dirs_for(filename):
    """Yield each directory from the dir containing ``filename`` up to the root."""
    path = filename
    while True:
        newpath = os.path.dirname(path)
        yield newpath
        if path == newpath:
            break
        path = newpath


def find_root_dir(filename):
    """Find the project root directory for ``filename``."""
    last_dir = None
    for d in dirs_for(filename):
        last_dir = d
        config = ConfigFile(d)
        if d.is_root:
            return d

    return last_dir


def get_filenames(path, filename):
    """Return full filepaths for filename in each directory in and above path"""
    path_list = []
    while True:
        path_list.append(os.path.join(path, filename))
        newpath = os.path.dirname(path)
        if path == newpath:
            break
        path = newpath
    return path_list
