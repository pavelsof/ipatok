import unicodedata

from ipatok.ipa import is_letter, is_tie_bar, is_diacritic, is_suprasegmental



def tokenise(string, strict=True):
	"""
	Tokenises the given IPA string into a list of tokens. Raise ValueError if
	the argument is not a valid IPA string.
	"""
	string = unicodedata.normalize('NFD', string)
	tokens = []

	for index, char in enumerate(string):
		if is_letter(char, strict):
			if tokens and is_tie_bar(string[index-1]):
				tokens[-1] += char
			else:
				tokens.append(char)

		elif is_diacritic(char):
			if not tokens:
				raise ValueError('The string starts with a diacritic')
			tokens[-1] += char

		elif is_suprasegmental(char):
			pass

		elif is_tie_bar(char):
			if not tokens:
				raise ValueError('The string starts with a tie bar')
			tokens[-1] += char

		else:
			raise ValueError('Unrecognised char: {}'.format(char))

	return tokens



"""
Provide for the alternative spelling.
"""
tokenize = tokenise
