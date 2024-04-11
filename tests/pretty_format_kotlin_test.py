import pytest

from language_formatters_pre_commit_hooks import _get_default_version
from language_formatters_pre_commit_hooks.pretty_format_kotlin import _download_ktfmt_formatter_jar
from language_formatters_pre_commit_hooks.pretty_format_kotlin import _download_ktlint_formatter_jar
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
def test__download_kotlin_formatter_jar_ktlint(ensure_download_possible, version):  # noqa: F811
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
def test__download_kotlin_formatter_jar_ktfmt(ensure_download_possible, version):  # noqa: F811
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
    ("filename", "expected_retval"),
    (
        ("NotPrettyFormattedFixedKtfmtDropbox.kt", 1),
        ("NotPrettyFormattedFixedKtfmtGoogle.kt", 0),
        ("NotPrettyFormattedFixedKtfmtKotlinlang.kt", 1),
        ("NotPrettyFormatted.kt", 1),
        ("Invalid.kt", 1),
    ),
)
def test_pretty_format_kotlin_ktfmt(undecorate_method, filename, expected_retval):
    assert undecorate_method(["--ktfmt", filename]) == expected_retval


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("NotPrettyFormattedFixedKtfmtDropbox.kt", 0),
        ("NotPrettyFormattedFixedKtfmtGoogle.kt", 1),
        ("NotPrettyFormattedFixedKtfmtKotlinlang.kt", 0),
        ("NotPrettyFormatted.kt", 1),
        ("Invalid.kt", 1),
    ),
)
def test_pretty_format_kotlin_ktfmt_dropbox_style(undecorate_method, filename, expected_retval):
    assert undecorate_method(["--ktfmt", "--ktfmt-style=dropbox", filename]) == expected_retval


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("NotPrettyFormattedFixedKtfmtDropbox.kt", 1),
        ("NotPrettyFormattedFixedKtfmtGoogle.kt", 0),
        ("NotPrettyFormattedFixedKtfmtKotlinlang.kt", 1),
        ("NotPrettyFormatted.kt", 1),
        ("Invalid.kt", 1),
    ),
)
def test_pretty_format_kotlin_ktfmt_google_style(undecorate_method, filename, expected_retval):
    assert undecorate_method(["--ktfmt", "--ktfmt-style=google", filename]) == expected_retval


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("NotPrettyFormattedFixedKtfmtDropbox.kt", 0),
        ("NotPrettyFormattedFixedKtfmtGoogle.kt", 1),
        ("NotPrettyFormattedFixedKtfmtKotlinlang.kt", 0),
        ("NotPrettyFormatted.kt", 1),
        ("Invalid.kt", 1),
    ),
)
def test_pretty_format_kotlin_ktfmt_kotlinglang_style(undecorate_method, filename, expected_retval):
    assert undecorate_method(["--ktfmt", "--ktfmt-style=kotlinlang", filename]) == expected_retval


@pytest.mark.parametrize(
    ("filename", "fixed_filename", "extra_parameters"),
    (
        ("NotPrettyFormatted.kt", "NotPrettyFormattedFixedKtlint.kt", []),
        ("NotPrettyFormatted.kt", "NotPrettyFormattedFixedKtfmtGoogle.kt", ["--ktfmt"]),
        ("NotPrettyFormatted.kt", "NotPrettyFormattedFixedKtfmtGoogle.kt", ["--ktfmt", "--ktfmt-style=google"]),
        ("NotPrettyFormatted.kt", "NotPrettyFormattedFixedKtfmtDropbox.kt", ["--ktfmt", "--ktfmt-style=dropbox"]),
        ("NotPrettyFormatted.kt", "NotPrettyFormattedFixedKtfmtKotlinlang.kt", ["--ktfmt", "--ktfmt-style=kotlinlang"]),
    ),
)
def test_pretty_format_kotlin_autofix(tmpdir, undecorate_method, filename, fixed_filename, extra_parameters):
    run_autofix_test(tmpdir, undecorate_method, filename, fixed_filename, extra_parameters)
