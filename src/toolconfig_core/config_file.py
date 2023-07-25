# config_file.py - read and process a ToolConfig file
# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause

import tomli


from .ecpy.exceptions import ParsingError


class ToolConfigFile(object):
    """Load a ToolConfig file"""

    def __init__(self, tc_path):
        """Constructor

        Args:
            tc_path (str): the absolute path of the toolconfig file
        """
        self.tc_path = tc_path

    @staticmethod
    def _get_config(tc_filename):
        """Load a toolconfig file"""
        with open(tc_filename, "rb") as f:
            try:
                config = tomli.load(f)
            except tomli.TomliDecodeError as e:
                raise ParsingError(f"Could not load {tc_filename}") from e

    @staticmethod
    def _extract_config(config, target_filename):
        """Extract the configuration for ``target_filename`` from ``config``"""
        # TODO RESUME HERE: ini.py:matches_filename()
        raise NotImplementedError()

    def get_options_for(target_path):
        """Get the options applicable to a file with absolute path
        ``target_path``
        """
        config = self._get_config(tc_path)
        return self._extract_options(config, target_path)
