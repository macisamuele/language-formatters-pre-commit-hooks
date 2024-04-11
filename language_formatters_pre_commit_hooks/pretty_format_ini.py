import argparse
import sys
import typing

from config_formatter import ConfigFormatter


def pretty_format_ini(argv: typing.Optional[typing.List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--autofix",
        action="store_true",
        dest="autofix",
        help="Automatically fixes encountered not-pretty-formatted files",
    )

    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(argv)

    status = 0

    for ini_file in set(args.filenames):
        with open(ini_file, encoding="utf8") as input_file:
            string_content = input_file.read()

        try:
            formatter = ConfigFormatter()

            pretty_content_str = formatter.prettify(string_content)

            if string_content != pretty_content_str:
                print(f"File {ini_file} is not pretty-formatted")

                if args.autofix:
                    print(f"Fixing file {ini_file}")
                    with open(ini_file, "w", encoding="UTF-8") as output_file:
                        output_file.write(pretty_content_str)

                status = 1
        except BaseException as e:
            print(f"Input File {ini_file} is not a valid INI file: {e}")
            return 1

    return status


if __name__ == "__main__":
    sys.exit(pretty_format_ini())
