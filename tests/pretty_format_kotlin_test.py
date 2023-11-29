# -*- coding: utf-8 -*-
import pytest

from language_formatters_pre_commit_hooks import _get_default_version
from language_formatters_pre_commit_hooks.pretty_format_kotlin import \
    _download_ktlint_formatter_jar, _download_ktfmt_formatter_jar
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
    "version",
    sorted(
        {
            _get_default_version("ktlint"),
            "0.41.0",
            "0.42.0",
            "0.42.1",
            "0.43.0",
            "0.43.2",
            "0.44.0",
            "0.45.0",
            "0.45.1",
            "0.45.2",
            "0.46.0",
            "0.46.1",
            "0.47.0",
            "0.47.1",
        }
    ),
)
@pytest.mark.integration
def test__download_kotlin_formatter_jar(ensure_download_possible, version):  # noqa: F811
    _download_ktlint_formatter_jar(version)

@pytest.mark.parametrize(
    "version",
    sorted(
        {
            _get_default_version("ktfmt"),
            "0.45",
            "0.46",
        }
    ),
)
@pytest.mark.integration
def test__download_kotlin_formatter_jar(ensure_download_possible, version):  # noqa: F811
    _download_ktfmt_formatter_jar(version)

@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("Invalid.kt", 1),
        ("PrettyPormatted.kt", 0),
        ("NotPrettyFormatted.kt", 1),
        ("NotPrettyFormattedFixed.kt", 0),
    ),
)
def test_pretty_format_kotlin_ktlint(undecorate_method, filename, expected_retval):
    assert undecorate_method([filename]) == expected_retval


@pytest.mark.parametrize(
    ("filename", "expected_retval", "extra_parameters"),
    (
        ("Invalid.kt", 1, []),
        ("PrettyFormatted.kt", 0, []),
        ("NotPrettyFormatted.kt", 1, []),
        ("NotPrettyFormattedFixedKtlint.kt", 0, []),
        # ktfmt dropbox style (same as kotlinlang in this example)
        ("NotPrettyFormattedFixedKtfmtDropbox.kt", 1, ["--ktfmt"]),
        ("NotPrettyFormattedFixedKtfmtDropbox.kt", 0, ["--ktfmt", "--ktfmt-style=dropbox"]),
        ("NotPrettyFormattedFixedKtfmtDropbox.kt", 1, ["--ktfmt", "--ktfmt-style=google"]),
        ("NotPrettyFormattedFixedKtfmtDropbox.kt", 0, ["--ktfmt", "--ktfmt-style=kotlinlang"]),
        # ktfmt google style
        ("NotPrettyFormattedFixedKtfmtGoogle.kt", 0, ["--ktfmt"]),
        ("NotPrettyFormattedFixedKtfmtGoogle.kt", 1, ["--ktfmt", "--ktfmt-style=dropbox"]),
        ("NotPrettyFormattedFixedKtfmtGoogle.kt", 0, ["--ktfmt", "--ktfmt-style=google"]),
        ("NotPrettyFormattedFixedKtfmtGoogle.kt", 1, ["--ktfmt", "--ktfmt-style=kotlinlang"]),
        # ktfmt kotlinlang style (same as dropbox in this example)
        ("NotPrettyFormattedFixedKtfmtKotlinlang.kt", 1, ["--ktfmt"]),
        ("NotPrettyFormattedFixedKtfmtKotlinlang.kt", 0, ["--ktfmt", "--ktfmt-style=dropbox"]),
        ("NotPrettyFormattedFixedKtfmtKotlinlang.kt", 1, ["--ktfmt", "--ktfmt-style=google"]),
        ("NotPrettyFormattedFixedKtfmtKotlinlang.kt", 0, ["--ktfmt", "--ktfmt-style=kotlinlang"]),
        # ktfmt other files
        ("NotPrettyFormatted.kt", 1, ["--ktfmt"]),
        ("Invalid.kt", 1, ["--ktfmt"]),
    )
)
def test_pretty_format_kotlin(undecorate_method, filename, expected_retval, extra_parameters):
    assert undecorate_method(extra_parameters + [filename]) == expected_retval


@pytest.mark.parametrize(
    ("filename", "fixed_filename", "extra_parameters"),
    (
        ("NotPrettyFormatted.kt", "NotPrettyFormattedFixedKtlint.kt", ["--autofix"]),
        ("NotPrettyFormatted.kt", "NotPrettyFormattedFixedKtfmtGoogle.kt", ["--autofix", "--ktfmt"]),
        ("NotPrettyFormatted.kt", "NotPrettyFormattedFixedKtfmtGoogle.kt", ["--autofix", "--ktfmt", "--ktfmt-style=google"]),
        ("NotPrettyFormatted.kt", "NotPrettyFormattedFixedKtfmtDropbox.kt", ["--autofix", "--ktfmt", "--ktfmt-style=dropbox"]),
        ("NotPrettyFormatted.kt", "NotPrettyFormattedFixedKtfmtKotlinlang.kt", ["--autofix", "--ktfmt", "--ktfmt-style=kotlinlang"]),
    ),
)
def test_pretty_format_kotlin_autofix(tmpdir, undecorate_method, filename, fixed_filename, extra_parameters):
    run_autofix_test(
        tmpdir,
        undecorate_method,
        filename,
        fixed_filename,
        extra_parameters
    )
