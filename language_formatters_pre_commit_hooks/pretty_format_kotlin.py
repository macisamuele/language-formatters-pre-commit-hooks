# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys

from language_formatters_pre_commit_hooks.pre_conditions import java_required
from language_formatters_pre_commit_hooks.utils import download_url
from language_formatters_pre_commit_hooks.utils import get_modified_files_in_repo
from language_formatters_pre_commit_hooks.utils import run_command


KTLINT_VERSION = '0.25.1'


def download_kotlin_formatter_jar(version=KTLINT_VERSION):  # pragma: no cover
    def get_url(_version):
        # Links extracted from https://github.com/shyiko/ktlint/
        return \
            'https://github.com/shyiko/ktlint/releases/download/{version}/ktlint'.format(
                version=_version,
            )

    return download_url(get_url(version), 'ktlint{version}'.format(version=version))


@java_required
def pretty_format_kotlin(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--autofix',
        action='store_true',
        dest='autofix',
        help='Automatically fixes encountered not-pretty-formatted files',
    )

    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    ktlint_jar = download_kotlin_formatter_jar()

    modified_files_pre_kotlin_formatting = get_modified_files_in_repo()

    status, output = run_command(
        'java -jar {} --verbose {} {}'.format(
            ktlint_jar,
            '--format' if args.autofix else '--',
            ' '.join(args.filenames),
        ),
    )

    if output:
        print(output)
        return 1

    # Check all the file modified by the execution of the previous commands
    modified_files_post_kotlin_formatting = get_modified_files_in_repo()
    if modified_files_pre_kotlin_formatting != modified_files_post_kotlin_formatting:
        print(
            '{}: {}'.format(
                'The following files have been fixed by ktlint' if args.autofix else 'The following files are not properly formatted',  # noqa
                ', '.join(sorted(
                    modified_files_post_kotlin_formatting.difference(modified_files_pre_kotlin_formatting),
                )),
            ),
        )
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(pretty_format_kotlin())
