"""ToolConfig file handler

Provides ``ToolConfigHandler`` class for locating and parsing
ToolConfig files relevant to a given filepath.

Licensed under Simplified BSD License (see LICENSE file).

"""

import os

from .exceptions import PathError


__all__ = ['ToolConfigHandler']


def get_filenames(path, filename):
    """Yield full filepath for filename in each directory in and above path"""
    path_list = []
    while True:
        path_list.append(os.path.join(path, filename))
        newpath = os.path.dirname(path)
        if path == newpath:
            break
        path = newpath
    return path_list


class ToolConfigHandler(object):

    """
    Allows locating and parsing of ToolConfig files for given filename

    In addition to the constructor a single public method is provided,
    ``get_configurations`` which returns the ToolConfig options for
    the ``filepath`` specified to the constructor.

    """

    def __init__(self, config_loader, filepath, conf_filename):
        """Create ToolConfigHandler for matching given filepath"""
        self.config_loader = config_loader
        self.filepath = filepath
        self.conf_filename = conf_filename
        self.options = None

    def get_configurations(self):

        """
        Find ToolConfig files and return all options matching filepath

        Special exceptions that may be raised by this function include:

        - ``PathError``: self.filepath is not a valid absolute filepath
        - ``ParsingError``: improperly formatted ToolConfig file found

        """

        self.check_assertions()
        path, filename = os.path.split(self.filepath)
        conf_files = get_filenames(path, self.conf_filename)

        # Attempt to find and parse every ToolConfig file in filetree
        for filename in conf_files:
            parser = self.config_loader(filename)
            options = parser.get_options_for(self.filepath)

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

        """Raise error if filepath has invalid values"""

        # Raise ``PathError`` if filepath isn't an absolute path
        if not os.path.isabs(self.filepath):
            raise PathError("Input file must be a full path name.")

    def preprocess_values(self):

        """Preprocess option values for consumption by plugins"""

        opts = self.options

        # Lowercase option value for certain options
        for name in ["end_of_line", "indent_style", "indent_size",
                     "insert_final_newline", "trim_trailing_whitespace",
                     "charset"]:
            if name in opts:
                opts[name] = opts[name].lower()

        # Set indent_size to "tab" if indent_size is unspecified and
        # indent_style is set to "tab".
        if (opts.get("indent_style") == "tab" and not "indent_size" in opts):
            opts["indent_size"] = "tab"

        # Set tab_width to indent_size if indent_size is specified and
        # tab_width is unspecified
        if ("indent_size" in opts and "tab_width" not in opts and
                opts["indent_size"] != "tab"):
            opts["tab_width"] = opts["indent_size"]

        # Set indent_size to tab_width if indent_size is "tab"
        if ("indent_size" in opts and "tab_width" in opts and
                opts["indent_size"] == "tab"):
            opts["indent_size"] = opts["tab_width"]
