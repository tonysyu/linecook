# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from linecook.transforms import parse


class TestJsonFromQS:

    def test_single_values(self):
        assert parse.json_from_qs()("a=1&b=2") == '{"a": "1", "b": "2"}'

    def test_single_values_no_flattening(self):
        parse_without_flattten = parse.json_from_qs(flatten=False)
        assert parse_without_flattten("a=1&b=2") == '{"a": ["1"], "b": ["2"]}'

    def test_values_list(self):
        assert parse.json_from_qs()("a=1&a=2") == '{"a": ["1", "2"]}'
