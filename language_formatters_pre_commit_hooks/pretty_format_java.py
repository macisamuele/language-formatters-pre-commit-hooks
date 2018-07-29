# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys

from language_formatters_pre_commit_hooks.pre_conditions import java_required
from language_formatters_pre_commit_hooks.utils import download_url
from language_formatters_pre_commit_hooks.utils import run_command


GOOGLE_JAVA_FORMATTER_VERSION = '1.6'


def download_google_java_formatter_jar(version=GOOGLE_JAVA_FORMATTER_VERSION):  # pragma: no cover
    def get_url(_version):
        # Links extracted from https://github.com/google/google-java-format/
        return \
            'https://github.com/google/google-java-format/releases/download/' \
            'google-java-format-{version}/google-java-format-{version}-all-deps.jar'.format(
                version=_version,
            )

    return download_url(get_url(version))


@java_required
def pretty_format_java(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--autofix',
        action='store_true',
        dest='autofix',
        help='Automatically fixes encountered not-pretty-formatted files',
    )

    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    google_java_formatter_jar = download_google_java_formatter_jar()

    status, output = run_command(
        'java -jar {} --set-exit-if-changed --aosp {} {}'.format(
            google_java_formatter_jar,
            '--replace' if args.autofix else '--dry-run',
            ' '.join(args.filenames),
        ),
    )

    if output:
        print(
            '{}: {}'.format(
                'The following files have been fixed by google-java-formatter' if args.autofix else 'The following files are not properly formatted',  # noqa
                ', '.join(output.splitlines()),
            ),
        )

    return 0 if status == 0 else 1


if __name__ == '__main__':
    sys.exit(pretty_format_java())
