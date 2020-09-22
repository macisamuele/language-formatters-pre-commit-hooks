# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys

from language_formatters_pre_commit_hooks.pre_conditions import java_required
from language_formatters_pre_commit_hooks.utils import download_url
from language_formatters_pre_commit_hooks.utils import run_command


__KTLINT_VERSION = "0.39.0"


def __download_kotlin_formatter_jar(version):  # pragma: no cover
    def get_url(_version):
        # Links extracted from https://github.com/pinterest/ktlint/
        return \
            'https://github.com/pinterest/ktlint/releases/download/{version}/ktlint'.format(
                version=_version,
            )

    url_to_download = get_url(version)
    try:
        return download_url(get_url(version), 'ktlint{version}.jar'.format(version=version))
    except:  # noqa: E722 (allow usage of bare 'except')
        raise RuntimeError(
            'Failed to download {url}. Probably the requested version, {version}, is '
            'not valid or you have some network issue.'.format(
                url=url_to_download, version=version,
            ),
        )


@java_required
def pretty_format_kotlin(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--autofix',
        action='store_true',
        dest='autofix',
        help='Automatically fixes encountered not-pretty-formatted files',
    )
    parser.add_argument(
        '--ktlint-version',
        dest='ktlint_version',
        default=__KTLINT_VERSION,
        help='KTLint version to use (default %(default)s)',
    )

    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    ktlint_jar = __download_kotlin_formatter_jar(
        args.ktlint_version,
    )

    # ktlint does not return exit-code!=0 if we're formatting them.
    # To workaround this limitation we do run ktlint in check mode only,
    # which provides the expected exit status and we run it again in format
    # mode if autofix flag is enabled
    check_status, check_output = run_command(
        'java -jar {} --verbose --relative -- {}'.format(
            ktlint_jar,
            ' '.join(set(args.filenames)),
        ),
    )

    not_pretty_formatted_files = set()
    if check_status != 0:
        not_pretty_formatted_files.update(
            line.split(':', 1)[0]
            for line in check_output.splitlines()
        )

        if args.autofix:
            print('Running ktlint format on {}'.format(not_pretty_formatted_files))
            run_command(
                'java -jar {} --verbose --relative --format -- {}'.format(
                    ktlint_jar,
                    ' '.join(not_pretty_formatted_files),
                ),
            )

    status = 0
    if not_pretty_formatted_files:
        status = 1
        print(
            '{}: {}'.format(
                'The following files have been fixed by ktlint' if args.autofix else 'The following files are not properly formatted',
                ', '.join(sorted(not_pretty_formatted_files)),
            ),
        )

    return status


if __name__ == '__main__':
    sys.exit(pretty_format_kotlin())
