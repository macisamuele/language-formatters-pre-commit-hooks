import os
import shutil

import pytest

from maci_pre_commit_hooks.pretty_format_java import pretty_format_java


@pytest.fixture(autouse=True)
def change_dir():
    working_directory = os.getcwd()
    try:
        os.chdir('test-data/pretty_format_java/')
        yield
    finally:
        os.chdir(working_directory)


@pytest.mark.parametrize(
    ('filename', 'expected_retval'), (
        ('valid.java', 0),
        ('invalid.java', 1),
    ),
)
def test_pretty_format_java(filename, expected_retval):
    assert pretty_format_java([filename]) == expected_retval


def test_pretty_format_java_autofix(tmpdir):
    srcfile = tmpdir.join('to_be_fixed.java')
    shutil.copyfile(
        'invalid.java',
        srcfile.strpath,
    )
    assert pretty_format_java(['--autofix', srcfile.strpath]) == 1

    # file was formatted (shouldn't trigger linter again)
    ret = pretty_format_java([srcfile.strpath])
    assert ret == 0
