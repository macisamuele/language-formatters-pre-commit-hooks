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
        ("not-pretty-formatted_subdir/src/bin/src/main.rs", 1),
    ),
)
def test_pretty_format_rust(undecorate_method, filename, expected_retval):
    manifest_root = filename.split("/")[0]
    manifest_root = os.path.abspath(manifest_root)
    filename = os.path.abspath(filename)

    with change_dir_context(manifest_root):
        assert undecorate_method([filename]) == expected_retval


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("invalid/src/main.rs", 1),
        ("pretty-formatted/src/main.rs", 0),
        ("not-pretty-formatted/src/main.rs", 1),
        ("not-pretty-formatted_fixed/src/main.rs", 0),
        ("not-pretty-formatted_subdir/src/bin/src/main.rs", 1),
    ),
)
def test_pretty_format_rust_manifest(undecorate_method, filename, expected_retval):
    manifest_root = filename.split("/")[0]
    manifest_root = os.path.abspath(manifest_root)
    filename = os.path.abspath(filename)

    manifest_file = os.path.join(manifest_root, "Cargo.toml")
    print(manifest_file)
    assert undecorate_method(["--manifest-path", manifest_file, filename]) == expected_retval


def test_pretty_format_rust_autofix(tmpdir, undecorate_method):
    copyfile("not-pretty-formatted/Cargo.toml", tmpdir.join("Cargo.toml").strpath)
    run_autofix_test(tmpdir, undecorate_method, "not-pretty-formatted/src/main.rs", "not-pretty-formatted_fixed/src/main.rs")


@pytest.mark.xfail
def test_pretty_format_rust_autofix_subdir_no_manifest_arg(tmpdir, undecorate_method):
    copyfile("not-pretty-formatted_subdir/Cargo.toml", tmpdir.join("Cargo.toml").strpath)
    run_autofix_test(
        tmpdir.mkdir("src").mkdir("bin"),
        undecorate_method,
        "not-pretty-formatted_subdir/src/bin/src/main.rs",
        "not-pretty-formatted_fixed/src/main.rs",
    )


def test_pretty_format_rust_autofix_subdir(tmpdir, undecorate_method):
    copyfile("not-pretty-formatted_subdir/Cargo.toml", tmpdir.join("Cargo.toml").strpath)
    run_autofix_test(
        tmpdir.mkdir("src").mkdir("bin"),
        undecorate_method,
        "not-pretty-formatted_subdir/src/bin/src/main.rs",
        "not-pretty-formatted_fixed/src/main.rs",
        ["--manifest-path", "../../Cargo.toml"],
    )
