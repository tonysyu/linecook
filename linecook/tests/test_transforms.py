# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from linecook.transforms import delete_text, filter_line, split_on


class TestDeleteText:

    def test_delete_literal_string(self):
        assert delete_text('delete me')('Hi; delete me bye') == 'Hi;  bye'

    def test_delete_regex(self):
        assert delete_text(r'\bban\b')('ban banish') == ' banish'

    def test_not_deleted(self):
        assert delete_text(r'\bban\b')('banish') == 'banish'


class TestFilterLine:

    def test_filter_line(self):
        assert filter_line(r'\bremove\b')('remove this line') is None


class TestSplitOn:

    def test_spilt_on(self):
        assert split_on('&')('a=1&b=2') == 'a=1{}b=2'.format(os.linesep)
