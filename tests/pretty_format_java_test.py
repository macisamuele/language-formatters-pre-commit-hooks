# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest
from packaging.version import Version

from language_formatters_pre_commit_hooks import _get_default_version
from language_formatters_pre_commit_hooks.pre_conditions import get_jdk_version
from language_formatters_pre_commit_hooks.pre_conditions import ToolNotInstalled
from language_formatters_pre_commit_hooks.pretty_format_java import _download_google_java_formatter_jar
from language_formatters_pre_commit_hooks.pretty_format_java import _download_palantir_java_formatter_jar
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
    "version",
    (
        _get_default_version("google_java_formatter"),
        # The following explicit versions are needed because the format
        # of the binary URL has changed on release 1.10.0
        "1.9",
        "1.10.0",
    ),
)
@pytest.mark.integration
def test__download_google_java_formatter_jar(ensure_download_possible, version):  # noqa: F811
    # Test that we can download different version of the Google Java Formatter
    _download_google_java_formatter_jar(version)


@pytest.mark.parametrize(
    "version",
    (_get_default_version("palantir"),),
)
@pytest.mark.integration
def test__download_palantir_java_formatter_jar(ensure_download_possible, version):  # noqa: F811
    # Test that we can download different version of the Google Java Formatter
    _download_palantir_java_formatter_jar(version)


@pytest.mark.parametrize(
    ("cli_args", "expected_retval"),
    (
        (["invalid.java"], 1),
        (["pretty-formatted.java"], 0),
        pytest.param(
            [
                "pretty-formatted.java",
                "--google-java-formatter-version=1.21.0",
                "--formatter-jar-checksum=1e69f8b63c39a5124a8efb7bad213eb9ac03944339eb9580ae210b0c60565d9b",
            ],
            0,
            id="valid checksum",
        ),
        pytest.param(
            [
                "pretty-formatted.java",
                "--google-java-formatter-version=1.21.0",
                "--formatter-jar-checksum=2d32af8ef04ffbf0ae77fc7953e86871b85143b29d51f9794466842f68f5fb48",
            ],
            1,
            id="invalid checksum",
        ),
        (["not-pretty-formatted.java"], 1),
        (["not-pretty-formatted_fixed.java"], 0),
    ),
)
def test_google_pretty_format_java(undecorate_method, cli_args, expected_retval):
    assert undecorate_method(cli_args) == expected_retval


@pytest.mark.skipif(condition=get_jdk_version() >= Version("21"), reason="Skipping test because it requires Java JDK before 21")
@pytest.mark.parametrize(
    ("cli_args", "expected_retval"),
    (
        (["--palantir", "invalid.java"], 1),
        (["--palantir", "pretty-formatted_palantir.java"], 0),
        (["--palantir", "not-pretty-formatted.java"], 1),
        (["--palantir", "not-pretty-formatted_fixed_palantir.java"], 0),
    ),
)
def test_palantir_pretty_format_java(undecorate_method, cli_args, expected_retval):
    assert undecorate_method(cli_args) == expected_retval


@pytest.mark.skipif(condition=get_jdk_version() < Version("16"), reason="Skipping test because it requires Java JDK 16+")
def test_google_pretty_format_java_up_to_1_9_is_not_allowed_on_jdk_16_and_above(undecorate_method):
    with pytest.raises(ToolNotInstalled, match="JRE: version < 16.0 is required to run this pre-commit hook."):
        undecorate_method(["--google-java-formatter-version=1.9", "pretty-formatted.java"])


@pytest.mark.skipif(condition=get_jdk_version() >= Version("16"), reason="Skipping test because it requires Java JDK before 16")
def test_google_pretty_format_java_up_to_1_9_is_allowed_on_jdk_before_16(undecorate_method):
    undecorate_method(["--google-java-formatter-version=1.9", "pretty-formatted.java"])


@pytest.mark.skipif(True, reason="No publication of old palantir versions has been requested")
@pytest.mark.skipif(condition=get_jdk_version() <= Version("11"), reason="Skipping test because it requires Java JDK above 11")
def test_palantir_pretty_format_java_up_to_1_9_is_allowed_on_jdk_11_and_above(undecorate_method):
    undecorate_method(["--palantir", "--palantir-java-formatter-version=1.9", "pretty-formatted.java"])


def test_google_pretty_format_java_autofix(tmpdir, undecorate_method):
    run_autofix_test(tmpdir, undecorate_method, "not-pretty-formatted.java", "not-pretty-formatted_fixed.java")


def test_palantir_pretty_format_java_autofix(tmpdir, undecorate_method):
    run_autofix_test(tmpdir, undecorate_method, "not-pretty-formatted.java", "not-pretty-formatted_fixed.java")


@pytest.mark.parametrize(
    ("cli_arg", "expected_retval"),
    (
        ("--google-java-formatter-jar=google-java-format-1.16.0-all-deps.jar", 0),
        ("", 0),
    ),
)
@patch("language_formatters_pre_commit_hooks.pretty_format_java.run_command", autospec=True)
def test_google_pretty_format_java_jar(mock_run_command, undecorate_method, cli_arg, expected_retval):
    mock_run_command.return_value = (0, "", "")
    assert undecorate_method([cli_arg, "pretty-formatted.java"]) == expected_retval
    in_args = cli_arg in mock_run_command.call_args.args
    if cli_arg == "":
        assert in_args
    else:
        assert not in_args


@pytest.mark.parametrize(
    ("cli_arg", "expected_retval"),
    (
        ("--palantir-java-formatter-jar=palantir-java-format-2.40.0-standalone.jar", 0),
        ("", 0),
    ),
)
@patch("language_formatters_pre_commit_hooks.pretty_format_java.run_command", autospec=True)
def test_palantir_pretty_format_java_jar(mock_run_command, undecorate_method, cli_arg, expected_retval):
    mock_run_command.return_value = (0, "", "")
    assert undecorate_method(["--palantir", cli_arg, "pretty-formatted.java"]) == expected_retval
    in_args = cli_arg in mock_run_command.call_args.args
    if cli_arg == "":
        assert in_args
    else:
        assert not in_args
