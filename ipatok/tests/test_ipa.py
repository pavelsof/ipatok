from functools import partial
from unittest import TestCase

from ipatok.ipa import is_letter, is_vowel, is_tie_bar
from ipatok.ipa import is_diacritic
from ipatok.ipa import is_suprasegmental, is_length
from ipatok.ipa import get_precomposed_chars
from ipatok.ipa import replace_substitutes



class IpaTestCase(TestCase):

	def test_is_letter(self):
		for strict in [True, False]:
			func = partial(is_letter, strict=strict)

			self.assertTrue(func('p'))
			self.assertTrue(func('ç'))
			self.assertTrue(func('ʘ'))
			self.assertTrue(func('ɥ'))
			self.assertTrue(func('ɒ'))

			self.assertFalse(func('ʰ'))
			self.assertFalse(func('ʷ'))

	def test_is_letter_non_ipa(self):
		for char in ['ʣ', 'ɫ', 'g', 'Γ', 'F', 'ǈ']:
			self.assertFalse(is_letter(char, strict=True))
			self.assertTrue(is_letter(char, strict=False))

	def test_is_vowel(self):
		self.assertTrue(is_vowel('i'))
		self.assertTrue(is_vowel('ɶ'))
		self.assertTrue(is_vowel('ɤ'))
		self.assertTrue(is_vowel('ɒ'))

		self.assertFalse(is_vowel('ʍ'))
		self.assertFalse(is_vowel('ɧ'))

	def test_is_tie_bar(self):
		self.assertTrue(is_tie_bar('◌͡'[1]))
		self.assertTrue(is_tie_bar('◌͜'[1]))

		self.assertFalse(is_tie_bar('ʋ'))
		self.assertFalse(is_tie_bar('‿'))

	def test_is_diacritic(self):
		for strict in [True, False]:
			func = partial(is_diacritic, strict=strict)

			self.assertTrue(func('◌̥'[1]))
			self.assertTrue(func('◌ʰ'[1]))
			self.assertTrue(func('◌̃'[1]))
			self.assertTrue(func('◌̚'[1]))

			self.assertFalse(func('ʌ'))
			self.assertFalse(func('ˌ'))
			self.assertFalse(func('ː'))

	def test_is_diacritic_non_ipa(self):
		for char in ['ˀ', '◌̇'[1], '◌̣'[1]]:
			self.assertFalse(is_diacritic(char, strict=True))
			self.assertTrue(is_diacritic(char, strict=False))

	def test_is_suprasegmental(self):
		self.assertTrue(is_suprasegmental('ˈ'))
		self.assertTrue(is_suprasegmental('◌̋'[1]))
		self.assertTrue(is_suprasegmental('↘'))

		self.assertFalse(is_suprasegmental('ɮ'))
		self.assertFalse(is_suprasegmental('◌͜'[1]))
		self.assertFalse(is_suprasegmental('◌̝'[1]))

	def test_is_length(self):
		self.assertTrue(is_length('ː'))
		self.assertTrue(is_length('ˑ'))
		self.assertTrue(is_length('◌̆'[1]))

		self.assertFalse(is_length('ʼ'))
		self.assertFalse(is_length('◌̃'[1]))

	def test_get_precomposed_chars(self):
		self.assertEqual(get_precomposed_chars(), set(['ç']))

	def test_replace_substitutes(self):
		self.assertEqual(replace_substitutes('g'), 'ɡ')
		self.assertEqual(replace_substitutes('ł'), 'l̴')
		self.assertEqual(replace_substitutes('ɫ'), 'l̴')
		self.assertEqual(replace_substitutes('·'), 'ˑ')
