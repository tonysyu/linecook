# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from contextlib import contextmanager

import mock

from linecook.transforms import core
from linecook.testing import IdentityMock


class TestDeleteText:

    def test_delete_literal_string(self):
        assert core.delete_text('delete me')('Hi; delete me bye') == 'Hi;  bye'

    def test_delete_regex(self):
        assert core.delete_text(r'\bban\b')('ban banish') == ' banish'

    def test_delete_regex_with_word_prefix(self):
        assert core.delete_text(r'w:ban')('ban banish') == ' banish'

    def test_not_deleted(self):
        assert core.delete_text(r'\bban\b')('banish') == 'banish'


class TestFilterLine:

    def test_remove_line(self):
        assert core.filter_line(r'\bremove\b')('remove this line') is None

    def test_line_not_removed(self):
        assert core.filter_line(r'\bremove\b')('not removed') == 'not removed'

    def test_call_on_match(self):
        on_match = mock.Mock()
        on_mismatch = mock.Mock()
        transform = core.filter_line(r'match', on_match=on_match,
                                     on_mismatch=on_mismatch)

        transform('match this line')
        on_match.assert_called_once_with('match this line')
        on_mismatch.assert_not_called()

    def test_call_on_mismatch(self):
        on_match = mock.Mock()
        on_mismatch = mock.Mock()
        transform = core.filter_line(r'mismatch', on_match=on_match,
                                     on_mismatch=on_mismatch)

        transform('line that does not match')
        on_match.assert_not_called()
        on_mismatch.assert_called_once_with('line that does not match')


class TestSplitOn:

    def test_spilt_on(self):
        assert core.split_on('&')('a=1&b=2') == 'a=1{}b=2'.format(os.linesep)


class TestPartition:

    def test_partition(self):
        word = self.create_partition_function('[A-z]+')
        word('1 match 2')

        self.on_match.assert_called_once_with('match')
        assert self.on_mismatch.calls == ['1 ', ' 2']

    def test_partition_with_capture_group(self):
        word = self.create_partition_function('([A-z]+)')
        word('1 match 2')

        self.on_match.assert_called_once_with('match')
        assert self.on_mismatch.calls == ['1 ', ' 2']

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
        self.on_match = IdentityMock(template=success_template)
        self.on_mismatch = IdentityMock(template=failure_template)
        return core.partition(match_pattern,
                              on_match=self.on_match,
                              on_mismatch=self.on_mismatch)


class TestColorText:

    def test_color_text(self):
        color_red = core.color_text('match words', 'red')
        assert (color_red('match words in this line') ==
                ascii_red_text('match words') + ' in this line')


class TestCountLines:

    def setup(self):
        self.counter = core.CountLines(count_template='{count}:')

    def test_count(self):
        with mock_colored():
            assert self.counter('first') == '1: first'
            assert self.counter('second') == '2: second'

    def test_reset(self):
        with mock_colored():
            assert self.counter('first') == '1: first'
            self.counter.reset()
            assert self.counter('second') == '1: second'


def ascii_esc(value):
    return '\x1b[{}'.format(value)


def ascii_red_text(text):
    return '{red}{text}{reset}'.format(
        red=ascii_esc('31m'),
        text=text,
        reset=ascii_esc('0m'),
    )


@contextmanager
def mock_colored(module=core):
    with mock.patch.object(module, 'colored') as fake_colored:
        fake_colored.side_effect = colored_text_identity
        yield fake_colored


def colored_text_identity(text, color=None, on_color=None, attrs=None):
    return text
