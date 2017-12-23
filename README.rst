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

``tokenise(string, strict=False, replace=False, diphtongs=False, merge=None)``
takes an IPA string and returns a list of tokens. A token usually consists of a
single letter together with its accompanying diacritics. If two letters are
connected by a tie bar, they are also considered a single token. Except for
length markers, suprasegmentals are excluded from the output. Whitespace is
also ignored. The function accepts the following keyword arguments:

- ``strict``: if set to ``True``, the function ensures that ``string`` complies
  to the IPA spec (`the 2015 revision`_); a ``ValueError`` is raised if it does
  not. If set to ``False`` (the default), the role of non-IPA characters is
  guessed based on their Unicode category.
- ``replace``: if set to ``True``, the function replaces some common
  substitutes with their IPA-compliant counterparts, e.g. ``g → ɡ``, ``ɫ → l̴``,
  ``ʦ → t͡s``. Refer to ``ipatok/data/replacements.tsv`` for a full list. If
  both ``strict`` and ``replace`` are set to ``True``, replacing is done before
  checking for spec compliance.
- ``diphtongs``: if set to ``True``, the function groups together non-syllabic
  vowels with their syllabic neighbours (e.g. ``aɪ̯`` would form a single
  token). If set to ``False`` (the default), vowels are not tokenised together
  unless there is a connecting tie bar (e.g. ``a͡ɪ``).
- ``merge``: expects a ``str, str → bool`` function to be applied onto each
  pair of consecutive tokens; those for which the output is ``True`` are merged
  together. You can use this to, e.g., plug in your own diphtong detection
  algorithm:

  >>> tokenise(string, diphtongs=False, merge=custom_func)

``tokenize`` is an alias for ``tokenise``.


pitfalls
========

When ``strict=True`` each symbol is looked up in the spec and there is no
ambiguity as to how the input should be tokenised.

With ``strict=False`` IPA symbols are still handled correctly. A non-IPA symbol
would be treated as follows:

- if it is a non-modifier letter (e.g. ``Γ``), it is considered a consonant;
- if it is a modifier (e.g. ``ˀ``) or a combining mark (e.g. ``ə̇``), it is
  considered a diacritic;
- if it is neither of those, it is ignored.

Regardless of the value of ``strict``, whitespace characters and underscores
are considered to be word boundaries, i.e. there would not be tokens grouping
together symbols separated by these characters, even though the latter are not
included in the output.


installation
============

This is a standard Python 3 package without dependencies. It is offered at the
`Cheese Shop`_, so you can install it with pip::

    pip install ipatok

or, alternatively, you can clone this repo (safe to delete afterwards) and do::

    python setup.py test
    python setup.py install

Of course, this could be happening within a virtualenv/venv as well.


other IPA packages
==================

- lingpy_ is a historical linguistics suite that includes an ipa2tokens_
  function.
- ipapy_ is a package for working with IPA strings.
- ipalint_ provides a command-line tool for checking IPA datasets for errors
  and inconsistencies.


licence
=======

MIT. Do as you please and praise the snake gods.

.. _`the 2015 revision`: https://www.internationalphoneticassociation.org/sites/default/files/phonsymbol.pdf
.. _`Cheese Shop`: https://pypi.python.org/pypi/ipatok
.. _`lingpy`: https://pypi.python.org/pypi/lingpy
.. _`ipa2tokens`: http://lingpy.org/reference/lingpy.sequence.html#lingpy.sequence.sound_classes.ipa2tokens
.. _`ipapy`: https://pypi.python.org/pypi/ipapy
.. _`ipalint`: https://pypi.python.org/pypi/ipalint
