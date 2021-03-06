=================
Developer's Guide
=================

Prerequisites
=============

The `linecook` package uses `poetry <https://github.com/sdispater/poetry>`_ for
dependency management and distribution. You call install `poetry` using::

    curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python


Setup
=====

Clone from github::

    git clone https://github.com/tonysyu/linecook.git

Install development requirements::

    cd linecook
    poetry install

For building the documentation locally, you'll also need to run::

    poetry install --extras "docs"

Development
===========

For local development, you'll also want to install pre-commit hooks using::

    poetry run pre-commit install

By default, this will run the black code formatter on *changed* files on every
commit. To run black on all files::

    poetry run pre-commit run --all-files


Running tests
=============

The test suite can be run without installing dev requirements using::

    $ tox


To run tests with a specific Python version, run::

    $ tox --env py36

You can isolate specific test files/functions/methods with::

    tox PATH/TO/TEST.py
    tox PATH/TO/TEST.py::TEST_FUNCTION
    tox PATH/TO/TEST.py::TEST_CLASS::TEST_METHOD


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


Release
=======

A reminder for the maintainers on how to deploy.

- Update the version and push::

    $ bumpversion patch # possible: major / minor / patch
    $ git push
    $ git push --tags

- Build release, deploy to PyPI, and clean ::

    $ make release
    $ make clean
