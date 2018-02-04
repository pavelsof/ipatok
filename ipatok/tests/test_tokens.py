from functools import partial
from itertools import product
from unittest import TestCase

from ipatok.tokens import (
		normalise, group, are_diphtong, tokenise, replace_digits_with_chao)



class TokensTestCase(TestCase):
	"""
	The IPA strings are sourced from NorthEuraLex (languages: ady, ava, bul,
	ckt, cmn, deu, eng).
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
		for comb in product(*[[True, False]] * 5):
			func = partial(tokenise, strict=comb[0], replace=comb[1],
							diphtongs=comb[2], tones=comb[3], unknown=comb[4])

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
		for comb in product(*[[True, False]] * 4):
			func = partial(tokenise, replace=comb[0],
							diphtongs=comb[1], tones=comb[2], unknown=comb[3])

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
		for comb in product(*[[True, False]] * 3):
			func = partial(tokenise, strict=True,
							diphtongs=comb[0], tones=comb[1], unknown=comb[2])

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
		for comb in product(*[[True, False]] * 4):
			func = partial(tokenise, strict=comb[0],
							replace=comb[1], tones=comb[2], unknown=comb[3])

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

	def test_tokenise_tones(self):
		"""
		Tones in IPA-compliant strings should be tokenised or ignored depending
		on the tones flag, regardless of other flags' values.
		"""
		for comb in product(*[[True, False]] * 4):
			func = partial(tokenise, strict=comb[0],
							replace=comb[1], diphtongs=comb[2], unknown=comb[3])

			self.assertEqual(func('t͡sɯ˦ɕy˦', tones=True), ['t͡s', 'ɯ', '˦', 'ɕ', 'y', '˦'])
			self.assertEqual(func('t͡sɯ˦ɕy˦', tones=False), ['t͡s', 'ɯ', 'ɕ', 'y'])

			self.assertEqual(func('˨˩˦', tones=True), ['˨˩˦'])
			self.assertEqual(func('˨˩˦', tones=False), [])

			self.assertEqual(func('ə̋ə̏', tones=True), ['ə̋', 'ə̏'])
			self.assertEqual(func('ə̋ə̏', tones=False), ['ə', 'ə'])

	def test_tokenise_tones_non_ipa(self):
		"""
		Modifier tone letters should raise ValueError unless strict is False,
		and should be otherwise tokenised only if tones is True.
		"""
		for comb in product(*[[True, False]] * 3):
			func = partial(tokenise,
							replace=comb[0], diphtongs=comb[1], unknown=comb[2])

			for tones in [True, False]:
				with self.assertRaises(ValueError):
					func('꜍꜈', strict=True, tones=tones)

			self.assertEqual(func('꜍꜈', strict=False, tones=False), [])
			self.assertEqual(func('꜍꜈', strict=False, tones=True), ['꜍꜈'])

	def test_tokenise_unknown(self):
		"""
		Unknown symbols should raise ValueError unless strict is False, in
		which case they should be ignored depending on the unknown flag.
		"""
		for comb in product(*[[True, False]] * 3):
			func = partial(tokenise, replace=comb[0], diphtongs=comb[1], tones=comb[2])

			for unknown in [True, False]:
				with self.assertRaises(ValueError):
					func('-/$', strict=True, unknown=unknown)

			self.assertEqual(func('-/$', unknown=True), ['-', '/', '$'])
			self.assertEqual(func('-/$', unknown=False), [])

	def test_tokenise_splits_words(self):
		"""
		Whitespace characters and underscores should serve as word boundaries,
		regardless of the flag values.
		"""
		for comb in product(*[[True, False]] * 5):
			func = partial(tokenise, strict=comb[0], replace=comb[1],
							diphtongs=comb[2], tones=comb[3], unknown=comb[4])

			self.assertEqual(func('prɤst na krak'), ['p', 'r', 'ɤ', 's', 't', 'n', 'a', 'k', 'r', 'a', 'k'])
			self.assertEqual(func('prɤst_na_krak'), ['p', 'r', 'ɤ', 's', 't', 'n', 'a', 'k', 'r', 'a', 'k'])

			self.assertEqual(func('etɬə tite'), ['e', 't', 'ɬ', 'ə', 't', 'i', 't', 'e'])
			self.assertEqual(func('etɬə_tite'), ['e', 't', 'ɬ', 'ə', 't', 'i', 't', 'e'])

	def test_replace_digits_with_chao(self):
		"""
		Digits should be correctly replaced with Chao tone letters, regardless
		of the flag value and whether superscript or not.
		"""
		self.assertEqual(replace_digits_with_chao('ɕiŋ⁵⁵ɕiŋ²'), 'ɕiŋ˥ɕiŋ˨')
		self.assertEqual(replace_digits_with_chao('ɕiŋ55ɕiŋ2'), 'ɕiŋ˥ɕiŋ˨')

		self.assertEqual(replace_digits_with_chao('ɕia⁵¹ɕyɛ²¹⁴'), 'ɕia˥˩ɕyɛ˨˩˦')
		self.assertEqual(replace_digits_with_chao('ɕia51ɕyɛ214'), 'ɕia˥˩ɕyɛ˨˩˦')

		self.assertEqual(replace_digits_with_chao('ɕiŋ⁵⁵ɕiŋ²', inverse=True), 'ɕiŋ˩ɕiŋ˦')
		self.assertEqual(replace_digits_with_chao('ɕiŋ55ɕiŋ2', inverse=True), 'ɕiŋ˩ɕiŋ˦')

		self.assertEqual(replace_digits_with_chao('ɕia⁵¹ɕyɛ²¹⁴', inverse=True), 'ɕia˩˥ɕyɛ˦˥˨')
		self.assertEqual(replace_digits_with_chao('ɕia51ɕyɛ214', inverse=True), 'ɕia˩˥ɕyɛ˦˥˨')
