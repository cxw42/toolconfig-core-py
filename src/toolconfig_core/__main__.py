# Part of toolconfig-core-py
# Copyright (c) 2023 Christopher White.
# SPDX-License-Identifier: BSD-2-Clause

"""toolconfig(1) CLI"""


import argparse

import tomli_w

from toolconfig_core import EC_CONFIG_NAME, VERSION
from toolconfig_core.config_file import ToolConfigFile, find_root_dir, get_filenames
from toolconfig_core.handler import ToolConfigHandler


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

    # Arguments intended for editorconfig-core-tests only
    parser.add_argument(
        "--ec-filename",
        "-f",
        metavar="FILENAME",
        nargs=1,
        help="Alternative name for .editorconfig files (TESTING ONLY).  Changes output format.",
    )

    return parser.parse_args()


def print_ec_output(output):
    """Print EditorConfig-format output for the sake of the core tests"""
    if len(output.keys()) != 1:
        raise RuntimeError("Sorry, but I don't support multiple inputs in EC test mode")
    for k, v in output[list(output.keys())[0]].items():
        print(f"{k}={v}")


def main():
    """CLI"""
    args = parse_args()
    ec_test_mode = "ec_filename" in args
    ec_filename = args.ec_filename[0] if ec_test_mode else EC_CONFIG_NAME

    options = {}
    for abs_path in args.abs_path:
        handler = ToolConfigHandler(abs_path, ec_filename)
        options[abs_path] = handler.get_options()

    # Produce output, always in sorted order of path name
    output = {k: options[k] for k in sorted(options.keys())}

    if ec_test_mode:
        print_ec_output(output)
    else:
        print(tomli_w.dumps(output))  # Normal output


if __name__ == "__main__":
    main()
