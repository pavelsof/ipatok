from unittest import TestCase

from ipatok.tokens import tokenise



class TokensTestCase(TestCase):

	def test_tokenise(self):
		self.assertEqual(tokenise('lit͡sɛ'), ['l', 'i', 't͡s', 'ɛ'])
		# self.assertEqual(tokenise('t͡ʃɛɫɔ'), ['t͡s', 'ɛ', 'ɫ', 'ɔ'])
		self.assertEqual(tokenise('t͡ʃɛʎust'), ['t͡ʃ', 'ɛ', 'ʎ', 'u', 's', 't'])
