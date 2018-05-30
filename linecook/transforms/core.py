# -*- coding: utf-8 -*-
"""
Text formatters match the signature of basic regex functions, taking a
text/regex match pattern and an input string.
"""
from __future__ import unicode_literals

import functools
import os

from termcolor import colored
from toolz import itertoolz
from toolz.functoolz import identity

from .utils import match_pattern_transform


@match_pattern_transform
def filter_line(string, match_pattern,
                on_match=None,
                on_mismatch=None):
    """Return line filtered by match pattern.

    If neither `on_match` or `on_mismatch` are given, return input
    string if it matches the given pattern. Otherwise, the input string is
    passed to those callback functions and the output is returned.

    Args:
        on_match (callable): A text transform that is called with the input
            `string` if the string matches the `match_pattern`.
        on_mismatch (callable): A text transform that is called with the input
            `string` if the string does not matche the `match_pattern`.
    """
    match = match_pattern.search(string)

    if not (on_match or on_mismatch):
        return None if match else string

    if match and on_match:
        return on_match(string)
    elif not match and on_mismatch:
        return on_mismatch(string)


@match_pattern_transform
def partition(string, match_pattern,
              on_match=None,
              on_mismatch=None):
    """Return line partitioned by pattern and re-joined after transformation.

    Args:
        on_match (callable): A text transform that is called with each
            matched substring.
        on_match (callable): A text transform that is called with each
            unmatched substring.
    """
    on_match = on_match or identity
    on_mismatch = on_mismatch or identity

    matched_output = (on_match(x)
                      for x in match_pattern.findall(string))
    # With capture groups, `re.split` returns matches, so those filter out.
    unmatched_output = (on_mismatch(x)
                        for x in match_pattern.split(string)
                        if not match_pattern.match(x))
    # Split will return an empty string at the beginning if pattern is found
    # at the beginning of the input string.
    substrings = itertoolz.interleave([unmatched_output, matched_output])
    return ''.join(substrings)


@match_pattern_transform
def replace_text(string, match_pattern, replacement):
    return match_pattern.sub(replacement, string)


def create_color_replacement(*color_args):
    """Return color function used as argument to `re.sub`.

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


class CountLines(object):
    """Tranformation returning line of text with line count added."""

    def __init__(self, line_template='{count_label} {line}',
                 count_template='{count:>3}:', color_args=('grey',)):
        self.count = 0
        self.line_template = line_template
        self.count_template = count_template
        self.color_args = color_args

    def __call__(self, line):
        self.count += 1
        count_label = self.count_template.format(count=self.count)
        count_label = colored(count_label, *self.color_args, attrs=['bold'])
        return self.line_template.format(count_label=count_label, line=line)

    def reset(self):
        self.count = 0


delete_text = functools.partial(replace_text, replacement='')
split_on = functools.partial(replace_text, replacement=os.linesep)
