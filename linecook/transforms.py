# -*- coding: utf-8 -*-
"""
Text formatters match the signature of basic regex functions, taking a
text/regex pattern and an input string.
"""
from __future__ import unicode_literals

import functools
import os
import re
import shlex

from termcolor import colored


def text_tranform(func):
    @functools.wraps(func)
    def wrapped(pattern, *args, **kwargs):
        def transform(string):
            return func(string, pattern, *args, **kwargs)
        return transform
    return wrapped


@text_tranform
def filter_line(string, pattern):
    pattern = re.compile(pattern)
    match = pattern.search(string)
    return None if match else string


@text_tranform
def replace_text(string, pattern, replacement):
    pattern = re.compile(pattern)
    return pattern.sub(replacement, string)


def create_color_replacement(*color_args):
    def color_replacement(match_string):
        if hasattr(match_string, 'group'):
            match_string = match_string.group()
        return colored(match_string, *color_args)
    return color_replacement


def color_text(pattern, *color_args):
    color_replacement = create_color_replacement(*color_args)
    return replace_text(pattern, replacement=color_replacement)


delete_text = functools.partial(replace_text, replacement='')
split_on = functools.partial(replace_text, replacement=os.linesep)
