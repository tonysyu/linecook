=================
Developer's Guide
=================

Setup
=====

Clone from github::

    git clone https://github.com/tonysyu/linecook.git

Install development requirements::

    cd linecook
    pip install -e .[dev]


Running tests
=============

The test suite can be run without installing dev requirements using::

    python setup.py test

That said, running pytest directly provides more options for debugging. With
dev requirements installed, you can just run the following from the root
directory of the repo::

    pytest

You can isolate specific test files/functions/methods with::

    pytest PATH/TO/TEST.py
    pytest PATH/TO/TEST.py::TEST_FUNCTION
    pytest PATH/TO/TEST.py::TEST_CLASS::TEST_METHOD


Documentation
=============

Documentation is built from within the docs directory::

    cd docs
    make html

After building, you can view the docs at `docs/_build/html/index.html`.


Debugging
=========

It turns out that breakpoints are a bit tricky when processing streamed input.
A simple `pdb.set_trace()` will fail, so you'll need to try one of the
solutions described on StackOverflow [1]_, [2]_ (`answer that worked for me`_).

Better yet, if you can use a single line of text can be passed in to test
an issue, you can use the `--text` (`-t`) flag instead of piping text::

     linecook <RECIPE> --text 'Line of text to test'

.. [1] https://stackoverflow.com/questions/17074177/how-to-debug-python-cli-that-takes-stdin
.. [2] https://stackoverflow.com/questions/9178751/use-pdb-set-trace-in-a-script-that-reads-stdin-via-a-pipe
.. _answer that worked for me: https://stackoverflow.com/a/48430325/260303
