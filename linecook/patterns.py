# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def any_pattern(*args):
    """Return regex that matches any of the input regex patterns.

    The returned value is equivalent to writing::

        r'(<arg1>|<arg2>|...)'
    """
    return '({})'.format('|'.join(args))


exact_template = r'^{}$'
word_template = r'\b{}\b'
quoted_string_template = r'(?<![{0}\w]){0}[^{0}]*{0}(?![{0}\w])'


def exact_match(string):
    """Return regex that matches the input string exactly.

    The returned value is equivalent to writing::

        r'^<string>$'
    """
    return exact_template.format(string)


def bounded_word(string):
    """Return regex that matches the input string as a bounded word.

    The returned value is equivalent to writing::

        r'\b<string>\b'
    """
    return word_template.format(string)


num_float = bounded_word(r'[+-]?(\d*[.])?\d+')
num_int = bounded_word(r'\d')
number = any_pattern(num_int, num_float)

year = r'\d{4}'
month = r'\d{2}'
day = r'\d{2}'

date = bounded_word(r'{}-{}-{}'.format(year, month, day))
time = bounded_word(r'(\d{2}:\d{2}(:\d{2})?)')
time_ms = bounded_word(r'\d{2}:\d{2}:\d{2}(,|.)\d{3}')

log_level = bounded_word(any_pattern('TRACE', 'DEBUG', 'INFO', 'WARN',
                                     'ERROR', 'SEVERE', 'FATAL'))

single_quoted_strings = quoted_string_template.format("'")
double_quoted_strings = quoted_string_template.format('"')
strings = any_pattern(single_quoted_strings, double_quoted_strings)
