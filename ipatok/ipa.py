import functools
import os.path


"""
Path to the IPA data file, storing a list of all valid IPA symbols.
"""
IPA_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data/ipa.tsv')


class Chart:
	"""
	Object that loads and stores the valid IPA symbols.
	"""

	def __init__(self):
		"""
		Init the instance's properties. These are character sets, one for each
		class of IPA symbols.
		"""
		self.letters = set()
		self.non_letters = set()
		self.tie_bars = set()
		self.diacritics = set()
		self.lengths = set()
		self.suprasegmentals = set()

	def load(self, file_path):
		"""
		Populate the instance's properties using the specified file.
		"""
		sections = {
			'# letters': self.letters,
			'# non-standard letters': self.non_letters,
			'# tie bars': self.tie_bars,
			'# diacritics': self.diacritics,
			'# lengths': self.lengths,
			'# suprasegmentals': self.suprasegmentals }

		curr_section = None

		with open(file_path, encoding='utf-8') as f:
			for line in map(lambda x: x.strip(), f):
				if line.startswith('#'):
					assert line in sections
					curr_section = sections[line]
				elif line:
					assert curr_section is not None
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
	Check whether the given character is an IPA letter.
	"""
	if strict:
		return char in chart.letters
	else:
		return char in chart.letters or char in chart.non_letters


@ensure_single_char
def is_tie_bar(char):
	"""
	Check whether the given character is one of the two tie bar symbols.
	"""
	return char in chart.tie_bars


@ensure_single_char
def is_diacritic(char, strict=True):
	"""
	Check whether the given character is an IPA diacritic.
	"""
	return char in chart.diacritics


@ensure_single_char
def is_length(char):
	"""
	Check whether the given character is an IPA length marker.
	"""
	return char in chart.lengths


@ensure_single_char
def is_suprasegmental(char):
	"""
	Check whether the given character is an IPA suprasegmental.
	"""
	return char in chart.suprasegmentals


"""
Load the chart
"""
chart = Chart()
chart.load(IPA_DATA_PATH)
