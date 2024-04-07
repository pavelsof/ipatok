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

``tokenise(string, strict=False, replace=False, diphthongs=False, tones=False,
unknown=False, merge=None)`` takes an IPA string and returns a list of tokens.
A token usually consists of a single letter together with its accompanying
diacritics. If two letters are connected by a tie bar, they are also considered
a single token. Except for length markers, suprasegmentals are excluded from
the output. Whitespace is also ignored. The function accepts the following
keyword arguments:

- ``strict``: if set to ``True``, the function ensures that ``string`` complies
  to the IPA spec (`the 2015 revision`_); a ``ValueError`` is raised if it does
  not. If set to ``False`` (the default), the role of non-IPA characters is
  guessed based on their Unicode category (cf. the pitfalls section below).
- ``replace``: if set to ``True``, the function replaces some common
  substitutes with their IPA-compliant counterparts, e.g. ``g → ɡ``, ``ɫ → l̴``,
  ``ʦ → t͡s``. Refer to ``ipatok/data/replacements.tsv`` for a full list. If
  both ``strict`` and ``replace`` are set to ``True``, replacing is done before
  checking for spec compliance.
- ``diphthongs``: if set to ``True``, the function groups together non-syllabic
  vowels with their syllabic neighbours (e.g. ``aɪ̯`` would form a single
  token). If set to ``False`` (the default), vowels are not tokenised together
  unless there is a connecting tie bar (e.g. ``a͡ɪ``).
- ``tones``: if set to ``True``, tone and word accents are included in the
  output (accent markers as diacritics and Chao letters as separate tokens). If
  set to ``False`` (the default), these are ignored.
- ``unknown``: if set to ``True``, the output includes (as separate tokens)
  symbols that cannot be classified as letters, diacritics or suprasegmentals
  (e.g. ``-``, ``/``, ``$``). If set to ``False`` (the default), such symbols
  are ignored. It does not have effect if ``strict`` is set to ``True``.
- ``merge``: expects a ``str, str → bool`` function to be applied onto each
  pair of consecutive tokens; those for which the output is ``True`` are merged
  together. You can use this to, e.g., plug in your own diphthong detection
  algorithm:

  >>> tokenise(string, diphthongs=False, merge=custom_func)

``tokenize`` is an alias for ``tokenise``.

other functions
---------------

``replace_digits_with_chao(string, inverse=False)`` takes an IPA string and
replaces the digits 1-5 (also in superscript) with Chao tone letters. If
``inverse=True``, smaller digits are converted into higher tones; otherwise,
they are converted into lower tones (the default).  Equal consecutive digits
are collapsed into a single Chao letter (e.g. ``55 → ˥``).

>>> tokenise(replace_numbers_with_chao('ɕia⁵¹ɕyɛ²¹⁴'), tones=True)
['ɕ', 'i', 'a', '˥˩', 'ɕ', 'y', 'ɛ', '˨˩˦']


``clusterise(string, strict=False, replace=False, diphthongs=False,
tones=False, unknown=False, merge=None)`` takes an IPA string and lists its
consonant and vowel clusters. The keyword arguments are identical as for
``tokenise``:

>>> from ipatok import clusterise
>>> clusterise("kiaːltaːʃ")
['k', 'iaː', 'lt', 'aː', 'ʃ']

``clusterize`` is an alias for ``clusterise``.

pitfalls
========

When ``strict=True`` each symbol is looked up in the spec and there is no
ambiguity as to how the input should be tokenised.

With ``strict=False`` IPA symbols are still handled correctly. A non-IPA symbol
would be treated as follows:

- if it is a non-modifier letter (e.g. ``Γ``), it is considered a consonant;
- if it is a modifier (e.g. ``ˀ``) or a combining mark (e.g. ``ə̇``), it is
  considered a diacritic;
- if it is a `modifier tone letter`_ (e.g. ``꜍``), it is considered a tone
  symbol;
- if it is neither of those, it is considered an unknown symbol.

Regardless of the value of ``strict``, whitespace characters and underscores
are considered to be word boundaries, i.e. there would not be tokens grouping
together symbols separated by these characters, even though the latter are not
included in the output.


installation
============

This is a Python 3 package without dependencies and it is offered at the
`Cheese Shop`_::

    # usually within a virtual environment
    pip install ipatok


other IPA packages
==================

- lingpy_ is a historical linguistics suite that includes an ipa2tokens_
  function.
- loanpy_ is another historical linguistics suite which works with IPA strings.
- ipapy_ is a package for working with IPA strings.
- ipalint_ provides a command-line tool for checking IPA datasets for errors
  and inconsistencies.
- asjp_ provides functions for converting between IPA and ASJP.


licence
=======

MIT. Do as you please and praise the snake gods.


.. _`the 2015 revision`: https://www.internationalphoneticassociation.org/sites/default/files/phonsymbol.pdf
.. _`modifier tone letter`: http://www.unicode.org/charts/PDF/UA700.pdf
.. _`Cheese Shop`: https://pypi.python.org/pypi/ipatok/
.. _`lingpy`: https://pypi.python.org/pypi/lingpy/
.. _`ipa2tokens`: http://lingpy.org/reference/lingpy.sequence.html#lingpy.sequence.sound_classes.ipa2tokens
.. _`loanpy`: https://pypi.org/project/loanpy/
.. _`ipapy`: https://pypi.python.org/pypi/ipapy/
.. _`ipalint`: https://pypi.python.org/pypi/ipalint/
.. _`asjp`: https://pypi.python.org/pypi/asjp/
