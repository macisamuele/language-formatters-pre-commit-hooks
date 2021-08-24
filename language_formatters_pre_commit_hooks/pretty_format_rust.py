# -*- coding: utf-8 -*-
import argparse
import sys
import typing
from os import getenv

from language_formatters_pre_commit_hooks.pre_conditions import rust_required
from language_formatters_pre_commit_hooks.utils import run_command


@rust_required
def pretty_format_rust(argv: typing.Optional[typing.List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--autofix",
        action="store_true",
        dest="autofix",
        help="Automatically fixes encountered not-pretty-formatted files",
    )

    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(argv)

    rust_toolchain_version = getenv("RUST_TOOLCHAIN", "stable")
    # Check
    status_code, output = run_command("cargo", "+{}".format(rust_toolchain_version), "fmt", "--", "--check", *args.filenames)
    not_well_formatted_files = sorted(line.split()[2] for line in output.splitlines() if line.startswith("Diff in "))
    if not_well_formatted_files:
        print(
            "{}: {}".format(
                "The following files have been fixed by cargo format" if args.autofix else "The following files are not properly formatted",
                ", ".join(not_well_formatted_files),
            ),
        )
        if args.autofix:
            run_command("cargo", "+{}".format(rust_toolchain_version), "fmt", "--", *not_well_formatted_files)
    elif status_code != 0:
        print("Detected not valid rust source files among {}".format("\n".join(sorted(args.filenames))))

    return 1 if status_code != 0 or not_well_formatted_files else 0


if __name__ == "__main__":
    sys.exit(pretty_format_rust())
