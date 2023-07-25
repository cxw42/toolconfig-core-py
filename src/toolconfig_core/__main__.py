# main.py - main CLI
# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause


import argparse

import tomli_w

from . import VERSION
from .config_file import ToolConfigFile
from .ecpy.handler import ToolConfigHandler


def parse_args():
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
        "--filename",
        "-f",
        type=str,
        nargs=1,
        metavar="FILENAME",
        default=".toolconfig.toml",
        help="Use FILENAME to find settings (default .toolconfig.toml)",
    )
    parser.add_argument(
        "--version", "-V", action="version", version=f"toolconfig-core-py {VERSION}"
    )

    return parser.parse_args()


def main():
    args = parse_args()

    configs = {}
    for abs_path in args.abs_path:
        handler = ToolConfigHandler(ToolConfigFile, abs_path, args.filename)
        configs[abs_path] = {"foo": 42}  # handler.get_configurations()

    # Produce output, always in sorted order of path name
    output = {k: configs[k] for k in sorted(configs.keys())}

    print(tomli_w.dumps(output))


if __name__ == "__main__":
    main()
