"""ToolConfig exception classes

Licensed under Simplified BSD License (see LICENSE file).

"""


class ToolConfigError(Exception):
    """Parent class of all exceptions raised by ToolConfig"""


class ParsingError(ToolConfigError):
    """Error raised if a ToolConfig file could not be parsed"""


class PathError(ToolConfigError):
    """Error raised if invalid filepath is specified"""
