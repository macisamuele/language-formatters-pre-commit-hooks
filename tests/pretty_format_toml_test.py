# -*- coding: utf-8 -*-
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


@pytest.mark.parametrize(
    ("filename", "args", "expected_retval"),
    (
        ("indent2-pretty-formatted.toml", [], 0),
        ("indent2-pretty-formatted.toml", ["--indent=4"], 1),
        ("indent4-pretty-formatted.toml", [], 1),
        ("indent4-pretty-formatted.toml", ["--indent=4"], 0),
        ("no-sort-pretty-formatted.toml", ["--no-sort"], 0),
        ("no-sort-pretty-formatted.toml", [], 1),
        ("inline-comment-2spaces-pretty-formatted.toml", [], 0),
        ("inline-comment-2spaces-pretty-formatted.toml", ["--inline-comment-spaces=2"], 0),
        ("inline-comment-1spaces-pretty-formatted.toml", [], 0),
        ("inline-comment-1spaces-pretty-formatted.toml", ["--inline-comment-spaces=2"], 1),
    ),
)
def test_pretty_format_toml_custom_cli_arguments(filename, args, expected_retval):
    assert pretty_format_toml([filename] + args) == expected_retval


def test_pretty_format_toml_autofix(tmpdir):
    run_autofix_test(
        tmpdir,
        pretty_format_toml,
        "not-pretty-formatted.toml",
        "not-pretty-formatted_fixed.toml",
    )
