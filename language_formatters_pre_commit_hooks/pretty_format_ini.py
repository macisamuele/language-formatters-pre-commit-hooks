# -*- coding: utf-8 -*-
import argparse
import io
import sys
import typing
from configparser import ConfigParser
from configparser import Error

from iniparse import INIConfig

from language_formatters_pre_commit_hooks.utils import remove_trailing_whitespaces_and_set_new_line_ending


def pretty_format_ini(argv: typing.Optional[typing.List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--autofix",
        action="store_true",
        dest="autofix",
        help="Automatically fixes encountered not-pretty-formatted files",
    )

    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(argv)

    status = 0

    for ini_file in set(args.filenames):
        with open(ini_file) as input_file:
            string_content = "".join(input_file.readlines())

        try:
            # INIConfig only supports strict mode for throwing errors
            config_parser = ConfigParser()
            config_parser.read_string(string_content)

            ini_config = INIConfig(io.StringIO(str(string_content)), parse_exc=False)

            pretty_content_str = remove_trailing_whitespaces_and_set_new_line_ending(
                str(ini_config),
            )

            if string_content != pretty_content_str:
                print("File {} is not pretty-formatted".format(ini_file))

                if args.autofix:
                    print("Fixing file {}".format(ini_file))
                    with io.open(ini_file, "w", encoding="UTF-8") as output_file:
                        output_file.write(str(pretty_content_str))

                status = 1
        except Error:
            print("Input File {} is not a valid INI file".format(ini_file))
            return 1

    return status


if __name__ == "__main__":
    sys.exit(pretty_format_ini())
