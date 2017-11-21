import functools
import os.path
import unicodedata


"""
Path to the IPA data file, storing a list of all valid IPA symbols.
"""
IPA_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data/ipa_2015.tsv')


class Chart:
	"""
	Object that loads and stores the valid IPA symbols.
	"""

	def __init__(self):
		"""
		Init the instance's properties. These are character sets, as needed by
		the is_ functions that comprise the module's api.
		"""
		self.consonants = set()
		self.vowels = set()
		self.tie_bars = set()
		self.diacritics = set()
		self.suprasegmentals = set()
		self.lengths = set()

	def load(self, file_path):
		"""
		Populate the instance's properties using the specified file.
		"""
		sections = {
			'# consonants (pulmonic)': self.consonants,
			'# consonants (non-pulmonic)': self.consonants,
			'# other symbols': self.consonants,
			'# tie bars': self.tie_bars,
			'# vowels': self.vowels,
			'# diacritics': self.diacritics,
			'# suprasegmentals': self.suprasegmentals,
			'# lengths': self.lengths,
			'# tones and word accents': self.suprasegmentals }

		curr_section = None

		with open(file_path, encoding='utf-8') as f:
			for line in map(lambda x: x.strip(), f):
				if line.startswith('#'):
					if line in sections:
						curr_section = sections[line]
					else:
						curr_section = None
				elif line:
					if curr_section is not None:
						curr_section.add(line.split('\t')[0])


def ensure_single_char(func):
	"""
	Decorator that ensures that the first argument of the decorated function is
	a single character, i.e. a string of length one.
	"""
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		if not isinstance(args[0], str) or len(args[0]) != 1:
			raise ValueError((
				'This function should be invoked with a string of length one '
				'as its first argument'))
		return func(*args, **kwargs)

	return wrapper


@ensure_single_char
def is_letter(char, strict=True):
	"""
	Check whether the character is a letter (as opposed to a diacritic or
	suprasegmental).

	In strict mode return True only if the letter is part of the IPA spec.
	"""
	if (char in chart.consonants) or (char in chart.vowels):
		return True

	if not strict:
		return unicodedata.category(char) in ['Ll', 'Lo']

	return False


@ensure_single_char
def is_vowel(char):
	"""
	Check whether the character is a vowel letter.
	"""
	if is_letter(char, strict=True):
		return char in chart.vowels

	return False


@ensure_single_char
def is_tie_bar(char):
	"""
	Check whether the character is one of the two IPA tie bar symbols.
	"""
	return char in chart.tie_bars


@ensure_single_char
def is_diacritic(char, strict=True):
	"""
	Check whether the character is a diacritic (as opposed to a letter or a
	suprasegmental).

	In strict mode return True only if the diacritic is part of the IPA spec.
	"""
	if char in chart.diacritics:
		return True

	if not strict:
		return (not is_suprasegmental(char)) and \
				(unicodedata.category(char) in ['Lm', 'Mn', 'Sk'])

	return False


@ensure_single_char
def is_suprasegmental(char):
	"""
	Check whether the character is a suprasegmental according to the IPA spec.
	This includes tones, word accents, and length markers.
	"""
	return (char in chart.suprasegmentals) or (char in chart.lengths)


@ensure_single_char
def is_length(char):
	"""
	Check whether the character is a length marker. Unlike other
	suprasegmentals, length markers are included in the tokenised output.
	"""
	return char in chart.lengths


def get_precomposed_chars():
	"""
	Return the set of IPA characters that are defined in normal form C in the
	spec. As of 2015, this is only the voiceless palatal fricative, ç.
	"""
	return set([
		letter for letter in chart.consonants
		if unicodedata.normalize('NFD', letter) != letter ])


"""
Load the chart
"""
chart = Chart()
chart.load(IPA_DATA_PATH)
