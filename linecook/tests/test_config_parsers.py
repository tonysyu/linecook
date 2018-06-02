from contextlib import contextmanager

import pytest

from linecook import config_parsers


def test_register_transform_parser():
    with mock_transform_parser_registry() as fake_registry:
        assert len(fake_registry) == 0

        @config_parsers.register_transform_parser('test')
        def fake_parser(*args, **kwargs):
            pass

        assert len(fake_registry) == 1
        assert fake_registry['test'] == fake_parser


class TestResolveRecipe:

    def test_transform_name_not_found(self):
        with pytest.raises(RuntimeError):
            list(config_parsers.resolve_recipe(['missing-transform-name'], {}))


@contextmanager
def mock_transform_parser_registry():
    original_registry = config_parsers.TRANSFORM_PARSERS
    config_parsers.TRANSFORM_PARSERS = {}
    try:
        yield config_parsers.TRANSFORM_PARSERS
    finally:
        config_parsers.TRANSFORM_PARSERS = original_registry
