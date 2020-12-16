# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import io
import itertools
import sys
import typing

import six
import tomlkit
from tomlkit.api import aot
from tomlkit.api import item
from tomlkit.api import ws
from tomlkit.container import Container
from tomlkit.exceptions import ParseError
from tomlkit.items import AoT
from tomlkit.items import Comment
from tomlkit.items import Item
from tomlkit.items import Table
from tomlkit.items import Trivia
from tomlkit.items import Whitespace
from tomlkit.toml_document import TOMLDocument

from language_formatters_pre_commit_hooks.utils import (
    remove_trailing_whitespaces_and_set_new_line_ending,
)


def write_header_comment(from_doc, to_doc):
    # type: (TOMLDocument, TOMLDocument) -> None
    for _, value in from_doc.body:
        if isinstance(value, Comment):  # pragma: no cover
            value.trivia.indent = ""
            to_doc.add(Comment(value.trivia))
        else:
            to_doc.add(ws("\n"))
        if not isinstance(value, Whitespace):
            return


def fix_buggy_mlkit_types(in_value, parent):
    # type: (object, Item) -> Item
    if isinstance(in_value, Item):
        return in_value
    elif isinstance(in_value, Container):  # pragma: no cover
        return Table(in_value, trivia=Trivia(), is_aot_element=False)
    else:  # pragma: no cover
        return item(in_value, parent)


class TomlSort:
    def __init__(self, input_str, only_sort_tables=False, header=True):
        # type: (six.text_type, bool, bool) -> None
        self.input_str = input_str
        self.only_sort_tables = only_sort_tables
        self.header = header

    def sorted_children_table(self, parent):
        # type: (Table) -> typing.Iterable[typing.Tuple[six.text_type, item]]
        table_items = [(key, fix_buggy_mlkit_types(parent[key], parent)) for key in parent.keys()]
        tables = ((key, value) for key, value in table_items if isinstance(value, (Table, AoT)))
        non_tables = ((key, value) for key, value in table_items if not isinstance(value, (Table, AoT)))
        non_tables_final = sorted(non_tables, key=lambda x: x[0]) if not self.only_sort_tables else non_tables
        return itertools.chain(non_tables_final, sorted(tables, key=lambda x: x[0]))

    def toml_elements_sorted(self, original):
        # type: (Item) -> Item
        if isinstance(original, Table):
            original.trivia.indent = "\n"
            new_table = Table(
                Container(),
                trivia=original.trivia,
                is_aot_element=original.is_aot_element(),
                is_super_table=original.is_super_table(),
            )
            for key, value in self.sorted_children_table(original):
                new_table[key] = self.toml_elements_sorted(value)
            return new_table
        if isinstance(original, AoT):
            new_aot = aot()
            for aot_item in original:
                new_aot.append(self.toml_elements_sorted(aot_item))
            return new_aot
        if isinstance(original, Item):
            original.trivia.indent = ""
            return original
        raise TypeError("Invalid TOML; " + str(type(original)) + " is not an Item.")  # pragma: no cover

    def toml_doc_sorted(self, original):
        # type: (TOMLDocument) -> TOMLDocument
        """Sort a TOMLDocument"""
        sorted_document = tomlkit.document()
        if self.header:
            write_header_comment(original, sorted_document)
        for key, value in self.sorted_children_table(original):
            sorted_document[key] = self.toml_elements_sorted(value)
        return sorted_document

    def sorted(self):
        # type: () -> six.text_type
        clean_str = remove_trailing_whitespaces_and_set_new_line_ending(self.input_str.strip())
        toml_doc = tomlkit.parse(clean_str)
        sorted_toml = self.toml_doc_sorted(toml_doc)
        return six.text_type(tomlkit.dumps(sorted_toml)).strip() + "\n"


def pretty_format_toml(argv=None):
    # type: (typing.Optional[typing.List[typing.Text]]) -> int
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

    for toml_file in set(args.filenames):
        with open(toml_file) as input_file:
            string_content = "".join(input_file.readlines())

        try:
            prettified_content = TomlSort(string_content, only_sort_tables=True).sorted()
            prettified_content = remove_trailing_whitespaces_and_set_new_line_ending(prettified_content)
            if string_content != prettified_content:
                print("File {} is not pretty-formatted".format(toml_file))

                if args.autofix:
                    print("Fixing file {}".format(toml_file))
                    with io.open(toml_file, "w", encoding="UTF-8") as output_file:
                        output_file.write(prettified_content)

                status = 1
        except ParseError:
            print("Input File {} is not a valid TOML file".format(toml_file))
            return 1

    return status


if __name__ == "__main__":
    sys.exit(pretty_format_toml())
