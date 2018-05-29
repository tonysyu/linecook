# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

import linecook.transforms as tf
from linecook.testing import IdentityMock


class TestDeleteText:

    def test_delete_literal_string(self):
        assert tf.delete_text('delete me')('Hi; delete me bye') == 'Hi;  bye'

    def test_delete_regex(self):
        assert tf.delete_text(r'\bban\b')('ban banish') == ' banish'

    def test_delete_regex_with_word_prefix(self):
        assert tf.delete_text(r'w:ban')('ban banish') == ' banish'

    def test_not_deleted(self):
        assert tf.delete_text(r'\bban\b')('banish') == 'banish'


class TestFilterLine:

    def test_filter_line(self):
        assert tf.filter_line(r'\bremove\b')('remove this line') is None


class TestSplitOn:

    def test_spilt_on(self):
        assert tf.split_on('&')('a=1&b=2') == 'a=1{}b=2'.format(os.linesep)


class TestPartition:

    def test_partition(self):
        word = self.create_partition_function('[A-z]+')
        word('1 match 2')

        self.on_match_success.assert_called_once_with('match')
        assert self.on_match_failure.calls == ['1 ', ' 2']

    def test_partition_with_capture_group(self):
        word = self.create_partition_function('([A-z]+)')
        word('1 match 2')

        self.on_match_success.assert_called_once_with('match')
        assert self.on_match_failure.calls == ['1 ', ' 2']

    def test_partition_output(self):
        word = self.create_partition_function(
            '([A-z]+)',
            success_template='success({})',
            failure_template='failure({})',
        )
        assert word('1 match 2') == 'failure(1 )success(match)failure( 2)'

    def create_partition_function(self, match_pattern,
                                  success_template='{}',
                                  failure_template='{}'):
        self.on_match_success = IdentityMock(template=success_template)
        self.on_match_failure = IdentityMock(template=failure_template)
        return tf.partition(match_pattern,
                            on_match_success=self.on_match_success,
                            on_match_failure=self.on_match_failure)
