from unittest import TestCase, skip

from ipatok.ipa import (
	is_letter, is_tie_bar, is_diacritic, is_length, is_suprasegmental)



class IpaTestCase(TestCase):

	@skip
	def test_assert_char(self):
		pass

	def test_is_letter(self):
		self.assertTrue(is_letter('p'))
		self.assertTrue(is_letter('ʘ'))

	def test_is_tie_bar(self):
		self.assertTrue(is_tie_bar('◌͡'[1]))
		self.assertTrue(is_tie_bar('◌͜'[1]))

	def test_is_diacritic(self):
		self.assertTrue(is_diacritic('◌̥'[1]))
		self.assertTrue(is_diacritic('◌ʰ'[1]))
		self.assertTrue(is_diacritic('◌̃'[1]))
		self.assertTrue(is_diacritic('◌̚'[1]))

	def test_is_length(self):
		self.assertTrue(is_length('ː'))
		self.assertTrue(is_length('ˑ'))
		self.assertTrue(is_length('◌̆'[1]))

	def test_is_suprasegmental(self):
		self.assertTrue(is_suprasegmental('ˈ'))
		self.assertTrue(is_suprasegmental('◌̋'[1]))
		self.assertTrue(is_suprasegmental('↘'))
