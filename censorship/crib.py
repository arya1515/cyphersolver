"""Predicted Morse mark sequences for Illustration No. 14 (the Amsterdam map) of the WW2 censorship manual.

The manual (TNA KV 2/2424, p. 17) states: "The morse letters had to be transposed 11 positions forward", and
gives only an English translation: "Oil has arrived, everything is ready. Gustav available for the appointed day."

Direction check against the one published fragment (reader 'm', klausschmeh blog, 15 Oct 2016): marks read
as AATHUT, shifted +11, give LLESFE - part of ALLES FERTIG. So the map carries plaintext shifted -11, and a
reader decodes Morse then shifts +11. This script produces, for candidate German wordings, the exact sequence
of dots and dashes a reader should find, with mark counts, so a reading of the original can be tested
against it mark by mark.

Usage: python crib.py
"""
MORSE = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 'g': '--.', 'h': '....', 'i': '..',
         'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
         's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-', 'y': '-.--', 'z': '--..'}

CANDIDATES = [
    'oel ist angekommen alles fertig gustav fuer den bestimmten tag verfuegbar',
    'oel angekommen alles fertig gustav am bestimmten tage bereit',
    'oel eingetroffen alles bereit gustav fuer den festgesetzten tag verfuegbar',
    'oel ist eingetroffen alles ist fertig gustav steht fuer den verabredeten tag zur verfuegung',
]


def enc(plain, k=-11):
    out = []
    for w in plain.split():
        letters = [chr((ord(c) - 97 + k) % 26 + 97) for c in w if c.isalpha()]
        out.append(letters)
    return out


def main():
    frag = 'aathut'
    print('check: fragment %s shifted +11 = %s' % (frag, ''.join(chr((ord(c) - 97 + 11) % 26 + 97) for c in frag)))
    for c in CANDIDATES:
        words = enc(c)
        marks = sum(len(MORSE[l]) for w in words for l in w)
        dashes = sum(MORSE[l].count('-') for w in words for l in w)
        print('\n%s' % c)
        print('   carried letters: %s' % ' '.join(''.join(w) for w in words))
        print('   %d letters, %d marks (%d dashes, %d dots)' % (sum(len(w) for w in words), marks, dashes, marks - dashes))
        print('   ' + ' / '.join(' '.join(MORSE[l] for l in w) for w in words))
    w = enc('alles fertig')[0] + enc('alles fertig')[1]
    print('\nthe stretch read in 2016, ALLES FERTIG: %s = %s' % (''.join(w), ' '.join(MORSE[l] for l in w)))


if __name__ == '__main__':
    main()
