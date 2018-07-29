# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
from contextlib import contextmanager


@contextmanager
def change_dir_context(directory):
    working_directory = os.getcwd()
    try:
        os.chdir(directory)
        yield
    finally:
        os.chdir(working_directory)


@contextmanager
def undecorate_function(func):
    passed_function = func
    func = passed_function.__wrapped__
    yield func
    func = passed_function
