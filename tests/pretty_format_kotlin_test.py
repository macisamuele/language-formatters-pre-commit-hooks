# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import shutil
from contextlib import contextmanager

import pytest

from language_formatters_pre_commit_hooks.pretty_format_kotlin import pretty_format_kotlin
from language_formatters_pre_commit_hooks.utils import run_command


@contextmanager
def _change_dir(directory):
    working_directory = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(working_directory)


@pytest.fixture(autouse=True)
def change_dir():
    with _change_dir('test-data/pretty_format_kotlin/'):
        yield


@pytest.mark.parametrize(
    ('filename', 'expected_retval'), (
        ('valid.kt', 0),
        ('invalid.kt', 1),
    ),
)
def test_pretty_format_java(filename, expected_retval):
    assert pretty_format_kotlin([filename]) == expected_retval


def test_pretty_format_kotlin_autofix(tmpdir):
    srcfile = tmpdir.join('to_be_fixed.kt')
    shutil.copyfile(
        'invalid.kt',
        srcfile.strpath,
    )
    with _change_dir(tmpdir.dirname):
        # KTLint does not provide information if files have been formatted
        # so the only way is to check if there are non stashed files in the repo
        run_command('git init && git add {}'.format(srcfile.strpath))

        assert pretty_format_kotlin(['--autofix', srcfile.strpath]) == 1

        # Stage the file in the repository
        run_command('git add {}'.format(srcfile.strpath))

        # file was formatted (shouldn't trigger linter again)
        assert pretty_format_kotlin([srcfile.strpath]) == 0
