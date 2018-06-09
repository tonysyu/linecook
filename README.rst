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
            'request': ['Can I', 'I can'],
            'verb': ['have', 'haz'],
            'noun': ['cheeseburger', 'cheezburger'],
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
            'warn_color': {
                'match_pattern': ' WARN ',
                'color': 'yellow',
            },
            'error_color': {
                'match_pattern': ' ERROR ',
                'on_color': 'on_red',
            },
        },
        'recipes': {
            'logs': [
                'warn_color',
                'error_color',
            ],
        },
    }

You can use the ::

    $ tail -f path/to/log.txt | linecook logs
