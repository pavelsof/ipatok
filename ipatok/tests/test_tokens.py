from unittest import TestCase

from ipatok.tokens import tokenise



class TokensTestCase(TestCase):

	def test_tokenise(self):
		self.assertEqual(tokenise('lit͡sɛ'), ['l', 'i', 't͡s', 'ɛ'])
		# self.assertEqual(tokenise('t͡ʃɛɫɔ'), ['t͡s', 'ɛ', 'ɫ', 'ɔ'])
		self.assertEqual(tokenise('t͡ʃɛʎust'), ['t͡ʃ', 'ɛ', 'ʎ', 'u', 's', 't'])

		self.assertEqual(tokenise('ˈd͡ʒɔɪ'), ['d͡ʒ', 'ɔ', 'ɪ'])
		self.assertEqual(tokenise('ˈtiːt͡ʃə'), ['t', 'iː', 't͡ʃ', 'ə'])
		self.assertEqual(tokenise('t͡ʃuːz'), ['t͡ʃ', 'uː', 'z'])
