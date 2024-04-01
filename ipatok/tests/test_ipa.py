from functools import partial
from unittest import TestCase

from ipatok.ipa import (
    is_letter,
    is_vowel,
    is_tie_bar,
    is_diacritic,
    is_suprasegmental,
    is_length,
    is_tone,
    get_precomposed_chars,
    replace_substitutes,
    chart,
)


class IpaTestCase(TestCase):
    def test_is_letter(self):
        """
        is_letter should always return True for IPA letters and False for other
        IPA symbols.
        """
        for strict in [True, False]:
            func = partial(is_letter, strict=strict)

            self.assertTrue(func('p'))
            self.assertTrue(func('ç'))
            self.assertTrue(func('ʘ'))
            self.assertTrue(func('ɥ'))
            self.assertTrue(func('ɒ'))

            self.assertFalse(func('ʰ'))
            self.assertFalse(func('ʷ'))
            self.assertFalse(func('꜍'))

            [self.assertTrue(func(x)) for x in chart.consonants]
            [self.assertTrue(func(x)) for x in chart.vowels]

            [self.assertFalse(func(x)) for x in chart.tie_bars]
            [self.assertFalse(func(x)) for x in chart.diacritics]
            [self.assertFalse(func(x)) for x in chart.suprasegmentals]
            [self.assertFalse(func(x)) for x in chart.lengths]
            [self.assertFalse(func(x)) for x in chart.tones]

    def test_is_letter_non_ipa(self):
        """
        is_letter should return False for non-IPA letters in strict mode and
        True in non-strict mode.
        """
        for char in ['ʣ', 'ɫ', 'g', 'Γ', 'F', 'ǈ']:
            self.assertFalse(is_letter(char, strict=True))
            self.assertTrue(is_letter(char, strict=False))

    def test_is_vowel(self):
        """
        is_vowel should return True for IPA vowels and False for other IPA
        symbols.
        """
        self.assertTrue(is_vowel('i'))
        self.assertTrue(is_vowel('ɶ'))
        self.assertTrue(is_vowel('ɤ'))
        self.assertTrue(is_vowel('ɒ'))

        self.assertFalse(is_vowel('ʍ'))
        self.assertFalse(is_vowel('ɧ'))
        self.assertFalse(is_vowel('꜍'))

        [self.assertTrue(is_vowel(x)) for x in chart.vowels]

        [self.assertFalse(is_vowel(x)) for x in chart.consonants]
        [self.assertFalse(is_vowel(x)) for x in chart.tie_bars]
        [self.assertFalse(is_vowel(x)) for x in chart.diacritics]
        [self.assertFalse(is_vowel(x)) for x in chart.suprasegmentals]
        [self.assertFalse(is_vowel(x)) for x in chart.lengths]
        [self.assertFalse(is_vowel(x)) for x in chart.tones]

    def test_is_tie_bar(self):
        """
        is_tie_bar should return True for IPA tie bars and False for other IPA
        symbols.
        """
        self.assertTrue(is_tie_bar('◌͡'[1]))
        self.assertTrue(is_tie_bar('◌͜'[1]))

        self.assertFalse(is_tie_bar('ʋ'))
        self.assertFalse(is_tie_bar('‿'))

        [self.assertTrue(is_tie_bar(x)) for x in chart.tie_bars]

        [self.assertFalse(is_tie_bar(x)) for x in chart.consonants]
        [self.assertFalse(is_tie_bar(x)) for x in chart.vowels]
        [self.assertFalse(is_tie_bar(x)) for x in chart.diacritics]
        [self.assertFalse(is_tie_bar(x)) for x in chart.suprasegmentals]
        [self.assertFalse(is_tie_bar(x)) for x in chart.lengths]
        [self.assertFalse(is_tie_bar(x)) for x in chart.tones]

    def test_is_diacritic(self):
        """
        is_diacritic should always return True for IPA diacritics and False for
        other IPA symbols.
        """
        for strict in [True, False]:
            func = partial(is_diacritic, strict=strict)

            self.assertTrue(func('◌̥'[1]))
            self.assertTrue(func('◌ʰ'[1]))
            self.assertTrue(func('◌̃'[1]))
            self.assertTrue(func('◌̚'[1]))

            self.assertFalse(func('ʌ'))
            self.assertFalse(func('ˌ'))
            self.assertFalse(func('ː'))
            self.assertFalse(func('꜍'))

            [self.assertTrue(func(x)) for x in chart.diacritics]

            [self.assertFalse(func(x)) for x in chart.consonants]
            [self.assertFalse(func(x)) for x in chart.vowels]
            [self.assertFalse(func(x)) for x in chart.tie_bars]
            [self.assertFalse(func(x)) for x in chart.suprasegmentals]
            [self.assertFalse(func(x)) for x in chart.lengths]
            [self.assertFalse(func(x)) for x in chart.tones]

    def test_is_diacritic_non_ipa(self):
        """
        is_diacritic should return False for non-IPA diacritics in strict mode
        and True in non-strict mode.
        """
        for char in ['ˀ', '◌̇'[1], '◌̣'[1]]:
            self.assertFalse(is_diacritic(char, strict=True))
            self.assertTrue(is_diacritic(char, strict=False))

    def test_is_suprasegmental(self):
        """
        is_suprasegmental should return True for IPA suprasegmentals and False
        for other IPA symbols.
        """
        for strict in [True, False]:
            func = partial(is_suprasegmental, strict=strict)

            self.assertTrue(func('ˈ'))
            self.assertTrue(func('◌̋'[1]))
            self.assertTrue(func('↘'))
            self.assertTrue(func('.'))
            self.assertTrue(func('‿'))

            self.assertFalse(func('ɮ'))
            self.assertFalse(func('◌͜'[1]))
            self.assertFalse(func('◌̝'[1]))

            [self.assertTrue(func(x)) for x in chart.suprasegmentals]
            [self.assertTrue(func(x)) for x in chart.lengths]
            [self.assertTrue(func(x)) for x in chart.tones]

            [self.assertFalse(func(x)) for x in chart.consonants]
            [self.assertFalse(func(x)) for x in chart.vowels]
            [self.assertFalse(func(x)) for x in chart.tie_bars]
            [self.assertFalse(func(x)) for x in chart.diacritics]

    def test_is_length(self):
        """
        is_length should return True for IPA length markers and False for other
        IPA symbols.
        """
        self.assertTrue(is_length('ː'))
        self.assertTrue(is_length('ˑ'))
        self.assertTrue(is_length('◌̆'[1]))

        self.assertFalse(is_length('ʼ'))
        self.assertFalse(is_length('◌̃'[1]))
        self.assertFalse(is_length('꜍'))

        [self.assertTrue(is_length(x)) for x in chart.lengths]

        [self.assertFalse(is_length(x)) for x in chart.consonants]
        [self.assertFalse(is_length(x)) for x in chart.vowels]
        [self.assertFalse(is_length(x)) for x in chart.tie_bars]
        [self.assertFalse(is_length(x)) for x in chart.diacritics]
        [self.assertFalse(is_length(x)) for x in chart.suprasegmentals]
        [self.assertFalse(is_length(x)) for x in chart.tones]

    def test_is_tone(self):
        """
        is_tone should always return True for IPA tone and word accent symbols
        and False for other IPA symbols.
        """
        for strict in [True, False]:
            func = partial(is_tone, strict=strict)

            [self.assertTrue(func(x)) for x in chart.tones]

            [self.assertFalse(func(x)) for x in chart.consonants]
            [self.assertFalse(func(x)) for x in chart.vowels]
            [self.assertFalse(func(x)) for x in chart.tie_bars]
            [self.assertFalse(func(x)) for x in chart.diacritics]
            [self.assertFalse(func(x)) for x in chart.suprasegmentals]
            [self.assertFalse(func(x)) for x in chart.lengths]

    def test_is_tone_non_ipa(self):
        """
        is_tone should return False for non-IPA tone symbols in strict mode and
        True in non-strict mode.
        """
        for char in ['꜀', '꜍', 'ꜟ']:
            self.assertFalse(is_tone(char, strict=True))
            self.assertTrue(is_tone(char, strict=False))

    def test_get_precomposed_chars(self):
        self.assertEqual(get_precomposed_chars(), set(['ç']))

    def test_replace_substitutes(self):
        self.assertEqual(replace_substitutes('g'), 'ɡ')
        self.assertEqual(replace_substitutes('ł'), 'l̴')
        self.assertEqual(replace_substitutes('ɫ'), 'l̴')
        self.assertEqual(replace_substitutes('·'), 'ˑ')
