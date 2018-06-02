import itertools

from toolz import dicttoolz

from .transforms.core import color_text


TRANSFORM_PARSERS = {}

TRANSFORM_PARSER_START_ORDER = []

TRANSFORM_PARSER_FINISH_ORDER = ['transforms']


def register_transform_parser(config_type):
    """Add parser to registry of known linecook config parsers.

    Args:
        config_type (str): The config type that is parsed by this decorated
            function The resulting output will be stored in the parsed config
            under this name.

    A config parser takes a sequence representing updated the an object
    containing the parsed data.

    You can register the a parser with the same name multiple times, which will
    simply override older instances.
    """
    def decorator(func):
        TRANSFORM_PARSERS[config_type] = func
        return func
    return decorator


@register_transform_parser('colorizers')
def parse_colorizers(colorizers_dict_seq):
    colorizers_dict = dicttoolz.merge(colorizers_dict_seq)
    return {key: color_text(color_kwargs)
            for key, color_kwargs in colorizers_dict.items()}


@register_transform_parser('transforms')
def parse_transforms(transforms_dict_seq):
    return dicttoolz.merge(transforms_dict_seq)


def iter_parsers():
    """Yield parsers in required order.

    Parsers in `TRANSFORM_PARSER_START_ORDER` are yielded first, those in
    `TRANSFORM_PARSER_FINISH_ORDER` are yielded last, and all other parsers in
    `TRANSFORM_PARSERS` are yielded in between in no guaranteed order.
    """
    unordered_parsers = (
        set(TRANSFORM_PARSERS)
        .difference(TRANSFORM_PARSER_START_ORDER)
        .difference(TRANSFORM_PARSER_FINISH_ORDER)
    )

    config_type_order = itertools.chain(
        TRANSFORM_PARSER_START_ORDER,
        unordered_parsers,
        TRANSFORM_PARSER_FINISH_ORDER
    )
    for config_type in config_type_order:
        parse = TRANSFORM_PARSERS.get(config_type)
        if parse:
            yield config_type, parse


def collect_tranforms(config_dicts):
    transforms = {}
    for config_type, parse in iter_parsers():
        config_type_data = get_value_from_each(config_type, config_dicts)
        transforms.update(parse(config_type_data))
    return transforms


def resolve_recipe(recipe, transforms_registry):
    for transform in recipe:
        transform = transforms_registry.get(transform, transform)
        if not callable(transform):
            msg = "Expected transform to be a callable, but found: {!r}"
            raise RuntimeError(msg.format(transform))
        yield transform


def collect_recipes(config_dicts, transforms_registry):
    recipe_dict = dicttoolz.merge(get_value_from_each('recipes', config_dicts))
    return {name: list(resolve_recipe(r, transforms_registry))
            for name, r in recipe_dict.items()}


def get_value_from_each(key, dict_list):
    return (d[key] for d in dict_list if key in d)
