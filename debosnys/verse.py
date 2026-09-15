"""Debosnys 'monographe verse' (c4a.png lines 1-15, c4b.png lines 16-20): the rhyme test.

Line-final glyphs, described in words (no transcription standard exists publicly), with the glyph
count of each line excluding punctuation, read at 3x (crops/verse_*.png). Counts carry about +-1 of
segmentation uncertainty; lines 11-13 are under a water stain.
"""
from math import comb

LINES = [  # (glyphs, final punctuation, final glyph)
    (12, ',', 'tilde-curl'), (13, '', 'tilde-curl'),
    (12, '-', 'dotted X'), (13, '-', 'dotted X'),
    (14, ',', 'Y with ring'), (14, '.', 'Y with ring'),
    (13, ',', 'barred o (triple bar over o)'), (13, ',', 'barred o (triple bar over o)'),
    (14, ',', 'venus sign'), (13, '.', 'venus sign'),
    (16, ',', 'delta'), (14, '.', 'delta'),
    (17, '', 'o with cross at lower right'), (17, '', 'o with cross above'),
    (14, '', 'dark note with arrow, two dots below'), (11, '', 'dark note with arrow, two dots below'),
    (15, '', 'tilde-curl'), (11, '.', 'tilde-curl'),
    (13, '', 'curly X'), (14, '', 'curly X'),
]


def main():
    same_in = sum(LINES[i][2] == LINES[i + 1][2] for i in range(0, 20, 2))
    same_across = sum(LINES[i][2] == LINES[i + 1][2] for i in range(1, 19, 2))
    print('identical final glyph within couplets (1-2, 3-4, ...): %d of 10' % same_in)
    print('identical final glyph across couplet boundaries (2-3, 4-5, ...): %d of 9' % same_across)
    for p in (0.05, 0.10, 0.20):
        tail = sum(comb(10, k) * p ** k * (1 - p) ** (10 - k) for k in range(same_in, 11))
        print('   P(>= %d of 10 by chance | match probability %.2f) = %.1e' % (same_in, p, tail))
    c = [n for n, _, _ in LINES]
    print('glyphs per line: %s  mean %.1f, range %d-%d' % (c, sum(c) / len(c), min(c), max(c)))
    print('final glyph of couplet 1 recurs at couplet 9:', LINES[0][2] == LINES[16][2])


if __name__ == '__main__':
    main()
