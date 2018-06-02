import imp
from os import path

from . import default_config
from .config_parsers import collect_recipes, collect_tranforms


# File configuration order: Files later in the list override earlier ones.
CONFIG_SEARCH_PATHS = [
    path.expanduser('~/.linecook/config.py'),
    path.expanduser('~/.linecookrc'),
    path.abspath('./.linecookrc'),
]


class LineCookConfig(object):

    def __init__(self, config_dicts):
        self.transforms = collect_tranforms(config_dicts)
        self.recipes = collect_recipes(config_dicts, self.transforms)


def load_config_file_from_path(path):
    try:
        module = imp.load_source('linecook_custom_config', path)
        return module.LINECOOK_CONFIG
    except (IOError, OSError):
        return {}


def load_config():
    """Return `LineCookConfig` reduced from all known configuration files."""

    config_dicts = [default_config.LINECOOK_CONFIG]
    config_dicts.extend(load_config_file_from_path(file_path)
                        for file_path in CONFIG_SEARCH_PATHS)
    return LineCookConfig(config_dicts)
