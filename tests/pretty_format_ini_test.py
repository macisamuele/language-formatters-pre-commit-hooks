# -*- coding: utf-8 -*-
import os
import shutil

import pytest

from language_formatters_pre_commit_hooks.pretty_format_ini import pretty_format_ini


@pytest.fixture(autouse=True)
def change_dir():
    working_directory = os.getcwd()
    try:
        os.chdir("test-data/pretty_format_ini/")
        yield
    finally:
        os.chdir(working_directory)


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("issue_99.ini", 1),
        ("not-pretty-formatted.ini", 1),
        ("not-valid-file.ini", 1),
        ("pretty-formatted.ini", 0),
    ),
)
def test_pretty_format_ini(filename, expected_retval):
    assert pretty_format_ini([filename]) == expected_retval


def test_pretty_format_ini_autofix(tmpdir):
    srcfile = tmpdir.join("to_be_fixed.ini")
    shutil.copyfile(
        "not-pretty-formatted.ini",
        srcfile.strpath,
    )
    assert pretty_format_ini(["--autofix", srcfile.strpath]) == 1

    # file was formatted (shouldn't trigger linter again)
    ret = pretty_format_ini([srcfile.strpath])
    assert ret == 0
