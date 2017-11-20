import unicodedata

from ipatok import ipa



def normalise(string):
	"""
	Normalise the string by removing the whitespace and convert the characters
	to Unicode's normal form NFD except for those that are pre-composed in IPA.
	"""
	string = ''.join(string.strip().split())
	string = unicodedata.normalize('NFD', string)

	for char_c in ipa.get_precomposed_chars():
		char_d = unicodedata.normalize('NFD', char_c)
		if char_d in string:
			string = string.replace(char_d, char_c)

	return string



def tokenise(string, strict=True):
	"""
	Tokenise the given IPA string into a list of tokens or raise ValueError if
	the argument cannot be tokenised (relatively) unambiguously.

	If the strict flag is set to False, then allow non-standard letters and
	diacritics, as well as initial diacritic-only tokens (e.g. pre-aspiration).
	"""
	string = normalise(string)
	tokens = []

	for index, char in enumerate(string):
		if ipa.is_letter(char, strict):
			if tokens and ipa.is_tie_bar(string[index-1]):
				tokens[-1] += char
			else:
				tokens.append(char)

		elif ipa.is_diacritic(char, strict) or ipa.is_length(char):
			if tokens:
				tokens[-1] += char
			else:
				if strict:
					raise ValueError('The string starts with a diacritic')
				else:
					tokens.append(char)

		elif ipa.is_suprasegmental(char):
			pass

		elif ipa.is_tie_bar(char):
			if not tokens:
				raise ValueError('The string starts with a tie bar')
			tokens[-1] += char

		else:
			raise ValueError('Unrecognised char: {} ({})'.format(char, unicodedata.name(char)))

	return tokens



"""
Provide for the alternative spelling.
"""
tokenize = tokenise
