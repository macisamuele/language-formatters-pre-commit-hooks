import argparse
import json
import sys
import typing

from language_formatters_pre_commit_hooks import _get_default_version
from language_formatters_pre_commit_hooks.pre_conditions import java_required
from language_formatters_pre_commit_hooks.utils import download_url
from language_formatters_pre_commit_hooks.utils import run_command


def _download_ktlint_formatter_jar(version: str) -> str:  # pragma: no cover
    def get_url(_version: str) -> str:
        # Links extracted from https://github.com/pinterest/ktlint/
        return "https://github.com/pinterest/ktlint/releases/download/{version}/ktlint".format(
            version=_version,
        )

    url_to_download = get_url(version)
    try:
        return download_url(get_url(version), f"ktlint{version}.jar")
    except:  # noqa: E722 (allow usage of bare 'except')
        raise RuntimeError(
            "Failed to download {url}. Probably the requested version, {version}, is "
            "not valid or you have some network issue.".format(
                url=url_to_download,
                version=version,
            ),
        )


def _download_ktfmt_formatter_jar(version: str) -> str:  # pragma: no cover
    url = "https://repo1.maven.org/maven2/com/facebook/ktfmt/{version}/ktfmt-{version}-jar-with-dependencies.jar".format(
        version=version,
    )
    try:
        return download_url(url)
    except:  # noqa: E722 (allow usage of bare 'except')
        raise RuntimeError(
            f"Failed to download {url}. Probably the requested version, {version}" ", is not valid or you have some network issue."
        )


def _fix_paths(paths: typing.Iterable[str]) -> typing.Iterable[str]:
    # Starting from KTLint 0.41.0 paths cannot contain backward slashes as path separator
    # Odd enough the error messages reported by KTLint contain `\` :(
    for path in paths:
        yield path.replace("\\", "/")


@java_required
def pretty_format_kotlin(argv: typing.Optional[typing.List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--autofix",
        action="store_true",
        dest="autofix",
        help="Automatically fixes encountered not-pretty-formatted files",
    )
    parser.add_argument(
        "--ktlint-version",
        dest="ktlint_version",
        default=_get_default_version("ktlint"),
        help="KTLint version to use (default %(default)s)",
    )
    parser.add_argument(
        "--ktlint-jar",
        dest="ktlint_jar",
        default=None,
        help="KTLint jar to use (instead of downloading)",
    )
    parser.add_argument(
        "--ktfmt-version",
        dest="kftmt_version",
        default=_get_default_version("ktfmt"),
        help="ktfmt version to use (default %(default)s)",
    )
    parser.add_argument(
        "--ktfmt-jar",
        dest="ktfmt_jar",
        default=None,
        help="ktfmt jar to use (instead of downloading)",
    )
    parser.add_argument(
        "--ktfmt",
        action="store_true",
        dest="ktfmt",
        help="Use ktfmt",
    )
    parser.add_argument(
        "--ktfmt-style",
        choices=["dropbox", "google", "kotlinlang"],
        dest="ktfmt_style",
        help="Which style to use",
    )
    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(argv)
    if args.ktfmt:
        jar = args.ktfmt_jar or _download_ktfmt_formatter_jar(args.kftmt_version)
        return run_ktfmt(jar, args.filenames, args.ktfmt_style, args.autofix)
    else:
        jar = args.ktlint_jar or _download_ktlint_formatter_jar(args.ktlint_version)
        return run_ktlint(jar, args.filenames, args.autofix)


def run_ktfmt(jar: str, filenames: typing.Iterable[str], ktfmt_style: typing.Optional[str], autofix: bool) -> int:
    ktfmt_args = ["--set-exit-if-changed"]
    if ktfmt_style is not None:
        ktfmt_args.append(f"--{ktfmt_style}-style")
    if not autofix:
        ktfmt_args.append("--dry-run")
    return_code, _, _ = run_command(
        "java",
        "-jar",
        jar,
        "ktfmt",
        *ktfmt_args,
        *filenames,
    )
    return return_code


def run_ktlint(jar: str, filenames: typing.Iterable[str], autofix: bool):
    jvm_args = ["--add-opens", "java.base/java.lang=ALL-UNNAMED"]

    # ktlint does not return exit-code!=0 if we're formatting them.
    # To workaround this limitation we do run ktlint in check mode only,
    # which provides the expected exit status and we run it again in format
    # mode if autofix flag is enabled
    #
    # Logging must be suppressed here as it goes to stdout. This would
    # interfere with parsing the output JSON.
    return_code, stdout, _ = run_command(
        "java",
        *jvm_args,
        "-jar",
        jar,
        "--log-level",
        "none",
        "--reporter=json",
        "--relative",
        "--",
        *_fix_paths(filenames),
    )

    not_pretty_formatted_files: typing.Set[str] = set()
    if return_code != 0:
        not_pretty_formatted_files.update(item["file"] for item in json.loads(stdout))

        if autofix:
            print(f"Running ktlint format on {not_pretty_formatted_files}")
            run_command(
                "java",
                *jvm_args,
                "-jar",
                jar,
                "--log-level",
                "none",
                "--relative",
                "--format",
                "--",
                *_fix_paths(not_pretty_formatted_files),
            )

    status = 0
    if not_pretty_formatted_files:
        status = 1
        print(
            "{}: {}".format(
                "The following files have been fixed by ktlint" if autofix else "The following files are not properly formatted",
                ", ".join(sorted(not_pretty_formatted_files)),
            ),
        )

    return status


if __name__ == "__main__":
    sys.exit(pretty_format_kotlin())
