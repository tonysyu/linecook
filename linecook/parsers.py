# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import re


TYPE_PREFIX_SEPARATOR = ':'


def create_regex_factory(format_string, flags=0):
    """Return a `create_regex` function that compiles a pattern to a regex."""
    def create_regex(pattern):
        return re.compile(format_string.format(pattern), flags=flags)
    return create_regex


REGEX_FORMATTERS = {
    'exact': create_regex_factory(r'^{}$'),
    'iexact': create_regex_factory(r'^{}$', flags=re.IGNORECASE),
    'substring': create_regex_factory(r'{}'),
    'isubstring': create_regex_factory(r'{}', flags=re.IGNORECASE),
    'word': create_regex_factory(r'\b{}\b'),
    'iword': create_regex_factory(r'\b{}\b', flags=re.IGNORECASE),
}

REGEX_FORMATTERS.update({
    alias: REGEX_FORMATTERS[key] for alias, key in [
        ('x', 'exact'),
        ('xi', 'iexact'),
        ('s', 'substring'),
        ('si', 'isubstring'),
        ('w', 'word'),
        ('wi', 'iword'),
    ]
})


def resolve_match_pattern(pattern):
    if isinstance(pattern, re._pattern_type):
        return pattern

    if TYPE_PREFIX_SEPARATOR in pattern:
        formatter_code, pattern_text = pattern.split(TYPE_PREFIX_SEPARATOR, 1)
        create_regex = REGEX_FORMATTERS.get(formatter_code)
        if create_regex:
            return create_regex(pattern_text)

    return re.compile(pattern)
