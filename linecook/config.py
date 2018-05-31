import imp
from pathlib import Path

from . import default_config


class LinecookConfig(object):

    def __init__(self, config_dicts):
        self.recipes = {}
        for config in config_dicts:
            self.recipes.update(config.get('recipes', {}))


def load_config_file_from_path(path):
    try:
        module = imp.load_source('linecook.custom.config', str(path))
        return module.LINECOOK_CONFIG
    except FileNotFoundError:
        return {}


def load_config():
    return LinecookConfig([
        default_config.LINECOOK_CONFIG,
        load_config_file_from_path(Path('~/.linecook/config.py').expanduser())
    ])
