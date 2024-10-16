# -*- coding: utf-8 -*-
import argparse
import os.path
import sys
import typing

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
    parser.add_argument(
        "--manifest-root",
        action="append",
        dest="manifest_root",
        help="The cargo manifest file location.",
    )
    parser.add_argument(
        '--format-verbose',
        action="store_true",
        dest='print_command_exec',
        help="Output tool execution messages",
    )

    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(argv)

    if not args.manifest_root:
        pretty_format_rust_internal(args.autofix, None, args.filenames, print_command_exec=args.print_command_exec)

    for manifest_root in args.manifest_root:
        manifest_path = os.path.join(manifest_root, 'Cargo.toml')

        # TODO: properly filter filenames
        filenames = list(filter(lambda filename: filename.startswith(manifest_root), args.filenames))
        pretty_format_rust_internal(args.autofix, manifest_path, filenames,
                                    print_command_exec=args.print_command_exec)

def pretty_format_rust_internal(autofix: bool, manifest_path: str|None, filenames:
                                list[str], *,  print_command_exec: bool):
    # Check
    if autofix:
        check_args = []
    else:
        check_args = ['--check']

    if manifest_path:
        manifest_path_args = ["--manifest-path", manifest_path]
    else:
        manifest_path_args = []

    status_code, output, _ = run_command(
        "cargo", "fmt", *manifest_path_args,  *check_args, "--", *filenames,
        print_if_ok=False, print_command_exec=print_command_exec
    )
    not_well_formatted_files = sorted(line.split()[2] for line in output.splitlines() if line.startswith("Diff in "))
    if not_well_formatted_files:
        print(
            "{}: {}".format(
                "The following files have been fixed by rustfmt" if autofix else "The following files are not properly formatted",
                ", ".join(not_well_formatted_files),
            ),
        )
    elif status_code != 0:
        print("Detected not valid rust source files among {}".format("\n".join(sorted(filenames))))

    return 1 if status_code != 0 or not_well_formatted_files else 0


if __name__ == "__main__":
    sys.exit(pretty_format_rust())
