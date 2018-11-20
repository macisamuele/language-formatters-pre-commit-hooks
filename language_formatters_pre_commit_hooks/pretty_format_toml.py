# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import sys

from toml import dumps
from toml import loads
from toml import TomlDecodeError

from language_formatters_pre_commit_hooks.utils import remove_trailing_whitespaces_and_set_new_line_ending


def pretty_format_toml(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--autofix',
        action='store_true',
        dest='autofix',
        help='Automatically fixes encountered not-pretty-formatted files',
    )

    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    status = 0

    for toml_file in set(args.filenames):
        with open(toml_file) as f:
            string_content = ''.join(f.readlines())

        try:
            prettified_content = remove_trailing_whitespaces_and_set_new_line_ending(
                dumps(loads(string_content)),
            )

            if string_content != prettified_content:
                print('File {} is not pretty-formatted'.format(toml_file))

                if args.autofix:
                    print('Fixing file {}'.format(toml_file))
                    with io.open(toml_file, 'w', encoding='UTF-8') as f:
                        f.write(prettified_content)

                status = 1
        except TomlDecodeError:
            print('Input File {} is not a valid TOML file'.format(toml_file))
            return 1

    return status


if __name__ == '__main__':
    sys.exit(pretty_format_toml())
