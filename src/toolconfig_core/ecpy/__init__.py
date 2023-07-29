"""EditorConfig Python Core"""

from toolconfig_core.ecpy.versiontools import join_version
from toolconfig_core.ecpy.version import VERSION

__all__ = ['get_properties', 'EditorConfigError', 'exceptions']

__version__ = join_version(VERSION)


def get_properties(filename):
    """Locate and parse EditorConfig files for the given filename"""
    handler = EditorConfigHandler(filename)
    return handler.get_configurations()


from toolconfig_core.ecpy.handler import EditorConfigHandler
from toolconfig_core.ecpy.exceptions import *
