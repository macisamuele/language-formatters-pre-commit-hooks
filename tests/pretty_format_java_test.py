# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import shutil

import pytest

from language_formatters_pre_commit_hooks.pretty_format_java import pretty_format_java
from tests import change_dir_context
from tests import run_autofix_test
from tests import undecorate_function


@pytest.fixture(autouse=True)
def change_dir():
    with change_dir_context("test-data/pretty_format_java/"):
        yield


@pytest.fixture
def undecorate_method():
    # Method undecoration is needed to ensure that tests could be executed even if the tool is not installed
    with undecorate_function(pretty_format_java) as undecorated:
        yield undecorated


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("invalid.java", 1),
        ("pretty-formatted.java", 0),
        ("not-pretty-formatted.java", 1),
        ("not-pretty-formatted_fixed.java", 0),
    ),
)
def test_pretty_format_java(undecorate_method, filename, expected_retval):
    assert undecorate_method([filename]) == expected_retval


def test_pretty_format_java_autofix(tmpdir, undecorate_method):
    run_autofix_test(tmpdir, undecorate_method, "not-pretty-formatted.java", "not-pretty-formatted_fixed.java")
