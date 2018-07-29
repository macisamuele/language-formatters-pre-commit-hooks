# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import shutil

import pytest

from language_formatters_pre_commit_hooks.pretty_format_java import pretty_format_java
from tests.conftest import change_dir_context
from tests.conftest import undecorate_function


@pytest.fixture(autouse=True)
def change_dir():
    with change_dir_context('test-data/pretty_format_java/'):
        yield


@pytest.fixture
def undecorate_method():
    # Method undecoration is needed to ensure that tests could be executed even if the tool is not installed
    with undecorate_function(pretty_format_java) as undecorated:
        yield undecorated


@pytest.mark.parametrize(
    ('filename', 'expected_retval'), (
        ('valid.java', 0),
        ('invalid.java', 1),
    ),
)
def test_pretty_format_java(undecorate_method, filename, expected_retval):
    assert undecorate_method([filename]) == expected_retval


def test_pretty_format_java_autofix(tmpdir, undecorate_method):
    srcfile = tmpdir.join('to_be_fixed.java')
    shutil.copyfile(
        'invalid.java',
        srcfile.strpath,
    )
    assert undecorate_method(['--autofix', srcfile.strpath]) == 1

    # file was formatted (shouldn't trigger linter again)
    ret = undecorate_method([srcfile.strpath])
    assert ret == 0
