# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import shutil

import pytest

from language_formatters_pre_commit_hooks.pretty_format_rust import pretty_format_rust
from tests.conftest import change_dir_context
from tests.conftest import undecorate_function


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
        ("valid/src/main.rs", 0),
        ("invalid/src/main.rs", 1),
    ),
)
def test_pretty_format_rust(undecorate_method, filename, expected_retval):
    filename = os.path.abspath(filename)
    with change_dir_context(os.path.dirname(os.path.dirname(filename))):
        assert undecorate_method([filename]) == expected_retval


def test_pretty_format_rust_autofix(tmpdir, undecorate_method):
    cargo_file = tmpdir.join("Cargo.toml")
    shutil.copyfile("invalid/Cargo.toml", cargo_file.strpath)

    tmpdir.mkdir("src")
    src_file = tmpdir.join("src", "main.rs")
    shutil.copyfile("invalid/src/main.rs", src_file.strpath)

    with change_dir_context(tmpdir.strpath):
        assert undecorate_method(["--autofix", src_file.strpath]) == 1

        # file was formatted (shouldn't trigger linter again)
        ret = undecorate_method([src_file.strpath])
        assert ret == 0
