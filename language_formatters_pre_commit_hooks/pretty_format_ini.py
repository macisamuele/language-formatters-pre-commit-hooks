# -*- coding: utf-8 -*-
import argparse
import io
import sys
import typing

from configobj import ConfigObj
from configobj import ParseError

from language_formatters_pre_commit_hooks.utils import remove_trailing_whitespaces_and_set_new_line_ending


def pretty_format_ini(argv: typing.Optional[typing.List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--autofix",
        action="store_true",
        dest="autofix",
        help="Automatically fixes encountered not-pretty-formatted files",
    )
    parser.add_argument(
        "--indent",
        type=str,
        default="    ",
        dest="ini_indent",
        help="INI Indentation characters (by default 4 spaces)",
    )

    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(argv)

    status = 0

    for ini_file in set(args.filenames):
        with open(ini_file) as input_file:
            string_content_lines = input_file.read().splitlines()

        try:
            config_object = ConfigObj(
                infile=string_content_lines,
                indent_type=args.ini_indent,
                raise_errors=True,
            )

            output_lines = [line.rstrip() for line in config_object.write()]

            if string_content_lines != output_lines:
                print("File {} is not pretty-formatted".format(ini_file))

                if args.autofix:
                    print("Fixing file {}".format(ini_file))
                    with io.open(ini_file, "w", encoding="UTF-8") as output_file:
                        output_file.write(remove_trailing_whitespaces_and_set_new_line_ending("\n".join(output_lines)))

                status = 1
        except ParseError as e:
            print("Input File {} is not a valid INI file: {}".format(ini_file, e))
            return 1

    return status


if __name__ == "__main__":
    sys.exit(pretty_format_ini())
