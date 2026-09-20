"""The Barberini-Ceva cipher of ASV SdS Francia 346 (1632-34).

System, as reconstructed by George Lasry (DECODE, 24 Oct 2020) and checked
here against his aligned decipherments of 346:1, 346/4, 346/5 and 346/9:

  6         word separator
  2x        null (no 2x pair is used for plaintext)
  XY        homophone / syllable, from KEY below
  pXY       nomenclator element: one prefix digit + a 2-digit code.
            Lasry's note names prefix 4; in his own readings the prefix is
            also 0, 1, 3, 5, 7, 8 or 9. None of the 95 he marked was solved.
"""

KEY = {}
for codes, val in [
    ('19|38|47', 'a'), ('73', 'al'), ('08|79', 'b'), ('10|71', 'c'),
    ('44', 'che'), ('55', 'chi'), ('00', 'con'), ('09|48', 'd'),
    ('74', 'da'), ('77', 'de'), ('84', 'di'), ('18|37|45', 'e'),
    ('97', 'et'), ('51|80', 'f'), ('91', 'g'), ('07', 'h'),
    ('17|35|41', 'i'), ('53', 'il'), ('34', 'in'), ('54', 'io'),
    ('57|90', 'l'), ('83', 'la'), ('01|78', 'm'), ('93', 'ma'),
    ('14', 'mi'), ('30|81', 'n'), ('11', 'no'), ('15|31|39', 'o'),
    ('04|58', 'p'), ('13', 'per'), ('89', 'qu'), ('88', 'quel'),
    ('59|70', 'r'), ('03|87', 's'), ('94', 'se'), ('95', 'si'),
    ('43', 'st'), ('40|85', 't'), ('49|75|98', 'v'), ('50', 'z'),
]:
    for c in codes.split('|'):
        KEY[c] = val

SEP = '6'
NULLS = {'2%d' % d for d in range(10)}

def is_null(t):
    return t in NULLS

def units(t):
    """Plaintext of a token, or None if it is not a plain 2-digit code."""
    return KEY.get(t)


# Nomenclator elements read here off the 1632 interlinear decipherment of R75
# and confirmed against Lasry's four letters.  He left all 95 unsolved.
NOMEN = {
    '474': 'mente',    # piena~, principal~, non sola~, malacomoda~
    '495': 'quanto',   # "e ~ al proporre arbitrare"; pairs with 498
    '498': 'tanto',    # "che ~ in <347> quanto in <857> si sappia la cagione"
    '830': 'francia',  # always after a feminine article: "render la ~ piu poderosa"
    '854': 'guerra',   # R75 interlinear, twice
    '149': 'piazza',   # R75 interlinear, "acquisto d'una ~"
}
