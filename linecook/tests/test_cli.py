# -*- coding: utf-8 -*-
"""
.. default-role:: literal

"""

from __future__ import unicode_literals

import sys
from contextlib import contextmanager
from io import StringIO

import mock

from linecook import cli


class TestBuildParser:

    def test_no_inputs(self):
        args = create_linecook_args([])
        assert args.recipe == 'default'
        assert args.text is None
        assert args.text_stream == sys.stdin

    def test_custom_recipe(self):
        args = create_linecook_args(['python'])
        assert args.recipe is 'python'

    def test_custom_text(self):
        args = create_linecook_args(['-t', 'Hello world'])
        assert args.text is 'Hello world'


class TestRun:

    def test_custom_text(self):
        input_text = 'Hello world'
        args = create_linecook_args(['identity', '-t', input_text])

        with mock_print() as fake_print:
            cli.run(args)

        fake_print.assert_called_once_with(input_text)

    def test_stdin(self):
        input_text = u'Hello world'

        with mock.patch.object(cli, 'sys') as fake_sys:
            fake_sys.stdin = StringIO(input_text)
            args = create_linecook_args(['identity'])

            with mock_print() as fake_print:
                cli.run(args)

        fake_print.assert_called_once_with(input_text, end='')

    def test_list_recipes(self):
        with mock.patch.object(cli.config, 'load_config') as fake_load_config:
            fake_load_config.return_value = cli.config.LineCookConfig([{
                'recipes': {'my-recipe': []}
            }])

            args = create_linecook_args(['--list-recipes'])
            with mock_print() as fake_print:
                cli.run(args)

        fake_print.assert_has_calls([
            mock.call('Available recipes:'),
            mock.call('- my-recipe'),
        ])


class TestMain:

    def test_main(self):
        args = create_linecook_args()

        with mock.patch.object(cli, 'run') as fake_run:
            cli.main()

        fake_run.assert_called_once_with(args)


@contextmanager
def mock_print(module=cli):
    with mock.patch.object(module, 'print') as fake_print:
        yield fake_print


def create_linecook_args(arg_list=()):
    parser = cli.build_parser()
    return parser.parse_args(arg_list)
