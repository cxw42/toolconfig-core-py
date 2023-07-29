"""ToolConfig file handler

Provides ``ToolConfigHandler`` class for locating and parsing
ToolConfig files relevant to a given filepath.

Licensed under Simplified BSD License (see LICENSE file).

"""

import os

from toolconfig_core.config_file import ConfigFile
from toolconfig_core.exceptions import PathError

__all__ = ["ToolConfigHandler"]


class ToolConfigHandler(object):

    """
    Allows locating and parsing of ToolConfig files for given filename

    In addition to the constructor a single public method is provided,
    ``get_configurations`` which returns the ToolConfig options for
    the ``filepath`` specified to the constructor.

    """

    def __init__(self, abs_path):
        """Create ToolConfigHandler for matching given filepath"""
        self.abs_path = abs_path
        self.options = None
        self.root_dir = find_root_dir(abs_path)
        self.check_assertions()

    def get_configurations(self):
        """
        Find ToolConfig files and return all options matching abs_path

        Special exceptions that may be raised by this function include:

        - ``PathError``: self.abs_path is not a valid absolute filepath
        - ``ParsingError``: improperly formatted ToolConfig file found

        """

        path, filename = os.path.split(self.abs_path)
        conf_files = get_filenames(path, self.conf_filename)

        # Attempt to find and parse every ToolConfig file in filetree
        for d in dirs_for(self.abs_path):
            parser = ConfigFile(d)
            options = parser.get_options_for(self.abs_path)

            # Merge new ToolConfig file's options into current options
            old_options = self.options
            self.options = parser.options
            if old_options:
                self.options.update(old_options)

            # Stop parsing if parsed file has a ``root = true`` option
            if parser.root_file:
                break

        self.preprocess_values()
        return self.options

    def check_assertions(self):
        """Raise error if abs_path has invalid values"""

        # Raise ``PathError`` if abs_path isn't an absolute path
        if not os.path.isabs(self.abs_path):
            raise PathError("Input file must be a full path name.")

    def preprocess_values(self):
        """Preprocess option values for consumption by plugins"""

        opts = self.options

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
