import re

TRIPLE = re.compile(r'(.)\1\1')
BADRUN = re.compile(r'[aeiouy]{4}|[^aeiouy]{5}')
ROMAN = re.compile(r'[ivxlcdmj]+')


def clean(s):
    """Lower-case a-z text from an OCR'd Scots edition, with the OCR noise and Roman numerals dropped.

    Tokens removed: pure Roman numerals (xviij, iiij ...), tokens with a tripled letter, 'ii' (OCR for n/u),
    any 'j', implausible vowel/consonant runs, and tokens of 20+ letters.
    """
    s = s.lower().replace('æ', 'ae')
    s = re.sub(r'[^a-z]+', ' ', s)
    toks = [w for w in s.split()
            if not ROMAN.fullmatch(w) and not TRIPLE.search(w) and len(w) < 20
            and 'ii' not in w and 'j' not in w and not BADRUN.search(w)]
    return ' '.join(toks)
