# -*- coding: utf-8 -*-
import typing
from textwrap import dedent
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from packaging.version import Version

from language_formatters_pre_commit_hooks.pre_conditions import _is_command_success
from language_formatters_pre_commit_hooks.pre_conditions import _ToolRequired
from language_formatters_pre_commit_hooks.pre_conditions import assert_max_jdk_version
from language_formatters_pre_commit_hooks.pre_conditions import assert_min_jdk_version
from language_formatters_pre_commit_hooks.pre_conditions import get_jdk_version
from language_formatters_pre_commit_hooks.pre_conditions import golang_required
from language_formatters_pre_commit_hooks.pre_conditions import java_required
from language_formatters_pre_commit_hooks.pre_conditions import rust_required
from language_formatters_pre_commit_hooks.pre_conditions import ToolNotInstalled
from language_formatters_pre_commit_hooks.pre_conditions import UnableToVerifyJDKVersion


@pytest.fixture(params=[True, False])
def success(request):
    with patch(
        "language_formatters_pre_commit_hooks.pre_conditions.run_command",
        autospec=True,
        return_value=(0 if request.param else 1, "", ""),
    ):
        yield request.param


def test__is_command_success(success: bool) -> None:
    assert success == _is_command_success(
        "cmd",
        "with",
        "args",
    )


def test__ToolRequired(success: bool) -> None:
    decorator = _ToolRequired(tool_name="test", check_command=lambda _: success, download_install_url="url")
    assert decorator.is_tool_installed() == success

    def throw_exception():
        raise SyntaxError("This error is thrown by the decorated function")

    try:
        decorator(throw_exception)()
    except Exception as e:
        raised_exception = e

    if success:
        assert isinstance(raised_exception, SyntaxError)
    else:
        assert isinstance(raised_exception, ToolNotInstalled)
        assert raised_exception.tool_name == "test"
        assert raised_exception.download_install_url == "url"


@pytest.mark.parametrize(
    "decorator, assert_content",
    [
        [java_required, "JRE is required"],
        [golang_required, "golang/gofmt is required"],
        [rust_required, "rustfmt is required"],
    ],
)
def test_tool_required(success, decorator, assert_content):
    @decorator
    def func():
        pass

    raised_exception = None
    try:
        func()
    except ToolNotInstalled as e:
        raised_exception = e

    if success:
        assert raised_exception is None
    else:
        assert isinstance(raised_exception, ToolNotInstalled) and assert_content in str(raised_exception)


@patch(
    "language_formatters_pre_commit_hooks.pre_conditions.run_command",
    autospec=True,
    return_value=(1, "", ""),
)
def test_get_jdk_version_with_java_not_installed(_) -> None:
    with pytest.raises(RuntimeError):
        get_jdk_version()


@pytest.mark.parametrize(
    "command_output, expected_result",
    (
        ("", UnableToVerifyJDKVersion()),
        (
            dedent(
                """
                some output
                that does not reflect the expected format
                """
            ),
            UnableToVerifyJDKVersion(),
        ),
        (
            dedent(
                """

                Property settings:
                    file.encoding = UTF-8
                    file.separator = /
                    java.class.path =
                    java.class.version = 60.0
                    ...
                    java.version = 16.0.2
                    java.version.date = 2021-07-20
                    ...

                openjdk version "16.0.2" 2021-07-20
                OpenJDK Runtime Environment Homebrew (build 16.0.2+0)
                OpenJDK 64-Bit Server VM Homebrew (build 16.0.2+0, mixed mode, sharing)
                """
            ),
            Version("16.0.2"),
        ),
    ),
)
@patch(
    "language_formatters_pre_commit_hooks.pre_conditions.run_command",
    autospec=True,
)
def test_get_jdk_version(mock_run_comand: Mock, command_output: str, expected_result: typing.Union[Exception, Version]) -> None:
    mock_run_comand.return_value = (0, "", command_output)

    if isinstance(expected_result, Exception):
        with pytest.raises(type(expected_result)):
            get_jdk_version()
    elif isinstance(expected_result, Version):
        assert get_jdk_version() == expected_result

    else:
        assert False, "We should never ever getting here"  # pragma: no cover


@pytest.mark.parametrize("min_version_str, expected_error", (("11.0.0", False), ("15.0.0", False), ("16.0.0", True)))
@patch(
    "language_formatters_pre_commit_hooks.pre_conditions.get_jdk_version",
    autospec=True,
    return_value=Version("15.0.0"),
)
def test_assert_min_jdk_version(_: Mock, min_version_str: str, expected_error: bool) -> None:
    version = Version(min_version_str)

    try:
        assert_min_jdk_version(version)
    except ToolNotInstalled:
        raised_exception = True
    else:
        raised_exception = False

    assert raised_exception == expected_error


@pytest.mark.parametrize(
    "max_version_str, inclusive, expected_error",
    (
        ("11.0.0", True, True),
        ("11.0.0", False, True),
        ("15.0.0", True, False),
        ("15.0.0", False, True),
        ("16.0.0", True, False),
        ("16.0.0", False, False),
    ),
)
@patch(
    "language_formatters_pre_commit_hooks.pre_conditions.get_jdk_version",
    autospec=True,
    return_value=Version("15.0.0"),
)
def test_assert_max_jdk_version(_: Mock, max_version_str: str, inclusive: bool, expected_error: bool) -> None:
    version = Version(max_version_str)

    try:
        assert_max_jdk_version(version, inclusive=inclusive)
    except ToolNotInstalled:
        raised_exception = True
    else:
        raised_exception = False

    assert raised_exception == expected_error
