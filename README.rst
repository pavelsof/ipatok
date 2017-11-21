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

``tokenise(string, strict=False, diphtongs=False, replace=False)`` takes an IPA
string and returns a list of tokens. A token usually consists of a single
letter together with its accompanying diacritics. If two letters are connected
by a tie bar, they are also considered a single token. Except for length
markers, suprasegmentals are excluded from the output. Whitespace is also
ignored. The function accepts the following keyword arguments:

- ``strict``: if set to ``True``, the function ensures that ``string`` complies
  to the `IPA spec`_ (the 2015 revision); a ``ValueError`` is raised if it does
  not. If set to ``False`` (the default), the role of non-IPA characters is
  guessed based on their Unicode category.
- ``replace``: if set to ``True``, the function replaces some common
  substitutes with their IPA-compliant counterparts, e.g. ``g → ɡ``, ``ɫ → l̴``,
  ``ʦ → t͡s``. Refer to ``ipatok/data/ipa.tsv`` for a full list.
- ``diphtongs``: if set to ``True``, the function groups together non-syllabic
  vowels with their syllabic neighbours (e.g. ``aɪ̯`` would form a single
  token). If set to ``False`` (the default), vowels are not tokenised together
  unless there is a connecting tie bar (e.g. ``a͡ɪ``).

``tokenize`` is an alias for ``tokenise``.


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
