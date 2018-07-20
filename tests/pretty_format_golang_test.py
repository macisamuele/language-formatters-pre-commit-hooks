# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import shutil

import pytest

from language_formatters_pre_commit_hooks.pretty_format_golang import pretty_format_golang


@pytest.fixture(autouse=True)
def change_dir():
    working_directory = os.getcwd()
    try:
        os.chdir('test-data/pretty_format_golang/')
        yield
    finally:
        os.chdir(working_directory)


@pytest.mark.parametrize(
    ('filename', 'expected_retval'), (
        ('valid.go', 0),
        ('invalid.go', 1),
    ),
)
def test_pretty_format_golang(filename, expected_retval):
    assert pretty_format_golang([filename]) == expected_retval


def test_pretty_format_golang_autofix(tmpdir):
    srcfile = tmpdir.join('to_be_fixed.go')
    shutil.copyfile(
        'invalid.go',
        srcfile.strpath,
    )
    assert pretty_format_golang(['--autofix', srcfile.strpath]) == 1

    # file was formatted (shouldn't trigger linter again)
    ret = pretty_format_golang([srcfile.strpath])
    assert ret == 0
