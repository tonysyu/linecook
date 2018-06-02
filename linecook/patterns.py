# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def _create_format_factory(template):
    def format_function(*args, **kwargs):
        return template.format(*args, **kwargs)
    return format_function


def any_pattern(*args):
    return '({})'.format('|'.join(args))


exact_template = r'^{}$'
word_template = r'\b{}\b'
quoted_string_template = r'(?<![{0}\w]){0}[^{0}]*{0}(?![{0}\w])'

exact_match = _create_format_factory(exact_template)
bounded_word = _create_format_factory(word_template)

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
