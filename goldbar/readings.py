"""Letter counts and chi-squared for each defensible reading of the gold bar strings.

McCurley's 1996 transcription was checked letter for letter against his fifteen photographs on
2026-09-15 (seven of them carry Latin text). Fourteen of the sixteen strings match. Two do not:

  H  UGMNCBXCFLDBEY (14) is 13 letters on bars 5, 7 and 12. The glyph before the final Y reads E on
     bar 12 (the clearest) and bar 5, and could be read B on bar 7. McCurley evidently kept both.
  K  KOWVRSRKWTMLDH (14): the K after RSR is not visible on bars 5, 7 or 13, but the crops are too
     coarse to rule it out.

Run: python readings.py   (needs scipy)
"""
import collections
from corpus import CRYPTOGRAMS

AL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VARIANTS = [
    ('McCurley 1996 as published', {}),
    ('H = UGMNCBXCFLDEY', {'H': 'UGMNCBXCFLDEY'}),
    ('H = UGMNCBXCFLDBY', {'H': 'UGMNCBXCFLDBY'}),
    ('H = ..DEY, K = KOWVRSRWTMLDH', {'H': 'UGMNCBXCFLDEY', 'K': 'KOWVRSRWTMLDH'}),
    ('H = ..DBY, K = KOWVRSRWTMLDH', {'H': 'UGMNCBXCFLDBY', 'K': 'KOWVRSRWTMLDH'}),
]

def main():
    try:
        from scipy import stats
    except ImportError:
        stats = None
    base = dict(CRYPTOGRAMS)
    for name, change in VARIANTS:
        d = dict(base); d.update(change)
        s = ''.join(d[k] for k, _ in CRYPTOGRAMS)
        n = len(s); c = collections.Counter(s); exp = n / 26
        counts = [c[x] for x in AL]
        chi = sum((v - exp) ** 2 / exp for v in counts)
        dev = ' '.join('%s%+d' % (x, v - 10) for x, v in zip(AL, counts) if v != 10)
        p = ('  P=%.1e' % stats.chi2.cdf(chi, 25)) if stats else ''
        print('%-32s n=%d  exactly ten: %2d/26  off: %-28s chi2=%.3f%s'
              % (name, n, sum(1 for v in counts if v == 10), dev, chi, p))

if __name__ == '__main__':
    main()
