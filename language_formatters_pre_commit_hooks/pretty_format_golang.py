# -*- coding: utf-8 -*-
import argparse
import sys
import typing

from language_formatters_pre_commit_hooks.pre_conditions import golang_required
from language_formatters_pre_commit_hooks.utils import run_command


def _get_eol_attribute() -> typing.Optional[str]:
    """
    Retrieve eol attribute defined for golang files
    The method will return None in case of any error interacting with git
    """
    status_code, output = run_command("git", "check-attr", "-z", "eol", "--", "filename.go")
    if status_code != 0:
        return None

    try:
        # Expected output: "filename.go\0eol\0lf\0"
        _, _, eol, _ = output.split("\0")
        return eol
    except:  # noqa: E722 (allow usage of bare 'except')
        print(
            "`git check-attr` output is not consistent to `<filename>\0<key>\0<value>\0` format: {output}".format(
                output=output,
            ),
            file=sys.stderr,
        )
        return None


@golang_required
def pretty_format_golang(argv: typing.Optional[typing.List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--autofix",
        action="store_true",
        dest="autofix",
        help="Automatically fixes encountered not-pretty-formatted files",
    )

    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(argv)

    cmd_args = ["gofmt", "-l"]
    if args.autofix:
        cmd_args.append("-w")
    status, output = run_command(*(cmd_args + args.filenames))

    if status != 0:  # pragma: no cover
        print(output)
        return 1

    status = 0
    if output:
        status = 1
        print(
            "{}: {}".format(
                "The following files have been fixed by gofmt" if args.autofix else "The following files are not properly formatted",
                ", ".join(output.splitlines()),
            ),
        )
        if sys.platform == "win32":  # pragma: no cover
            eol_attribute = _get_eol_attribute()
            if eol_attribute and eol_attribute != "lf":
                print(
                    "Hint: gofmt uses LF (aka `\\n`) as new line, but on Windows the default new line is CRLF (aka `\\r\\n`). "
                    "You might want to ensure that go files are forced to use LF via `.gitattributes`. "
                    "Example: https://github.com/macisamuele/language-formatters-pre-commit-hooks/commit/53f27fda02ead5b1b9b6a9bbd9c36bb66d229887",  # noqa: E501
                    file=sys.stderr,
                )

    return status


if __name__ == "__main__":
    sys.exit(pretty_format_golang())
