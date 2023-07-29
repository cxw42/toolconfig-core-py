# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause

"""Read and process a ToolConfig file"""

import tomli

from toolconfig_core.exceptions import ParsingError


class ToolConfigFile(object):
    """Load a ToolConfig file.

    Args:
        tc_path (str): the absolute path of the toolconfig file

    """

    def __init__(self, tc_path):
        self.tc_path = tc_path

    @staticmethod
    def _get_config(tc_filename):
        """Load toolconfig file ``tc_filename``"""
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
        """Get the options applicable to a file.

        Args:
            target_path (str): Absolute path to the file of interest.

        Raises:
            OSError: if the toolconfig file for this instance cannot be opened
            toolconfig_core.exceptions.ParsingError: if there is a parsing problem

        """
        config = self._get_config(tc_path)
        return self._extract_options(config, target_path)
