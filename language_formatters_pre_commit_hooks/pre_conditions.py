# -*- coding: utf-8 -*-
import re
import typing
from functools import wraps
from os import getenv

from packaging.version import Version

from language_formatters_pre_commit_hooks.utils import run_command


F = typing.TypeVar("F", bound=typing.Callable[..., int])


def _is_command_success(
    *command_args: str,
    output_should_match: typing.Optional[typing.Callable[[str], bool]] = None,
) -> bool:
    exit_status, output = run_command(*command_args)
    return exit_status == 0 and (output_should_match is None or output_should_match(output))


class ToolNotInstalled(RuntimeError):
    def __init__(self, tool_name: str, download_install_url: str) -> None:
        self.tool_name = tool_name
        self.download_install_url = download_install_url

    def __str__(self) -> str:
        return str(
            "{tool_name} is required to run this pre-commit hook.\n"
            "Make sure that you have it installed and available on your path.\n"
            "Download/Install URL: {download_install_url}".format(
                tool_name=self.tool_name,
                download_install_url=self.download_install_url,
            )
        )


class _ToolRequired:
    def __init__(
        self,
        tool_name: str,
        check_command: typing.Callable[[typing.Optional[typing.Mapping[str, typing.Any]]], bool],
        download_install_url: str,
        extras: typing.Optional[typing.Mapping[str, typing.Any]] = None,
    ) -> None:
        self.tool_name = tool_name
        self.check_command = check_command
        self.download_install_url = download_install_url
        self.extras = extras

    def is_tool_installed(self) -> bool:
        return self.check_command(self.extras)

    def assert_tool_installed(self) -> None:
        if not self.is_tool_installed():
            raise ToolNotInstalled(
                tool_name=self.tool_name,
                download_install_url=self.download_install_url,
            )

    def __call__(self, f: F) -> F:
        @wraps(f)
        def wrapper(*args: typing.Any, **kwargs: typing.Any) -> int:
            self.assert_tool_installed()
            return f(*args, **kwargs)

        return wrapper  # type: ignore


java_required = _ToolRequired(
    tool_name="JRE",
    check_command=lambda _: _is_command_success("java", "-version"),
    download_install_url="https://www.java.com/en/download/",
)

golang_required = _ToolRequired(
    tool_name="golang/gofmt",
    check_command=lambda _: _is_command_success("go", "version"),
    download_install_url="https://golang.org/doc/install#download",
)


rust_required = _ToolRequired(
    tool_name="rustfmt",
    check_command=(lambda _: _is_command_success("cargo", "+{}".format(getenv("RUST_TOOLCHAIN", "stable")), "fmt", "--", "--version")),
    download_install_url="https://github.com/rust-lang-nursery/rustfmt#quick-start",
)


class UnableToVerifyJDKVersion(RuntimeError):
    def __str__(self) -> str:
        return "Unable to verify the JDK version"  # pragma: no cover


def get_jdk_version() -> Version:
    """
    Extract the version of the JDK accessible by the tool.

    :raises UnableToVerifyJDKVersion: if it was not possible to gather the JDK version
        This includes the case of `java` binary is not found in the path.
    """
    _, output = run_command("java", "-XshowSettings:properties", "-version")
    try:
        java_property_line = next(line for line in output.splitlines() if re.match(r"^\s+java.version\s+=\s+[^s]+$", line))
        return Version(java_property_line.split()[-1])
    except Exception as e:
        raise UnableToVerifyJDKVersion() from e


def assert_min_jdk_version(version: Version) -> None:
    """
    Ensure that the version of the accessible JDK is at least at the provided version.

    :raises UnableToVerifyJDKVersion: if it was not possible to gather the JDK version
        This includes the case of `java` binary is not found in the path.
    :raises ToolNotInstalled: if `java` binary is found in the path but the JDK version does not
        respect the min version requirement
    """
    _ToolRequired(
        tool_name=f"JRE: min version {version}",
        check_command=lambda extras: bool(extras and get_jdk_version() >= extras["min_sdk"]),
        download_install_url="https://www.java.com/en/download/",
        extras={"min_sdk": version},
    ).assert_tool_installed()


def assert_max_jdk_version(version: Version, *, inclusive: bool = False) -> None:
    """
    Ensure that the version of the accessible JDK is at most at the provided version.
    The inclusive parameter allows us to include or exclude the specified version:
    * if `inclusive=True` then `get_jdk_version() <= version` is evaluated
    * if `inclusive=False` then `get_jdk_version() < version` is evaluated
      NOTE: The missing `=` in the operation

    :raises UnableToVerifyJDKVersion: if it was not possible to gather the JDK version
        This includes the case of `java` binary is not found in the path.
    :raises ToolNotInstalled: if `java` binary is found in the path but the JDK version does not
        respect the max version requirement
    """
    if inclusive:
        tool_name = f"JRE: version <= {version}"
    else:
        tool_name = f"JRE: version < {version}"

    _ToolRequired(
        tool_name=tool_name,
        check_command=lambda extras: bool(
            extras and (get_jdk_version() <= extras["max_sdk"] if inclusive else get_jdk_version() < extras["max_sdk"])
        ),
        download_install_url="https://www.java.com/en/download/",
        extras={"max_sdk": version},
    ).assert_tool_installed()
