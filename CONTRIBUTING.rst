=================
how to contribute
=================

Thank you for opening this file! :)


project setup
=============

.. code:: sh

    # clone this repo or your fork of it
    git clone github:pavelsof/ipatok
    cd ipatok

    # create a virtual env
    # the venv dir is git-ignored
    python3 -m venv venv
    source venv/bin/activate

    # install the dependencies
    # you can also pip install -r requirements.txt
    pip install pip-tools
    pip-sync

    # run the tests
    python -m unittest

    # run the code linter
    ruff check

    # run the code formatter
    ruff format


conventions
===========

For file encoding, newlines, indentation: please use the ``.editorconfig``
rules (`take a look here <https://editorconfig.org/>`_ if this is new for you).

For coding style: please follow `PEP8
<https://www.python.org/dev/peps/pep-0008/>`_.
