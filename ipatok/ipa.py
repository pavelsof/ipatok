import functools
import os.path
import unicodedata


"""
Paths to the ipatok/data dir and the two files in there.
"""
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

IPA_CHART_PATH = os.path.join(DATA_DIR, 'ipa_2015.tsv')
REPLACEMENTS_PATH = os.path.join(DATA_DIR, 'replacements.tsv')


class Chart:
    """
    Object that loads and stores the valid IPA symbols.
    """

    def __init__(self):
        """
        Init the instance's properties. All of these but the last one are
        character sets, as needed by the is_ functions that comprise the
        module's api. The last one is a dict mapping common substitutes to
        their respective IPA counterparts.
        """
        self.consonants = set()
        self.vowels = set()
        self.tie_bars = set()
        self.diacritics = set()
        self.suprasegmentals = set()
        self.lengths = set()
        self.tones = set()

        self.replacements = {}

    def load_ipa(self, file_path):
        """
        Populate the instance's set properties using the specified file.
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
            '# tones and word accents': self.tones,
        }

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

    def load_replacements(self, file_path):
        """
        Populate self.replacements using the specified file.
        """
        with open(file_path, encoding='utf-8') as f:
            for line in map(lambda x: x.strip(), f):
                if line:
                    line = line.split('\t')
                    self.replacements[line[0]] = line[1]


def ensure_single_char(func):
    """
    Decorator that ensures that the first argument of the decorated function is
    a single character, i.e. a string of length one.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not isinstance(args[0], str) or len(args[0]) != 1:
            raise ValueError(
                'This function should be invoked with a string of length one '
                'as its first argument'
            )

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
        return unicodedata.category(char) in ['Ll', 'Lo', 'Lt', 'Lu']

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
        return (
            unicodedata.category(char) in ['Lm', 'Mn', 'Sk']
            and not is_suprasegmental(char)
            and not is_tie_bar(char)
            and not 0xA700 <= ord(char) <= 0xA71F
        )

    return False


@ensure_single_char
def is_suprasegmental(char, strict=True):
    """
    Check whether the character is a suprasegmental according to the IPA spec.
    This includes tones, word accents, and length markers.

    In strict mode return True only if the diacritic is part of the IPA spec.
    """
    if (char in chart.suprasegmentals) or (char in chart.lengths):
        return True

    return is_tone(char, strict)


@ensure_single_char
def is_length(char):
    """
    Check whether the character is a length marker. Unlike other
    suprasegmentals, length markers are included in the tokenised output.
    """
    return char in chart.lengths


@ensure_single_char
def is_tone(char, strict=True):
    """
    Check whether the character is a tone or word accent symbol. In strict mode
    return True only for the symbols listed in the last group of the chart. If
    strict=False, also accept symbols that belong to the Modifier Tone Letters
    Unicode block [1].

    [1]: http://www.unicode.org/charts/PDF/UA700.pdf
    """
    if char in chart.tones:
        return True

    if not strict:
        return 0xA700 <= ord(char) <= 0xA71F

    return False


def get_precomposed_chars():
    """
    Return the set of IPA characters that are defined in normal form C in the
    spec. As of 2015, this is only the voiceless palatal fricative, ç.
    """
    return set(
        letter
        for letter in chart.consonants
        if unicodedata.normalize('NFD', letter) != letter
    )


def replace_substitutes(string):
    """
    Return the given string with all known common substitutes replaced with
    their IPA-compliant counterparts.
    """
    for non_ipa, ipa in chart.replacements.items():
        string = string.replace(non_ipa, ipa)

    return string


"""
Load the chart.
"""
chart = Chart()
chart.load_ipa(IPA_CHART_PATH)
chart.load_replacements(REPLACEMENTS_PATH)
