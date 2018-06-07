====================================================
linecook: Prepare lines of text for easy consumption
====================================================

.. default-role:: literal

.. image:: https://travis-ci.com/tonysyu/linecook.svg?branch=master
   :target: https://travis-ci.com/tonysyu/linecook

.. image:: https://codecov.io/gh/tonysyu/linecook/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/tonysyu/linecook

.. image:: https://readthedocs.org/projects/linecook/badge/
   :target: https://linecook.readthedocs.io


See the documentation at https://linecook.readthedocs.io

NOTE: Most of this is just planning, and doesn't actually work yet.

This was originally designed as a tool to transform logging output into a form
that I'd prefer to consume::

    $ echo "Can I have a cheeseburger?" | linecook lolcats
    I can haz cheezburger?

`linecook` doesn't actually define way translate lines of text into lolcats,
but you could easily define your own:

.. code-block:: python

    {
        'replacers': {
            'request': ['s:Can I', 'I can'],
            'verb': ['s:have', 'haz'],
            'noun': ['s:cheeseburger', 'cheezburger'],
        },
        'recipes': {
            'lolcats': ['request', 'verb', 'noun'],
        },
    }

Recipes are just collections of transformations that translate a line of text
into another line of text.

transforms:
    A transform is the most generic type of transformation. It's just
    a function that takes a string and returns an output string.
colorizers:
    A colorizer is simply a transform that takes a substring match and wraps
    it with a terminal color.
replacers:
    A replacer is a simple way to specify a transform that replaces a substring
    pattern with some output text.
deleters:
    A deleter is simply a replacer where the output is an empty string.
filters:
    A filter matches lines of text, which are skipped.

Obviously, this is an incredibly basic (and ridiculous) example. A more useful
example colorizes lines of a log file using the following configuration:

.. code-block:: python

    {
        'colorizers': {
            'info_color': [r'w:INFO', 'cyan'],
            'warn_color': [r'w:WARN', 'yellow', ['bold']],
            'error_color': [r'w:ERROR', 'white', 'on_red'],
        },
        'recipes': {
            'log_level_color': [
                'info_color',
                'warn_color',
                'error_color',
            ],
            'logs': [
                'log_level_color',
            ],
        },
    }

You can use the ::

    $ tail -f path/to/log.txt | linecook logs

patterns:
    A pattern is a regex pattern for matching a piece of text.
recipes:
    A presenter is a collection of transforms used to transform a line of code,
    log entry, or whatever piece of text you like.

While `linecook` comes with a handful of patterns and transforms
to create your own recipes, the core idea is to make it easy to define your
own:

.. code-block:: python

    {
        'patterns': {
            'PATTERN_NAME': <MATCH_STRING>,
            ...
        },
        'filters': {
            'FILTER_NAME': <MATCH_STRING>,
            ...
        },
        'deleters': {
            'DELETER_NAME': <MATCH_STRING>,
            ...
        },
        'replacers': {
            'REPLACER_NAME': [<MATCH_STRING>, 'OUTPUT'],
            ...
        },
        'colorizers': {
            'COLORIZER_NAME': [<MATCH_STRING>, 'COLOR_NAME'],
            ...
        },
        'transforms': {
            'TRANSFORM_NAME': 'PACKAGE.MODULE.TRANSFORM_NAME',
            'TRANSFORM_NAME': <transform function>,
            'TRANSFORM_NAME': ['PACKAGE.MODULE.TRANSFORM_NAME', <MATCH_STRING>],
            'TRANSFORM_NAME': ['PACKAGE.MODULE.TRANSFORM_NAME', [ARG, ...], {'KEY': VALUE, ...}],
            'TRANSFORM_NAME': ['PACKAGE.MODULE.TRANSFORM_NAME', [ARG, ...], {'KEY': VALUE, ...}],
            'TRANSFORM_NAME': {
                'filter': <MATCH_STRING>,
                'then': <TRANSFORM>,
                'else': <TRANSFORM>,
            }
            ...
        },
        'recipes': {
            'NAME': [
                'TRANSFORM_NAME',
                ...
            ],
        },
        ...
    }


The `<MATCH_STRING>` above is a string that's prefixed with a match-string
type, as described below:
`'w:WORD'` (`'wi:WORD_IGNORE_CASE'`):
    An exact word match, which is basically a regex in the form of '\bWORD\b'.
`'x:EXACT_STRING'` (`'xi:EXACT_STRING_IGNORE_CASE'`):
    An exact string match, which only matches if the entire string matches,
    which is basically a regex in the form of `'^EXACT_STRING$'`.
`'p:PATTERN_NAME'`:
    A named version of any of the above match-strings.

You don't just have to put all your configuration in one place. You can easily
include any configuration as a dictionary that's importable:

.. code-block:: python

    {
        'includes': [
            'PACKAGE.MODULE.CONFIG_DICT',
            'PATH/TO/CONFIG.json',
            'PATH/TO/CONFIG.yaml',
            ...
        ],
        ...
    }
