====================================================
linecook: Prepare lines of text for easy consumption
====================================================

.. default-role:: literal

.. image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :target: https://github.com/tonysyu/linecook/blob/master/LICENSE

.. image:: https://travis-ci.com/tonysyu/linecook.svg?branch=master
   :target: https://travis-ci.com/tonysyu/linecook

.. image:: https://codecov.io/gh/tonysyu/linecook/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/tonysyu/linecook

.. image:: https://readthedocs.org/projects/linecook/badge/
   :target: https://linecook.readthedocs.io

`linecook` is a command-line tool that transforms lines of text into a form
that's pleasant to consume.

- **Documentation:** https://linecook.readthedocs.io
- **Source:** https://github.com/tonysyu/linecook

Install
=======

The recommended way of installing `linecook` is to use `pip`::

    pip install linecook

Cooking up some beautiful text
==============================

The core goal of `linecook` is to make it easy to create your own transforms to
parse whatever text you have. For example, take an `app.log` file that looks
like:

.. image:: docs/_static/images/app_log_raw.png

If you want to highlight the log type and mute the dates/times, then you can
create a custom recipe in one of your `configuration files
<https://linecook.readthedocs.io/en/latest/configuration.html>`_ like the
following:

.. code-block:: python

   from linecook import patterns as rx
   from linecook.transforms import color_text

   LINECOOK_CONFIG = {
       'recipes': {
           'my-logs': [
                color_text(rx.any_of(rx.date, rx.time), color='blue'),
                color_text('INFO', color='cyan'),
                color_text('WARN', color='grey', on_color='on_yellow'),
                color_text('ERROR', on_color='on_red'),
           ],
       },
   }

To use this recipe, you can just pipe the log output to `linecook` with your
new recipe as an argument:

.. image:: docs/_static/images/app_log_linecook.png

That's all there is to it!

See Also
========

- `grc <https://github.com/garabik/grc>`_: A generic colouriser (sic;) for log
  files and command output.
- `rainbow <https://github.com/nicoulaj/rainbow>`_: Colorize commands output or
  STDIN using patterns.
- `multitail <https://www.vanheusden.com/multitail/>`_: Tail multiple files at
  once, with features to colorize, filter, and merge.
- `colortail <https://github.com/joakim666/colortail>`_: Like the tail command
  line utility but with colors
- `StackOverflow post on colored output
  <https://unix.stackexchange.com/questions/8414>`_
