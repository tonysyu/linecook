========
Overview
========

.. role:: blue
.. role:: cyan
.. role:: red
.. role:: yellow
.. role:: on-red
.. role:: black-on-yellow

`linecook` is a command-line tool that transforms lines of text into a form
that's pleasant to consume.

The core goal of `linecook` is to make it easy to create your own transforms to
parse whatever text you have. For example, if we have an `app.log` file that
looks like:

.. parsed-literal::
    :class: terminal

    :yellow:`$` tail app.log

    2018-06-09 13:55:26 INFO Dependencies loaded successfully
    2018-06-09 13:55:26 WARN Could not find version number for app
    2018-06-09 13:55:27 INFO Starting app...
    2018-06-09 13:55:27 ERROR SyntaxError: invalid syntax
        >>> while True print('Hello world')
           File "<stdin>", line 1
              while True print('Hello world')
                             ^
        SyntaxError: invalid syntax

If you want to highlight the log type and mute the dates/times, then you can
create a custom recipe in one of your :ref:`configuration files` like the
following:

.. code-block:: python

   from linecook import patterns as rx
   from linecook.transforms import color_text

   LINECOOK_RECIPES = {
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

.. parsed-literal::
    :class: terminal

    :yellow:`$` tail app.log | linecook my-logs

    :blue:`2018-06-09 13:55:26` :cyan:`INFO` Dependencies loaded successfully
    :blue:`2018-06-09 13:55:26` :black-on-yellow:`WARN` Could not find version number for app
    :blue:`2018-06-09 13:55:27` :cyan:`INFO` Starting app...
    :blue:`2018-06-09 13:55:27` :on-red:`ERROR` SyntaxError: invalid syntax
        >>> while True print('Hello world')
          File "<stdin>", line 1
            while True print('Hello world')
                           ^
        SyntaxError: invalid syntax

That's all there is to it!

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   self
   configuration.rst
   developer_guide.rst
   api/modules.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
