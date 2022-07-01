# -*- coding: utf-8 -*-
import argparse
import io
import sys
import typing

from config_formatter import ConfigFormatter


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
        with open(ini_file, encoding="utf8") as input_file:
            string_content = input_file.read()

        try:
            formatter = ConfigFormatter()

            pretty_content_str = formatter.prettify(string_content)

            if string_content != pretty_content_str:
                print("File {} is not pretty-formatted".format(ini_file))

                if args.autofix:
                    print("Fixing file {}".format(ini_file))
                    with io.open(ini_file, "w", encoding="UTF-8") as output_file:
                        output_file.write(pretty_content_str)

                status = 1
        except BaseException as e:
            print("Input File {} is not a valid INI file: {}".format(ini_file, e))
            return 1

    return status


if __name__ == "__main__":
    sys.exit(pretty_format_ini())
