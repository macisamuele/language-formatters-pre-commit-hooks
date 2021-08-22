# -*- coding: utf-8 -*-
import argparse
import sys
import typing

import requests
from packaging.version import Version

from language_formatters_pre_commit_hooks import _get_default_version
from language_formatters_pre_commit_hooks.pre_conditions import assert_max_jdk_version
from language_formatters_pre_commit_hooks.pre_conditions import java_required
from language_formatters_pre_commit_hooks.utils import download_url
from language_formatters_pre_commit_hooks.utils import run_command


def _download_google_java_formatter_jar(version: str) -> str:  # pragma: no cover
    def get_urls(_version: str) -> typing.List[str]:
        # Links extracted from https://github.com/google/google-java-format/
        return [
            "https://github.com/google/google-java-format/releases/download/"
            "v{version}/google-java-format-{version}-all-deps.jar".format(
                version=_version,
            ),
            # Versions older than 1.10 have a different template
            "https://github.com/google/google-java-format/releases/download/"
            "google-java-format-{version}/google-java-format-{version}-all-deps.jar".format(
                version=_version,
            ),
        ]

    possible_urls = get_urls(version)
    try:
        for url_to_download in possible_urls:
            try:
                return download_url(url_to_download, "google-java-formatter{version}.jar".format(version=version))
            except requests.HTTPError as e:
                if e.response.status_code != 404:
                    # If the url was not found then move forward with the next links
                    raise

        raise RuntimeError("Failed to load any of the provided links")
    except:  # noqa: E722 (allow usage of bare 'except')
        raise RuntimeError(
            "Failed to download any of: {urls}. Probably the requested version, "
            "{version}, is not valid or you have some network issue.".format(
                urls=", ".join(possible_urls),
                version=version,
            ),
        )


@java_required
def pretty_format_java(argv: typing.Optional[typing.List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--autofix",
        action="store_true",
        dest="autofix",
        help="Automatically fixes encountered not-pretty-formatted files",
    )
    parser.add_argument(
        "--google-java-formatter-version",
        dest="google_java_formatter_version",
        default=_get_default_version("google_java_formatter"),
        help="Google Java Formatter version to use (default %(default)s)",
    )
    parser.add_argument(
        "--aosp",
        action="store_true",
        dest="aosp",
        help="Formats Java code into AOSP format",
    )

    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(argv)

    # Google Java Formatter 1.10+ does support Java 16+, before that version
    # the tool can only be executed on Java up to version 15.
    # Context: https://github.com/google/google-java-format/releases/tag/v1.10.0
    if Version(args.google_java_formatter_version) <= Version("1.9"):
        assert_max_jdk_version(Version("16.0"), inclusive=False)  # pragma: no cover

    google_java_formatter_jar = _download_google_java_formatter_jar(
        args.google_java_formatter_version,
    )

    cmd_args = [
        "java",
        # export JDK internal classes for Java 16+
        "--add-exports",
        "jdk.compiler/com.sun.tools.javac.api=ALL-UNNAMED",
        "--add-exports",
        "jdk.compiler/com.sun.tools.javac.file=ALL-UNNAMED",
        "--add-exports",
        "jdk.compiler/com.sun.tools.javac.parser=ALL-UNNAMED",
        "--add-exports",
        "jdk.compiler/com.sun.tools.javac.tree=ALL-UNNAMED",
        "--add-exports",
        "jdk.compiler/com.sun.tools.javac.util=ALL-UNNAMED",
        "-jar",
        google_java_formatter_jar,
        "--set-exit-if-changed",
    ]
    if args.aosp:  # pragma: no cover
        cmd_args.append("--aosp")
    if args.autofix:
        cmd_args.append("--replace")
    else:
        cmd_args.append("--dry-run")
    status, output = run_command(*(cmd_args + args.filenames))

    if output:
        print(
            "{}: {}".format(
                "The following files have been fixed by google-java-formatter"
                if args.autofix
                else "The following files are not properly formatted",  # noqa
                ", ".join(output.splitlines()),
            ),
        )

    return 0 if status == 0 else 1


if __name__ == "__main__":
    sys.exit(pretty_format_java())
