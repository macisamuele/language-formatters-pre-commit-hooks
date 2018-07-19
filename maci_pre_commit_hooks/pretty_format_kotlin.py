from __future__ import print_function

import argparse
import sys

from maci_pre_commit_hooks import download_url
from maci_pre_commit_hooks import run_command


def download_google_kotlin_formatter_jar(version='0.24.0'):  # pragma: no cover
    def get_url(_version):
        # Links extracted from https://github.com/shyiko/ktlint/
        return \
            'https://github.com/shyiko/ktlint/releases/download/{version}/ktlint'.format(
                version=_version,
            )

    return download_url(get_url(version), 'ktlint{version}'.format(version=version))


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

    ktlint_jar = download_google_kotlin_formatter_jar()

    status, output = run_command('java -version')
    if status != 0:  # pragma: no cover
        # This is possible if kotlin is not available on the path, most probably because kotlin is not installed
        print(output)
        return 1

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
    _, output = run_command('git diff-index --name-status --binary --exit-code --no-ext-diff $(git write-tree) --')
    if output:
        print(
            '{}: {}'.format(
                'The following files have been fixed by ktlint' if args.autofix else 'The following files are not properly formatted',  # noqa
                ', '.join(line.split()[-1] for line in output.splitlines()),
            ),
        )
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(pretty_format_kotlin())
