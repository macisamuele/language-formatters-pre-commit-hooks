# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import sys
from sys import maxsize

from ruamel.yaml import YAML
from ruamel.yaml.error import YAMLError
from six import StringIO
from six import text_type


def pretty_format_yaml(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--autofix',
        action='store_true',
        dest='autofix',
        help='Automatically fixes encountered not-pretty-formatted files',
    )
    parser.add_argument(
        '--indent',
        type=int,
        default='2',
        help=(
            'The number of indent spaces or a string to be used as delimiter'
            ' for indentation level e.g. 4 or "\t" (Default: 2)'
        ),
    )

    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    status = 0

    yaml = YAML()
    yaml.indent = args.indent
    # Prevent ruamel.yaml to wrap yaml lines
    yaml.width = maxsize

    for yaml_file in args.filenames:
        with open(yaml_file) as f:
            string_content = ''.join(f.readlines())

        try:
            pretty_content = StringIO()
            yaml.dump(yaml.load(string_content), pretty_content)

            if string_content != pretty_content.getvalue():
                print('File {} is not pretty-formatted'.format(yaml_file))

                if args.autofix:
                    print('Fixing file {}'.format(yaml_file))
                    with io.open(yaml_file, 'w', encoding='UTF-8') as f:
                        f.write(text_type(pretty_content.getvalue()))

                status = 1
        except YAMLError:
            print(
                'Input File {} is not a valid YAML file, consider using check-yaml'.format(
                    yaml_file,
                ),
            )
            return 1

    return status


if __name__ == '__main__':
    sys.exit(pretty_format_yaml())
