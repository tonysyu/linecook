# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from linecook.parsers import resolve_match_pattern


class TestResolveSearchPattern:

    def test_create_word_boundary_regex(self):
        assert resolve_match_pattern('w:my-word') == re.compile(r'\bmy-word\b')

    def test_create_exact_regex(self):
        assert resolve_match_pattern('x:hello') == re.compile(r'^hello$')
