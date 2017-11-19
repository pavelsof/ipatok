======
ipatok
======

A simple IPA tokeniser, as simple as in:

>>> from ipatok import tokenise
>>> tokenise('ˈtiːt͡ʃə')
['t', 'iː', 't͡ʃ', 'ə']
>>> tokenise('ʃːjeq͡χːʼjer')
['ʃː', 'j', 'e', 'q͡χːʼ', 'j', 'e', 'r']


api
===

``tokenise(string, strict=True)`` takes an IPA string and returns a list of
tokens. A token usually consists of a single letter together with its
accompanying diacritics. If two letters are connected by a tie bar, they are
also considered a single token. Except for length markers, suprasegmentals are
excluded from the output. Whitespace is also ignored.

By default the function raises a ``ValueError`` if the string does not conform
to the `IPA spec`_ (the 2015 revision). Invoking it with ``strict=False`` makes
it accept some common replacements such as ``g`` and ``ɫ``.

``tokenize(string, strict=True)`` is an alias for ``tokenise``.


installation
============

This is a standard Python 3 package without dependencies. It is offered at the
`Cheese Shop`_, so you can install it with pip::

    pip install ipatok

or, alternatively, you can clone this repo (safe to delete afterwards) and do::

    python setup.py test
    python setup.py install

Of course, this could be happening within a virtualenv/venv as well.


similar projects
================

* lingpy_ provides an ipa2tokens_ function.


licence
=======

MIT. Do as you please and praise the snake gods.

.. _`IPA spec`: https://www.internationalphoneticassociation.org/sites/default/files/phonsymbol.pdf
.. _`Cheese Shop`: https://pypi.python.org/pypi/ipatok
.. _`lingpy`: http://lingpy.org/
.. _`ipa2tokens`: http://lingpy.org/reference/lingpy.sequence.html#lingpy.sequence.sound_classes.ipa2tokens
