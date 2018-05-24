# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from linecook.parsers import resolve_pattern


class TestResolveSearchPattern:

    def test_create_word_boundary_regex(self):
        assert resolve_pattern('w:my-word') == re.compile(r'\bmy-word\b')
