# -*- coding: utf-8 -*-
"""
Text formatters match the signature of basic regex functions, taking a
text/regex match pattern and an input string.
"""
from __future__ import unicode_literals

import functools
import os

from termcolor import colored

from .parsers import resolve_match_pattern


def match_pattern_transform(func):
    """Decorator transforming a text transform into factory function.

    This should be used to decorate functions that expect a string to transform
    as the first argument and a match pattern as a second argument (see
    `linecook.parsers.resolve_match_pattern` for details on match patterns).
    The decorated function will be a factory function where the output is
    a function that operates solely on text.

    This is used for functions that you want to initialize with a match pattern
    (and possibility other configuration) and use multiple times on text.

    Examples:

    >>> @match_pattern_transform
    ... def replace_text(string, match_pattern, replacement):
    ...     return match_pattern.sub(replacement, string)
    ...
    >>> verbose_thanks = replace_text('Thx', 'Thanks')
    >>> verbose_thanks('Thx for the memories')
    'Thanks for the memories'
    >>> verbose_thanks("You're the best! Thx!")
    "You're the best! Thanks!"

    Note that the match pattern was defined as the second argument, but the
    resulting function is called with the pattern as the first argument. This

    """
    @functools.wraps(func)
    def wrapped(match_pattern, *args, **kwargs):
        match_pattern = resolve_match_pattern(match_pattern)

        def transform(string):
            return func(string, match_pattern, *args, **kwargs)
        return transform

    return wrapped


@match_pattern_transform
def filter_line(string, match_pattern):
    match = match_pattern.search(string)
    return None if match else string


@match_pattern_transform
def replace_text(string, match_pattern, replacement):
    return match_pattern.sub(replacement, string)


def create_color_replacement(*color_args):
    """Return colore replacement function used as argument to `re.sub`.

    `re.sub` accepts a function for string replacement, where the match object
    is passed in as the only argument.

    Args:
        *color_args (list(str)): Color arguments matching those expected by
            `termcolor.colored`.
    """
    def color_replacement(match_string):
        if hasattr(match_string, 'group'):
            match_string = match_string.group()
        return colored(match_string, *color_args)
    return color_replacement


def color_text(match_pattern, *color_args):
    color_replacement = create_color_replacement(*color_args)
    return replace_text(match_pattern, replacement=color_replacement)


delete_text = functools.partial(replace_text, replacement='')
split_on = functools.partial(replace_text, replacement=os.linesep)
