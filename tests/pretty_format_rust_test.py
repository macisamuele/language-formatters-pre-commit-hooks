# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
from shutil import copyfile

import pytest

from language_formatters_pre_commit_hooks.pretty_format_rust import pretty_format_rust
from tests import change_dir_context
from tests import run_autofix_test
from tests import undecorate_function


@pytest.fixture(autouse=True)
def change_dir():
    with change_dir_context("test-data/pretty_format_rust/"):
        yield


@pytest.fixture
def undecorate_method():
    # Method undecoration is needed to ensure that tests could be executed even if the tool is not installed
    with undecorate_function(pretty_format_rust) as undecorated:
        yield undecorated


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("invalid/src/main.rs", 1),
        ("pretty-formatted/src/main.rs", 0),
        ("not-pretty-formatted/src/main.rs", 1),
        ("not-pretty-formatted_fixed/src/main.rs", 0),
    ),
)
def test_pretty_format_rust(undecorate_method, filename, expected_retval):
    filename = os.path.abspath(filename)
    x = os.path.dirname(os.path.dirname(filename))
    print(x)
    with change_dir_context(x):
        assert undecorate_method([filename]) == expected_retval


def test_pretty_format_rust_autofix(tmpdir, undecorate_method):
    copyfile("not-pretty-formatted/Cargo.toml", tmpdir.join("Cargo.toml").strpath)
    run_autofix_test(tmpdir, undecorate_method, "not-pretty-formatted/src/main.rs", "not-pretty-formatted_fixed/src/main.rs")
