# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import shutil

import pytest

from language_formatters_pre_commit_hooks.pretty_format_kotlin import pretty_format_kotlin
from language_formatters_pre_commit_hooks.utils import run_command
from tests.conftest import change_dir_context
from tests.conftest import undecorate_function


@pytest.fixture(autouse=True)
def change_dir():
    with change_dir_context('test-data/pretty_format_kotlin/'):
        yield


@pytest.fixture
def undecorate_method():
    # Method undecoration is needed to ensure that tests could be executed even if the tool is not installed
    with undecorate_function(pretty_format_kotlin) as undecorated:
        yield undecorated


@pytest.mark.parametrize(
    ('filename', 'expected_retval'), (
        ('valid.kt', 0),
        ('invalid.kt', 1),
    ),
)
def test_pretty_format_kotlin(undecorate_method, filename, expected_retval):
    assert undecorate_method([filename]) == expected_retval


def test_pretty_format_kotlin_autofix(tmpdir, undecorate_method):
    srcfile = tmpdir.join('to_be_fixed.kt')
    shutil.copyfile(
        'invalid.kt',
        srcfile.strpath,
    )
    with change_dir_context(tmpdir.strpath):
        # KTLint does not provide information if files have been formatted
        # so the only way is to check if there are non stashed files in the repo
        run_command('git init && git add {}'.format(srcfile.strpath))

        assert undecorate_method(['--autofix', srcfile.strpath]) == 1

        # Stage the file in the repository
        run_command('git add {}'.format(srcfile.strpath))

        # file was formatted (shouldn't trigger linter again)
        assert undecorate_method([srcfile.strpath]) == 0
