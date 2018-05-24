# -*- coding: utf-8 -*-
from __future__ import unicode_literals


date = r'\b(\d{4}-\d{2}-\d{2})\b'
time = r'\b(\d{2}:\d{2}(:\d{2})?)\b'

log_level = r'\b(TRACE|DEBUG|INFO|WARN|ERROR|SEVERE|FATAL)\b'

quoted_string_template = r'(?<![{0}\w]){0}[^{0}]*{0}(?![{0}\w])'
single_quoted_strings = quoted_string_template.format("'")
double_quoted_strings = quoted_string_template.format('"')
strings = '({}|{})'.format(single_quoted_strings, double_quoted_strings)
