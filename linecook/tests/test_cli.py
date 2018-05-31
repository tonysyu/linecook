import sys
from contextlib import contextmanager
from io import StringIO

import mock

from linecook import cli


class TestBuildParser:

    def setup(self):
        self.parser = cli.build_parser()

    def test_no_inputs(self):
        args = self.parser.parse_args([])
        assert args.recipe == 'default'
        assert args.text is None
        assert args.text_stream == sys.stdin

    def test_custom_recipe(self):
        args = self.parser.parse_args(['python'])
        assert args.recipe is 'python'

    def test_custom_text(self):
        args = self.parser.parse_args(['-t', 'Hello world'])
        assert args.text is 'Hello world'


class TestRun:

    def test_custom_text(self):
        input_text = 'Hello world'
        parser = cli.build_parser()
        args = parser.parse_args(['identity', '-t', input_text])

        with mock_print() as fake_print:
            cli.run(args)

        fake_print.assert_called_once_with(input_text)

    def test_stdin(self):
        input_text = 'Hello world'

        with mock.patch.object(cli, 'sys') as fake_sys:
            fake_sys.stdin = StringIO(input_text)
            parser = cli.build_parser()
            args = parser.parse_args(['identity'])

            with mock_print() as fake_print:
                cli.run(args)

        fake_print.assert_called_once_with(input_text, end='')


class TestMain:

    def test_main(self):
        parser = cli.build_parser()
        args = parser.parse_args()

        with mock.patch.object(cli, 'run') as fake_run:
            cli.main()

        fake_run.assert_called_once_with(args)


@contextmanager
def mock_print(module=cli):
    with mock.patch.object(module, 'print') as fake_print:
        yield fake_print
