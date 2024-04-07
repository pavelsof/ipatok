import unicodedata

from ipatok import ipa


def normalise(string):
    """
    Convert each character of the string to the normal form in which it was
    defined in the IPA spec. This would be normal form D, except for the
    voiceless palatar fricative (ç) which should be in normal form C.

    Helper for tokenise_word(string, ..).
    """
    string = unicodedata.normalize('NFD', string)

    for char_c in ipa.get_precomposed_chars():
        char_d = unicodedata.normalize('NFD', char_c)
        if char_d in string:
            string = string.replace(char_d, char_c)

    return string


def group(merge_func, tokens):
    """
    Group together those of the tokens for which the merge function returns
    true. The merge function should accept two arguments/tokens and should
    return a boolean indicating whether the strings should be merged or not.

    Helper for tokenise(string, ..).
    """
    output = []

    if tokens:
        output.append(tokens[0])

        for token in tokens[1:]:
            prev_token = output[-1]

            if merge_func(prev_token, token):
                output[-1] += token
            else:
                output.append(token)

    return output


def are_diphthong(tokenA, tokenB):
    """
    Check (naively) whether the two tokens can form a diphthong. This would be
    a sequence of vowels of which no more than one is syllabic. Vowel sequences
    connected with a tie bar would already be handled in tokenise_word, so are
    not checked for here.

    Users who want more sophisticated diphthong detection should instead write
    their own function and do something like::

        tokenise(string, diphthong=False, merge=user_func)

    Helper for tokenise(string, ..).
    """

    def is_short(token):
        return '◌̯'[1] in token

    subtokens = []

    for char in tokenA + tokenB:
        if ipa.is_vowel(char):
            subtokens.append(char)
        elif ipa.is_diacritic(char) or ipa.is_length(char):
            if subtokens:
                subtokens[-1] += char
            else:
                break
        else:
            break
    else:
        if len([x for x in subtokens if not is_short(x)]) < 2:
            return True

    return False


def tokenise_word(
    string, strict=False, replace=False, tones=False, unknown=False
):
    """
    Tokenise the string into a list of tokens or raise ValueError if it cannot
    be tokenised (relatively) unambiguously. The string should not include
    whitespace, i.e. it is assumed to be a single word.

    If strict=False, allow non-standard letters and diacritics, as well as
    initial diacritic-only tokens (e.g. pre-aspiration). If replace=True,
    replace some common non-IPA symbols with their IPA counterparts. If
    tones=False, ignore tone symbols. If unknown=False, ignore symbols that
    cannot be classified into a relevant category.

    Helper for tokenise(string, ..).
    """
    string = normalise(string)

    if replace:
        string = ipa.replace_substitutes(string)

    tokens = []

    for index, char in enumerate(string):
        if ipa.is_letter(char, strict):
            if tokens and ipa.is_tie_bar(string[index - 1]):
                tokens[-1] += char
            else:
                tokens.append(char)

        elif ipa.is_tie_bar(char):
            if not tokens:
                raise ValueError(f'The string starts with a tie bar: {string}')
            tokens[-1] += char

        elif ipa.is_diacritic(char, strict) or ipa.is_length(char):
            if tokens:
                tokens[-1] += char
            else:
                if strict:
                    raise ValueError(
                        f'The string starts with a diacritic: {string}'
                    )
                else:
                    tokens.append(char)

        elif tones and ipa.is_tone(char, strict):
            if unicodedata.combining(char):
                if not tokens:
                    raise ValueError(
                        f'The string starts with an accent mark: {string}'
                    )
                tokens[-1] += char
            elif tokens and ipa.is_tone(tokens[-1][-1], strict):
                tokens[-1] += char
            else:
                tokens.append(char)

        elif ipa.is_suprasegmental(char, strict):
            pass

        else:
            if strict:
                raise ValueError(
                    f'Unrecognised char: {char} ({ unicodedata.name(char)})'
                )
            elif unknown:
                tokens.append(char)
            else:
                pass

    return tokens


def tokenise(
    string,
    strict=False,
    replace=False,
    diphthongs=False,
    tones=False,
    unknown=False,
    merge=None,
):
    """
    Tokenise an IPA string into a list of tokens. Raise ValueError if there is
    a problem; if strict=True, this includes the string not being compliant to
    the IPA spec.

    If replace=True, replace some common non-IPA symbols with their IPA
    counterparts. If diphthongs=True, try to group diphthongs into single
    tokens. If tones=True, do not ignore tone symbols. If unknown=True, do not
    ignore symbols that cannot be classified into a relevant category. If merge
    is not None, use it for within-word token grouping.

    Part of ipatok's public API.
    """
    words = string.strip().split()
    output = []

    for word in words:
        tokens = tokenise_word(word, strict, replace, tones, unknown)

        if diphthongs:
            tokens = group(are_diphthong, tokens)

        if merge is not None:
            tokens = group(merge, tokens)

        output.extend(tokens)

    return output


def clusterise(
    string,
    strict=False,
    replace=False,
    diphthongs=False,
    tones=False,
    unknown=False,
    merge=None,
):
    """
    Tokenise an IPA string and return a list of consonant and vowel clusters.
    Raise ValueError if there is a problem.

    Forward the keyword arguments to tokenise.

    Part of ipatok's public API.
    """

    def groupit(ipalist):
        """Merge subsequent consonants and vowels to clusters."""
        tmp = []
        it = iter(ipalist)
        nextit = next(it)
        for char in ipalist:
            charcv = any(ipa.is_vowel(i) for i in char)
            while any(ipa.is_vowel(i) for i in nextit) != charcv:
                yield ''.join(tmp)
                tmp = []
                nextit = next(it)
            tmp.append(char)
        yield ''.join(tmp)

    args = list(locals().values())[:-1]  # last arg would be groupit()
    return [i for i in groupit(tokenise(*args)) if i]


def replace_digits_with_chao(string, inverse=False):
    """
    Replace the digits 1-5 (also in superscript) with Chao tone letters. Equal
    consecutive digits are collapsed into a single Chao letter.

    If inverse=True, smaller digits are converted into higher tones; otherwise,
    they are converted into lower tones (the default).

    Part of ipatok's public API.
    """
    chao_letters = '˩˨˧˦˥'

    if inverse:
        chao_letters = chao_letters[::-1]

    string = string.translate(str.maketrans('¹²³⁴⁵', '12345'))
    string = string.translate(str.maketrans('12345', chao_letters))

    string = ''.join(
        char
        for index, char in enumerate(string)
        if not (index and char in chao_letters and string[index - 1] == char)
    )

    return string


"""
Provide for the alternative spellings.
"""
tokenize = tokenise
clusterize = clusterise
