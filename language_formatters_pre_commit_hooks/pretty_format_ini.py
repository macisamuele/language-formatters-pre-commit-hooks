# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import sys
import typing

from six import PY3
from six import StringIO
from six import text_type
from six.moves.configparser import ConfigParser
from six.moves.configparser import Error

from language_formatters_pre_commit_hooks.utils import remove_trailing_whitespaces_and_set_new_line_ending


def pretty_format_ini(argv=None):
    # type: (typing.Optional[typing.List[typing.Text]]) -> int
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

        config_parser = ConfigParser()
        try:
            if PY3:  # pragma: no cover # py3+ only
                config_parser.read_string(string_content)
            else:  # pragma: no cover # py27 only
                config_parser.readfp(StringIO(str(string_content)))

            pretty_content = StringIO()
            config_parser.write(pretty_content)

            pretty_content_str = remove_trailing_whitespaces_and_set_new_line_ending(
                pretty_content.getvalue(),
            )

            if string_content != pretty_content_str:
                print("File {} is not pretty-formatted".format(ini_file))

                if args.autofix:
                    print("Fixing file {}".format(ini_file))
                    with io.open(ini_file, "w", encoding="UTF-8") as output_file:
                        output_file.write(text_type(pretty_content_str))

                status = 1
        except Error:
            print("Input File {} is not a valid INI file".format(ini_file))
            return 1

    return status


if __name__ == "__main__":
    sys.exit(pretty_format_ini())
