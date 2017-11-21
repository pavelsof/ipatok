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


def group(merge_func, tokens):
	"""
	"""
	output = []

	if tokens:
		output.append(tokens[0])

		for i in range(1, len(tokens)):
			prev_token, token = tokens[i-1], tokens[i]

			if merge_func(prev_token, token):
				output[-1] += token
			else:
				output.append(token)

	return output


def are_diphtong(tokenA, tokenB):
	"""
	Check whether the two tokens can form a diphtong.
	"""
	if ipa.is_vowel(tokenA[0]) and ipa.is_vowel(tokenB[0]):
		return any([char == '◌̯'[1] for char in tokenA+tokenB])

	return False


def tokenise_word(string, strict=False, replace=False):
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


def tokenise(string, strict=False, replace=False, diphtongs=False):
	"""
	"""
	words = string.strip().split()
	output = []

	for word in words:
		tokens = tokenise_word(word, strict=strict, replace=replace)
		if diphtongs:
			tokens = group(are_diphtong, tokens)

		output.extend(tokens)

	return output


"""
Provide for the alternative spelling.
"""
tokenize = tokenise
