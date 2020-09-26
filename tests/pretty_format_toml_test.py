# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import shutil

import pytest

from language_formatters_pre_commit_hooks.pretty_format_toml import pretty_format_toml


@pytest.fixture(autouse=True)
def change_dir():
    working_directory = os.getcwd()
    try:
        os.chdir("test-data/pretty_format_toml/")
        yield
    finally:
        os.chdir(working_directory)


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("pretty-formatted.toml", 0),
        ("not-pretty-formatted.toml", 1),
        ("not-valid-file.toml", 1),
    ),
)
def test_pretty_format_toml(filename, expected_retval):
    assert pretty_format_toml([filename]) == expected_retval


def test_pretty_format_toml_autofix(tmpdir):
    srcfile = tmpdir.join("to_be_fixed.toml")
    shutil.copyfile(
        "not-pretty-formatted.toml",
        srcfile.strpath,
    )
    assert pretty_format_toml(["--autofix", srcfile.strpath]) == 1

    # file was formatted (shouldn't trigger linter again)
    ret = pretty_format_toml([srcfile.strpath])
    assert ret == 0
