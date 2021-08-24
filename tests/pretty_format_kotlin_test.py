# -*- coding: utf-8 -*-
import shutil

import pytest

from language_formatters_pre_commit_hooks.pretty_format_kotlin import pretty_format_kotlin
from tests import change_dir_context
from tests import run_autofix_test
from tests import undecorate_function


@pytest.fixture(autouse=True)
def change_dir():
    with change_dir_context("test-data/pretty_format_kotlin/"):
        yield


@pytest.fixture
def undecorate_method():
    # Method undecoration is needed to ensure that tests could be executed even if the tool is not installed
    with undecorate_function(pretty_format_kotlin) as undecorated:
        yield undecorated


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("invalid.kt", 1),
        ("pretty-formatted.kt", 0),
        ("not-pretty-formatted.kt", 1),
        ("not-pretty-formatted_fixed.kt", 0),
    ),
)
def test_pretty_format_kotlin(undecorate_method, filename, expected_retval):
    assert undecorate_method([filename]) == expected_retval


def test_pretty_format_kotlin_autofix(tmpdir, undecorate_method):
    run_autofix_test(tmpdir, undecorate_method, "not-pretty-formatted.kt", "not-pretty-formatted_fixed.kt")
