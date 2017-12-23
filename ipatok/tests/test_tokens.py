from functools import partial
from itertools import product
from unittest import TestCase

from ipatok.tokens import normalise, group, are_diphtong, tokenise



class TokensTestCase(TestCase):
	"""
	The IPA strings are sourced from NorthEuraLex (languages: ady, ava, bul,
	ckt, deu, eng).
	"""

	def test_normalise(self):
		"""
		The voiceless palatal fricative should be in normal form C in the
		output, regardless of its input form.
		"""
		self.assertEqual(normalise('nɪçt'), 'nɪçt')  # ç in normal form C
		self.assertEqual(normalise('nɪçt'), 'nɪçt')  # ç in normal form D

	def test_group(self):
		self.assertEqual(group(lambda: True, []), [])

		for i in range(4, 1):
			self.assertEqual(group(lambda x, y: x == y, ['a'] * i), ['a' * i])

	def test_are_diphtong(self):
		self.assertTrue(are_diphtong('ə', 'ə̯'))
		self.assertTrue(are_diphtong('ə̯', 'ə'))
		self.assertTrue(are_diphtong('ə̯', 'ə̯'))
		self.assertFalse(are_diphtong('ə', 'ə'))

		self.assertTrue(are_diphtong('əə̯', 'ə̯'))
		self.assertTrue(are_diphtong('ə̯ə', 'ə̯'))
		self.assertFalse(are_diphtong('əə̯', 'ə'))
		self.assertFalse(are_diphtong('ə̯ə', 'ə'))

	def test_tokenise(self):
		"""
		IPA-compliant strings should be correctly tokenised, regardless of the
		flag values.
		"""
		for comb in product([True, False], [True, False], [True, False]):
			func = partial(tokenise,
					strict=comb[0], replace=comb[1], diphtongs=comb[2])

			self.assertEqual(func('miq͡χː'), ['m', 'i', 'q͡χː'])
			self.assertEqual(func('ʃːjeq͡χːʼjer'), ['ʃː', 'j', 'e', 'q͡χːʼ', 'j', 'e', 'r'])
			self.assertEqual(func('t͡ɬʼibil'), ['t͡ɬʼ', 'i', 'b', 'i', 'l'])
			self.assertEqual(func('ɬalkʼ'), ['ɬ', 'a', 'l', 'kʼ'])

			self.assertEqual(func('lit͡sɛ'), ['l', 'i', 't͡s', 'ɛ'])
			self.assertEqual(func('t͡ʃɛʎust'), ['t͡ʃ', 'ɛ', 'ʎ', 'u', 's', 't'])
			self.assertEqual(func('dirʲa'), ['d', 'i', 'rʲ', 'a'])
			self.assertEqual(func('ut͡ʃa sɛ'), ['u', 't͡ʃ', 'a', 's', 'ɛ'])

			self.assertEqual(func('nɪçt'), ['n', 'ɪ', 'ç', 't'])

			self.assertEqual(func('ˈd͡ʒɔɪ'), ['d͡ʒ', 'ɔ', 'ɪ'])
			self.assertEqual(func('ˈtiːt͡ʃə'), ['t', 'iː', 't͡ʃ', 'ə'])
			self.assertEqual(func('t͡ʃuːz'), ['t͡ʃ', 'uː', 'z'])

	def test_tokenise_non_ipa(self):
		"""
		Tokenising non-compliant strings should raise ValueError unless strict
		is False, regardless of the other flags' values.
		"""
		for comb in product([True, False], [True, False]):
			func = partial(tokenise, replace=comb[0], diphtongs=comb[1])

			with self.assertRaises(ValueError):
				func('ʷəˈʁʷa', strict=True)
			self.assertEqual(func('ʷəˈʁʷa', strict=False), ['ʷ', 'ə', 'ʁʷ', 'a'])

			with self.assertRaises(ValueError):
				func('t͡ɕˀet͡ɕeŋ', strict=True)
			self.assertEqual(func('t͡ɕˀet͡ɕeŋ', strict=False), ['t͡ɕˀ', 'e', 't͡ɕ', 'e', 'ŋ'])

			with self.assertRaises(ValueError):
				func('kat͡ɕˀaɹ', strict=True)
			self.assertEqual(func('kat͡ɕˀaɹ', strict=False), ['k', 'a', 't͡ɕˀ', 'a', 'ɹ'])

	def test_tokenise_replace(self):
		"""
		Strings containing common substitutes but otherwise IPA-compliant
		should pass the strictness check only if replace is True.
		"""
		for diphtongs in [True, False]:
			func = partial(tokenise, strict=True, diphtongs=diphtongs)

			with self.assertRaises(ValueError):
				func('t͡ʃɛɫɔ', replace=False)
			self.assertEqual(func('t͡ʃɛɫɔ', replace=True), ['t͡ʃ', 'ɛ', 'l̴', 'ɔ'])

			with self.assertRaises(ValueError):
				func('ɫuna', replace=False)
			self.assertEqual(func('ɫuna', replace=True), ['l̴', 'u', 'n', 'a'])

	def test_tokenise_diphtongs(self):
		"""
		Diphtongs in IPA-compliant strings should be merged depending on the
		diphtongs flag, regardless of the other flags' values.
		"""
		for comb in product([True, False], [True, False]):
			func = partial(tokenise, strict=comb[0], replace=comb[1])

			self.assertEqual(func('t͡saɪ̯çən', diphtongs=False), ['t͡s', 'a', 'ɪ̯', 'ç', 'ə', 'n'])
			self.assertEqual(func('t͡saɪ̯çən', diphtongs=True), ['t͡s', 'aɪ̯', 'ç', 'ə', 'n'])

			self.assertEqual(func('hɛɐ̯t͡s', diphtongs=False), ['h', 'ɛ', 'ɐ̯', 't͡s'])
			self.assertEqual(func('hɛɐ̯t͡s', diphtongs=True), ['h', 'ɛɐ̯', 't͡s'])

			self.assertEqual(func('moːɐ̯', diphtongs=False), ['m', 'oː', 'ɐ̯'])
			self.assertEqual(func('moːɐ̯', diphtongs=True), ['m', 'oːɐ̯'])

			self.assertEqual(func('aɪ̯çhœɐ̯nçən', diphtongs=False), ['a', 'ɪ̯', 'ç', 'h', 'œ', 'ɐ̯', 'n', 'ç', 'ə', 'n'])
			self.assertEqual(func('aɪ̯çhœɐ̯nçən', diphtongs=True), ['aɪ̯', 'ç', 'h', 'œɐ̯', 'n', 'ç', 'ə', 'n'])

			self.assertEqual(func('klaʊ̯ə', diphtongs=False), ['k', 'l', 'a', 'ʊ̯', 'ə'])
			self.assertEqual(func('klaʊ̯ə', diphtongs=True), ['k', 'l', 'aʊ̯', 'ə'])

	def test_tokenise_splits_words(self):
		"""
		Whitespace characters and underscores should serve as word boundaries,
		regardless of the flag values.
		"""
		for comb in product([True, False], [True, False], [True, False]):
			func = partial(tokenise,
					strict=comb[0], replace=comb[1], diphtongs=comb[2])

			self.assertEqual(func('prɤst na krak'), ['p', 'r', 'ɤ', 's', 't', 'n', 'a', 'k', 'r', 'a', 'k'])
			self.assertEqual(func('prɤst_na_krak'), ['p', 'r', 'ɤ', 's', 't', 'n', 'a', 'k', 'r', 'a', 'k'])

			self.assertEqual(func('etɬə tite'), ['e', 't', 'ɬ', 'ə', 't', 'i', 't', 'e'])
			self.assertEqual(func('etɬə_tite'), ['e', 't', 'ɬ', 'ə', 't', 'i', 't', 'e'])
