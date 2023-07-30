"""ToolConfig file handler

Provides ``ToolConfigHandler`` class for locating and parsing
ToolConfig files relevant to a given filepath.

Licensed under Simplified BSD License (see LICENSE file).

"""

import os

from toolconfig_core.config_file import ConfigFile, dirs_for, find_root_dir
from toolconfig_core.exceptions import PathError


class ToolConfigHandler(object):

    """
    Allows locating and parsing of ToolConfig files for given filename

    In addition to the constructor a single public method is provided,
    ``get_options`` which returns the ToolConfig options for
    the ``abs_path`` specified to the constructor.

    """

    def __init__(self, abs_path):
        """Create ToolConfigHandler for matching given abs_path"""
        if not os.path.isabs(abs_path):
            raise PathError("Input file must be a full path name.")

        self.abs_path = abs_path
        self.root_dir = find_root_dir(abs_path)

    def get_options(self):
        """
        Find ToolConfig files and return all options matching abs_path

        Special exceptions that may be raised by this function include:

        - ``PathError``: self.abs_path is not a valid absolute filepath
        - ``ParsingError``: improperly formatted ToolConfig file found

        """

        result = {}

        # Attempt to find and parse every config file up to the root
        for d in dirs_for(self.abs_path):
            parser = ConfigFile(d)
            options = parser.settings_for(self.abs_path)
            result.update(options)

            # Stop parsing if parsed file has a ``root = true`` option
            if parser.is_root:
                break

        self.preprocess_values(result)

        return result

    def check_assertions(self):
        """Raise error if abs_path has invalid values"""

        # Raise ``PathError`` if abs_path isn't an absolute path

    @staticmethod
    def preprocess_values(opts):
        """Preprocess option values for consumption by plugins"""

        # Lowercase option value for certain options
        for name in [
            "end_of_line",
            "indent_style",
            "indent_size",
            "insert_final_newline",
            "trim_trailing_whitespace",
            "charset",
        ]:
            if name in opts:
                opts[name] = opts[name].lower()

        # Set indent_size to "tab" if indent_size is unspecified and
        # indent_style is set to "tab".
        if opts.get("indent_style") == "tab" and not "indent_size" in opts:
            opts["indent_size"] = "tab"

        # Set tab_width to indent_size if indent_size is specified and
        # tab_width is unspecified
        if (
            "indent_size" in opts
            and "tab_width" not in opts
            and opts["indent_size"] != "tab"
        ):
            opts["tab_width"] = opts["indent_size"]

        # Set indent_size to tab_width if indent_size is "tab"
        if (
            "indent_size" in opts
            and "tab_width" in opts
            and opts["indent_size"] == "tab"
        ):
            opts["indent_size"] = opts["tab_width"]
