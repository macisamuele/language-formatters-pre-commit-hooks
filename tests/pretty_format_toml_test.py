# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os

import pytest

from language_formatters_pre_commit_hooks.pretty_format_toml import pretty_format_toml
from tests import run_autofix_test


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
        ("invalid.toml", 1),
        ("pretty-formatted.toml", 0),
        ("not-pretty-formatted.toml", 1),
        ("not-pretty-formatted_fixed.toml", 0),
    ),
)
def test_pretty_format_toml(filename, expected_retval):
    assert pretty_format_toml([filename]) == expected_retval


def test_pretty_format_toml_autofix(tmpdir):
    run_autofix_test(
        tmpdir,
        pretty_format_toml,
        "not-pretty-formatted.toml",
        "not-pretty-formatted_fixed.toml",
    )
