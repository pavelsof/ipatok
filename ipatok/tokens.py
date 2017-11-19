import unicodedata

from ipatok import ipa



def tokenise(string, strict=True):
	"""
	Tokenises the given IPA string into a list of tokens. Raise ValueError if
	the argument is not a valid IPA string.
	"""
	string = ''.join(string.strip().split())
	string = unicodedata.normalize('NFD', string)

	tokens = []

	for index, char in enumerate(string):
		if ipa.is_letter(char, strict):
			if tokens and ipa.is_tie_bar(string[index-1]):
				tokens[-1] += char
			else:
				tokens.append(char)

		elif ipa.is_diacritic(char) or ipa.is_length(char):
			if not tokens:
				raise ValueError('The string starts with a diacritic')
			tokens[-1] += char

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
