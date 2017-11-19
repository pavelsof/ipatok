from unittest import TestCase

from ipatok.tokens import tokenise



class TokensTestCase(TestCase):

	def test_tokenise(self):
		self.assertEqual(tokenise('lit͡sɛ'), ['l', 'i', 't͡s', 'ɛ'])
		self.assertEqual(tokenise('t͡ʃɛʎust'), ['t͡ʃ', 'ɛ', 'ʎ', 'u', 's', 't'])

		self.assertEqual(tokenise('ˈd͡ʒɔɪ'), ['d͡ʒ', 'ɔ', 'ɪ'])
		self.assertEqual(tokenise('ˈtiːt͡ʃə'), ['t', 'iː', 't͡ʃ', 'ə'])
		self.assertEqual(tokenise('t͡ʃuːz'), ['t͡ʃ', 'uː', 'z'])

	def test_tokenise_strictness(self):
		with self.assertRaises(ValueError):
			tokenise('t͡ʃɛɫɔ', strict=True)

		self.assertEqual(tokenise('t͡ʃɛɫɔ', strict=False), ['t͡ʃ', 'ɛ', 'ɫ', 'ɔ'])
