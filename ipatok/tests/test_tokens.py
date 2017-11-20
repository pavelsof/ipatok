from functools import partial
from unittest import TestCase

from ipatok.tokens import normalise, tokenise



class TokensTestCase(TestCase):
	"""
	The IPA strings are sourced from NorthEuraLex (languages: ady, ava, bul,
	ckt, deu, eng).
	"""

	def test_normalise(self):
		self.assertEqual(normalise('nɪçt'), 'nɪçt')  # ç in normal form C
		self.assertEqual(normalise('nɪçt'), 'nɪçt')  # ç in normal form D

	def test_tokenise(self):
		for strict in [True, False]:
			func = partial(tokenise, strict=strict)

			self.assertEqual(func('miq͡χː'), ['m', 'i', 'q͡χː'])
			self.assertEqual(func('ʃːjeq͡χːʼjer'), ['ʃː', 'j', 'e', 'q͡χːʼ', 'j', 'e', 'r'])
			self.assertEqual(func('t͡ɬʼibil'), ['t͡ɬʼ', 'i', 'b', 'i', 'l'])
			self.assertEqual(func('ɬalkʼ'), ['ɬ', 'a', 'l', 'kʼ'])

			self.assertEqual(func('lit͡sɛ'), ['l', 'i', 't͡s', 'ɛ'])
			self.assertEqual(func('t͡ʃɛʎust'), ['t͡ʃ', 'ɛ', 'ʎ', 'u', 's', 't'])
			self.assertEqual(func('dirʲa'), ['d', 'i', 'rʲ', 'a'])
			self.assertEqual(func('ut͡ʃa sɛ'), ['u', 't͡ʃ', 'a', 's', 'ɛ'])

			self.assertEqual(func('nɪçt'), ['n', 'ɪ', 'ç', 't'])
			self.assertEqual(func('t͡saɪ̯çən'), ['t͡s', 'a', 'ɪ̯', 'ç', 'ə', 'n'])

			self.assertEqual(func('ˈd͡ʒɔɪ'), ['d͡ʒ', 'ɔ', 'ɪ'])
			self.assertEqual(func('ˈtiːt͡ʃə'), ['t', 'iː', 't͡ʃ', 'ə'])
			self.assertEqual(func('t͡ʃuːz'), ['t͡ʃ', 'uː', 'z'])

	def test_tokenise_non_ipa(self):
		with self.assertRaises(ValueError):
			tokenise('ʷəˈʁʷa', strict=True)
		self.assertEqual(tokenise('ʷəˈʁʷa', strict=False), ['ʷ', 'ə', 'ʁʷ', 'a'])

		with self.assertRaises(ValueError):
			tokenise('t͡ʃɛɫɔ', strict=True)
		self.assertEqual(tokenise('t͡ʃɛɫɔ', strict=False), ['t͡ʃ', 'ɛ', 'ɫ', 'ɔ'])

		with self.assertRaises(ValueError):
			tokenise('t͡ɕˀet͡ɕeŋ', strict=True)
		self.assertEqual(tokenise('t͡ɕˀet͡ɕeŋ', strict=False), ['t͡ɕˀ', 'e', 't͡ɕ', 'e', 'ŋ'])

		with self.assertRaises(ValueError):
			tokenise('kat͡ɕˀaɹ', strict=True)
		self.assertEqual(tokenise('kat͡ɕˀaɹ', strict=False), ['k', 'a', 't͡ɕˀ', 'a', 'ɹ'])
