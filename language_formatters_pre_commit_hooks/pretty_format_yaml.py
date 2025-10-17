# -*- coding: utf-8 -*-
import argparse
import io
import re
import sys
import typing
from sys import maxsize

from ruamel.yaml import YAML


def _process_single_document(document: str, yaml: YAML) -> str:
    """Pretty format one YAML document.

    This is needed in order to prevent `ruamel.yaml` to interfere with documents that have primitive types on the document root.
    For more context check https://github.com/macisamuele/language-formatters-pre-commit-hooks/pull/1

    Args:
        document (str): Original document content.
        yaml: YAML library instance.
    Returns:
        Pretty-formatted content (str).
    """
    content = yaml.load(document)
    if isinstance(content, (list, dict)):
        pretty_output = io.StringIO()
        yaml.dump(content, pretty_output)
        return pretty_output.getvalue()
    else:
        # do not disturb primitive content (unstructured text)
        return str(document)


def pretty_format_yaml(argv: typing.Optional[typing.List[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--autofix",
        action="store_true",
        dest="autofix",
        help="Automatically fixes encountered not-pretty-formatted files",
    )
    parser.add_argument(
        "--indent",
        type=int,
        default="2",
        help="The number of spaces to be used as delimiter for indentation level (Default: %(default)s)",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default="0",
        help="The number of spaces to be used as offset for nested structures (Default: %(default)s)",
    )
    parser.add_argument(
        "--preserve-quotes",
        action="store_true",
        dest="preserve_quotes",
        help="Keep existing string quoting",
    )
    parser.add_argument(
        "--line-width",
        type=int,
        default=maxsize,
        dest="line_width",
        help=(
            "Max line length on the generated file. NOTE: As far as we attempt to"
            " enforce the limit we cannot guarantee that it is always possible"
        ),
    )
    parser.add_argument(
        "--explicit-start",
        action="store_true",
        dest="explicit_start",
        help="Enforce a document-start marker (---)",
    )

    parser.add_argument("filenames", nargs="*", help="Filenames to fix")
    args = parser.parse_args(argv)

    status = 0

    if args.indent < 0:  # pragma: no cover
        print("indent argument ({}) cannot be negative. Defaulting it to 2".format(args.indent), file=sys.stderr)
        args.indent = 2
    if args.offset < 0:  # pragma: no cover
        print("offset argument ({}) cannot be negative. Defaulting it to 0".format(args.offset), file=sys.stderr)
        args.offset = 0

    yaml = YAML()
    yaml.indent(mapping=args.indent, sequence=args.indent + args.offset, offset=args.offset)
    yaml.preserve_quotes = args.preserve_quotes
    yaml.explicit_start = args.explicit_start
    # Prevent ruamel.yaml to wrap yaml lines
    yaml.width = args.line_width  # type: ignore  # mypy recognise yaml.width as None

    separator = "---\n"

    for yaml_file in set(args.filenames):
        with open(yaml_file, encoding="utf8") as input_file:
            string_content = "".join(input_file.readlines())

        # Split multi-document file into individual documents
        #
        # Not using yaml.load_all() because it reformats primitive (non-YAML) content. It removes
        # newline characters.
        separator_pattern = r"^---\s*\n"
        original_docs = re.split(separator_pattern, string_content, flags=re.MULTILINE)

        # A valid multi-document YAML file might starts with the separator.
        # In this case the first document of original docs will be empty and should not be considered
        if string_content.startswith("---"):
            original_docs = original_docs[1:]

        # if file is a multi-doc, explicit_start must be turned off since separators will be added below
        if len(original_docs) > 1:
            yaml.explicit_start = False

        pretty_docs = []

        try:
            for doc in original_docs:
                content = _process_single_document(doc, yaml)
                if content is not None:
                    pretty_docs.append(content)

            # Start multi-doc file with separator
            pretty_content = "" if len(pretty_docs) == 1 else separator
            pretty_content += separator.join(pretty_docs)

            if string_content != pretty_content:
                print("File {} is not pretty-formatted".format(yaml_file))

                if args.autofix:
                    print("Fixing file {}".format(yaml_file))
                    with io.open(yaml_file, "w", encoding="UTF-8") as output_file:
                        output_file.write(str(pretty_content))

                status = 1
        except BaseException as e:  # pragma: no cover
            print(
                "Input File {} is not a valid YAML file, consider using check-yaml: {}".format(yaml_file, e),
            )
            return 1

    return status


if __name__ == "__main__":
    sys.exit(pretty_format_yaml())
