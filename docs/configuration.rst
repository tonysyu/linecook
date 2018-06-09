.. _configuration:

=============
Configuration
=============

.. _configuration files:

Configuration files
===================

The following configuration files are loaded, in order:

    - `linecook.default_config`: Package configuration
    - `~/.linecook/config.py`: User configuration
    - `./.linecook/config.py`: Local configuration

Each file should define a dictionary named `LINECOOK_CONFIG` containing keys
such as `transforms` and `recipes`.

Files loaded later (lower on the list) override values loaded earlier. Note
that the overriding happens at the *second* level of dictionaries. For example,
if `~/.linecook/config.py` is defined as::

    from linecook.transforms.core import color_text

    LINECOOK_CONFIG = {
        'transforms': {
            'warn_color': color_text(' WARN ', color='yellow'),
            'error_color': color_text(' ERROR ', on_color='on_red'),
        },
        'recipes': {
            'logs': ['warn_color', 'error_color'],
            'default': ['warn_color', 'error_color'],
        },
    }

And then, `./.linecook/config.py` is defined as::

    from linecook.transforms.core import filter_line

    LINECOOK_CONFIG = {
        'recipes': {
            'default': [filter_line(' DEBUG '), 'error_color']
        },
    }

The loaded result would roughly translate to::

    from linecook.transforms.core import color_text, filter_line

    LINECOOK_CONFIG = {
        'transforms': {
            'warn_color': color_text(' WARN ', color='yellow'),
            'error_color': color_text(' ERROR ', on_color='on_red'),
        },
        'recipes': {
            'logs': ['warn_color', 'error_color'],
            'default': [filter_line(' DEBUG '), 'error_color']
        },
    }

You'll notice that `recipes` doesn't match the `recipes` in the second config
file: Instead, the second file only overrode the `'default'` value in the first
config file, but preseved the `'logs'` value.
