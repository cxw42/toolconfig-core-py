# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause

"""Normalize a ToolConfig file.

This loads the given file, makes sure it's a valid ToolConfig TOML file,
normalizes properties, and outputs the normalized TOML."""

import argparse
import sys

import tomli
import tomli_w

from toolconfig_core import VERSION


def parse_args():
    """Parse the arguments.
    Return:
        argparse.Namespace: the parsed arguments
    """
    parser = argparse.ArgumentParser(description="Validate a ToolConfig file")
    parser.add_argument(
        "file",
        metavar="FILE",
        nargs="?",
        type=argparse.FileType("r"),
        default="-",
        help="The file to process (default stdin)",
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Do not output the processed file",
    )
    parser.add_argument(
        "--version", "-V", action="version", version=f"toolconfig-core-py {VERSION}"
    )
    return parser.parse_args()


def normalize(data):
    """Normalize the data.

    Not yet implemented."""
    return data


def main():
    """CLI"""
    args = parse_args()
    data = {}
    try:
        # Have to use loads(...read()) rather than load() because of
        # <https://github.com/python/cpython/issues/58364>
        data = tomli.loads(args.file.read())
    except Exception as e:
        raise Exception("Could not load input file") from e

    data = normalize(data)
    if not args.quiet:
        print(tomli_w.dumps(data), end="")


if __name__ == "__main__":
    main()
