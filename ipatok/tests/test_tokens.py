from unittest import TestCase

from ipatok.tokens import tokenise



class TokensTestCase(TestCase):
	"""
	The IPA strings are sourced from NorthEuraLex (bul, eng, ava).
	"""

	def test_tokenise(self):
		self.assertEqual(tokenise('lit͡sɛ'), ['l', 'i', 't͡s', 'ɛ'])
		self.assertEqual(tokenise('t͡ʃɛʎust'), ['t͡ʃ', 'ɛ', 'ʎ', 'u', 's', 't'])
		self.assertEqual(tokenise('dirʲa'), ['d', 'i', 'rʲ', 'a'])
		self.assertEqual(tokenise('ut͡ʃa sɛ'), ['u', 't͡ʃ', 'a', 's', 'ɛ'])

		self.assertEqual(tokenise('ˈd͡ʒɔɪ'), ['d͡ʒ', 'ɔ', 'ɪ'])
		self.assertEqual(tokenise('ˈtiːt͡ʃə'), ['t', 'iː', 't͡ʃ', 'ə'])
		self.assertEqual(tokenise('t͡ʃuːz'), ['t͡ʃ', 'uː', 'z'])

		self.assertEqual(tokenise('miq͡χː'), ['m', 'i', 'q͡χː'])
		self.assertEqual(tokenise('ʃːjeq͡χːʼjer'), ['ʃː', 'j', 'e', 'q͡χːʼ', 'j', 'e', 'r'])
		self.assertEqual(tokenise('t͡ɬʼibil'), ['t͡ɬʼ', 'i', 'b', 'i', 'l'])
		self.assertEqual(tokenise('ɬalkʼ'), ['ɬ', 'a', 'l', 'kʼ'])

	def test_tokenise_strictness(self):
		with self.assertRaises(ValueError):
			tokenise('t͡ʃɛɫɔ', strict=True)

		self.assertEqual(tokenise('t͡ʃɛɫɔ', strict=False), ['t͡ʃ', 'ɛ', 'ɫ', 'ɔ'])
