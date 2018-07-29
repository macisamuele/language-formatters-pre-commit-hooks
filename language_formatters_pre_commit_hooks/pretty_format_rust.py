# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import sys

from language_formatters_pre_commit_hooks.pre_conditions import rust_required
from language_formatters_pre_commit_hooks.utils import run_command


@rust_required
def pretty_format_rust(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--autofix',
        action='store_true',
        dest='autofix',
        help='Automatically fixes encountered not-pretty-formatted files',
    )

    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    # Check
    _, output = run_command(
        'cargo +nightly fmt  -- --check {}'.format(
            ' '.join(args.filenames),
        ),
    )
    not_well_formatted_files = sorted(
        line.split()[2]
        for line in output.splitlines()
        if line.startswith('Diff in ')
    )
    if not_well_formatted_files:
        print(
            '{}: {}'.format(
                'The following files have been fixed by cargo format' if args.autofix else 'The following files are not properly formatted',
                ', '.join(not_well_formatted_files),
            ),
        )
        if args.autofix:
            run_command(
                'cargo +nightly fmt  -- {}'.format(
                    ' '.join(not_well_formatted_files),
                ),
            )

    return 1 if not_well_formatted_files else 0


if __name__ == '__main__':
    sys.exit(pretty_format_rust())
