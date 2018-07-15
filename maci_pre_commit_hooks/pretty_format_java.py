from __future__ import print_function

import argparse
import os
import shutil
import sys

import requests
from six.moves.urllib.parse import urlparse

from maci_pre_commit_hooks import run_command


def _base_directory():
    # Extracted from pre-commit code:
    # https://github.com/pre-commit/pre-commit/blob/master/pre_commit/store.py
    return os.environ.get('PRE_COMMIT_HOME') or os.path.join(
        os.environ.get('XDG_CACHE_HOME') or os.path.expanduser('~/.cache'),
        'pre-commit',
    )


def download_google_java_formatter_jar(version='1.6'):  # pragma: no cover
    def get_url(_version):
        # Links extracted from https://github.com/google/google-java-format/
        return \
            'https://github.com/google/google-java-format/releases/download/' \
            'google-java-format-{version}/google-java-format-{version}-all-deps.jar'.format(
                version=_version,
            )

    url = get_url(version)
    final_file = os.path.join(
        _base_directory(),
        os.path.basename(urlparse(url).path),
    )

    if os.path.exists(final_file):
        return final_file

    r = requests.get(url, stream=True)
    tmp_file = '{}_tmp.jar'.format(final_file)
    with open(tmp_file, mode='wb') as f:
        # Copy on a temporary file in case of issues while downloading the file
        shutil.copyfileobj(r.raw, f)

    os.rename(tmp_file, final_file)
    return final_file


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

    status, output = run_command('java -version')
    if status != 0:  # pragma: no cover
        # This is possible if java is not available on the path, most probably because java is not installed
        print(output)
        return 1

    status, output = run_command(
        'java -jar {} --set-exit-if-changed --aosp {} {}'.format(
            google_java_formatter_jar,
            '--replace' if args.autofix else '--dry-run',
            ' '.join(args.filenames),
        ),
    )

    if output:
        print(
            '{}: {}'
            'The following files have been fixed by google-java-formatter' if args.autofix else 'The following files are not properly formatted',  # noqa
            ', '.join(output.splitlines()),
        )

    return 0 if status == 0 else 1


if __name__ == '__main__':
    sys.exit(pretty_format_java())
