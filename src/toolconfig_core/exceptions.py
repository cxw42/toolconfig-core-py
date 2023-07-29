"""
exceptions.py - Exceptions we can raise
Part of toolconfig-core-py
Copyright (c) 2023 EditorConfig Team and Christopher White
SPDX-License-Identifier: BSD-2-Clause
"""

try:
    from ConfigParser import ParsingError as _ParsingError
except:
    from configparser import ParsingError as _ParsingError


class ToolConfigError(Exception):
    """Parent class of all exceptions raised by ToolConfig"""


class ParsingError(_ParsingError, ToolConfigError):
    """Error raised if a ToolConfig or EditorConfig file could not be parsed"""


class PathError(ValueError, ToolConfigError):
    """Error raised if invalid filepath is specified"""


class VersionError(ValueError, ToolConfigError):
    """Error raised if invalid version number is specified"""
