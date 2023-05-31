# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest

from language_formatters_pre_commit_hooks.pretty_format_golang import _get_eol_attribute
from language_formatters_pre_commit_hooks.pretty_format_golang import pretty_format_golang
from tests import change_dir_context
from tests import run_autofix_test
from tests import undecorate_function


@pytest.fixture(autouse=True)
def change_dir():
    with change_dir_context("test-data/pretty_format_golang/"):
        yield


@pytest.fixture
def undecorate_method():
    # Method undecoration is needed to ensure that tests could be executed even if the tool is not installed
    with undecorate_function(pretty_format_golang) as undecorated:
        yield undecorated


@pytest.mark.parametrize(
    "exit_status, output, expected_eol",
    [
        (1, "", None),
        (0, "", None),
        (0, "a\0eol\0lf\0", "lf"),
    ],
)
@patch("language_formatters_pre_commit_hooks.pretty_format_golang.run_command", autospec=True)
def test__get_eol_attribute(mock_run_command, exit_status, output, expected_eol):
    mock_run_command.return_value = (exit_status, output, "")
    assert _get_eol_attribute() == expected_eol


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("invalid.go", 1),
        ("pretty-formatted.go", 0),
        ("not-pretty-formatted.go", 1),
        ("not-pretty-formatted_fixed.go", 0),
    ),
)
def test_pretty_format_golang(undecorate_method, filename, expected_retval):
    assert undecorate_method([filename]) == expected_retval


def test_pretty_format_golang_autofix(tmpdir, undecorate_method):
    run_autofix_test(tmpdir, undecorate_method, "not-pretty-formatted.go", "not-pretty-formatted_fixed.go")
