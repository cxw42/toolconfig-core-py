# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause

"""toolconfig(1) CLI"""


import argparse

import tomli_w

from toolconfig_core import VERSION
from toolconfig_core.config_file import ToolConfigFile, find_root_dir, get_filenames
from toolconfig_core.tc.handler import ToolConfigHandler


def parse_args():
    """Parse the arguments.
    Return:
        argparse.Namespace: the parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Get tool settings to apply to a particular file in a project"
    )
    parser.add_argument(
        "abs_path",
        metavar="PATH",
        type=str,
        nargs="+",
        help="The absolute path to the file in the project",
    )
    parser.add_argument(
        "--version", "-V", action="version", version=f"toolconfig-core-py {VERSION}"
    )

    return parser.parse_args()


def get_options_for(abs_path, args):
    """Get the options for ``abs_path``."""


def main():
    """CLI"""
    args = parse_args()

    options = {}
    for abs_path in args.abs_path:
        handler = ToolConfigHandler(abs_path)
        options[abs_path] = handler.get_options()

    # Produce output, always in sorted order of path name
    output = {k: options[k] for k in sorted(options.keys())}

    print(tomli_w.dumps(output))


if __name__ == "__main__":
    main()
