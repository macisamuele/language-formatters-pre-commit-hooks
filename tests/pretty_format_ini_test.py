# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import shutil

import pytest
import six

from language_formatters_pre_commit_hooks.pretty_format_ini import pretty_format_ini


@pytest.fixture(autouse=True)
def change_dir():
    working_directory = os.getcwd()
    try:
        os.chdir('test-data/pretty_format_ini/')
        yield
    finally:
        os.chdir(working_directory)


@pytest.mark.parametrize(
    ('filename', 'expected_retval'), (
        pytest.mark.xfail(
            condition=not six.PY3,
            reason='ConfigParser writing format has changed between Python2 and Python3, let\'s test it only once',
        )(('pretty-formatted.ini', 0)),
        ('not-pretty-formatted.ini', 1),
        ('not-valid-file.ini', 1),
    ),
)
def test_pretty_format_ini(filename, expected_retval):
    assert pretty_format_ini([filename]) == expected_retval


def test_pretty_format_ini_autofix(tmpdir):
    srcfile = tmpdir.join('to_be_fixed.ini')
    shutil.copyfile(
        'not-pretty-formatted.ini',
        srcfile.strpath,
    )
    assert pretty_format_ini(['--autofix', srcfile.strpath]) == 1

    # file was formatted (shouldn't trigger linter again)
    ret = pretty_format_ini([srcfile.strpath])
    assert ret == 0
