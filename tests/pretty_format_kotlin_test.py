# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest
from packaging.version import Version

from language_formatters_pre_commit_hooks import _get_default_version
from language_formatters_pre_commit_hooks.pre_conditions import get_jdk_version
from language_formatters_pre_commit_hooks.pretty_format_kotlin import _download_kotlin_formatter_jar
from language_formatters_pre_commit_hooks.pretty_format_kotlin import pretty_format_kotlin
from tests import change_dir_context
from tests import run_autofix_test
from tests import undecorate_function
from tests import UnexpectedStatusCode


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
    (_get_default_version("ktlint"),),
)
@pytest.mark.integration
def test__download_kotlin_formatter_jar(ensure_download_possible, version):  # noqa: F811
    _download_kotlin_formatter_jar(version)


@pytest.mark.parametrize(
    ("filename", "expected_retval"),
    (
        ("Invalid.kt", 1),
        ("PrettyPormatted.kt", 0),
        ("NotPrettyFormatted.kt", 1),
        ("NotPrettyFormattedFixed.kt", 0),
    ),
)
@pytest.mark.skipif(condition=get_jdk_version() >= Version("16"), reason="Skipping test because it requires Java JDK lower than 16")
def test_pretty_format_kotlin(undecorate_method, filename, expected_retval):
    assert undecorate_method([filename]) == expected_retval


@pytest.mark.skipif(condition=get_jdk_version() >= Version("16"), reason="Skipping test because it requires Java JDK lower than 16")
def test_pretty_format_kotlin_autofix(tmpdir, undecorate_method):
    run_autofix_test(tmpdir, undecorate_method, "NotPrettyFormatted.kt", "NotPrettyFormattedFixed.kt")


@pytest.mark.skipif(condition=get_jdk_version() < Version("16"), reason="Skipping test because it requires Java JDK 16+")
def test_ktlint_does_not_yet_support_java_16_or_more(tmpdir, undecorate_method):
    """
    Test that running pretty-format-kotlin with Java 16+ is still not supported.
    The test is meant to be an early indicator that Java 16+ is now supported and as such
    `assert_max_jdk_version(...)` invocation can be removed from `pretty_format_kotlin.py` file
    """
    with patch(
        "language_formatters_pre_commit_hooks.pretty_format_kotlin.assert_max_jdk_version",
        autospec=True,
        return_value=None,
    ), pytest.raises(UnexpectedStatusCode):
        run_autofix_test(tmpdir, undecorate_method, "NotPrettyFormatted.kt", "NotPrettyFormattedFixed.kt")
