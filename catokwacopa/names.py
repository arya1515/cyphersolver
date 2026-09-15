"""How specific are the name cribs? Substitute every name-like word into each published frame and
count those that fit exactly (0 misprints) with no more omissions than the published name.

Name list: words that occur capitalised mid-sentence in the 24-novel corpus at least 3 times and
almost never in lower case (about a thousand names and proper nouns), plus the published names.
"""
import collections, glob, os, re
import mech
from ads import PAIRS

FRAMES = [
    (8, 'I ATTENDED {} LECSURS', 'CONINGTON'),
    (25, 'I ATTENDED {} LECSURS', 'JOWETT'),
    (24, 'TOLD {}', 'SHIRLEY'),
    (15, '{} TOLD US TO ADD A SECOND MOTTO', 'CONINGTON'),
    (10, '{} SCHOLARSHIP EXAMINATION', 'HERTFORD'),
    (19, '{} MAN POSTED', 'BALLIOL'),
]


def names():
    cap, low = collections.Counter(), collections.Counter()
    for f in glob.glob(os.path.join('..', 'beale', 'lmcorpus', '*.txt')):
        t = open(f, encoding='utf-8', errors='ignore').read()
        for m in re.finditer(r'(?<=[a-z,;] )([A-Z][a-z]{2,})\b', t): cap[m.group(1)] += 1
        low.update(re.findall(r'\b[a-z]{3,}\b', t))
    out = {w.upper() for w, c in cap.items() if c >= 3 and low[w.lower()] <= c // 10}
    return sorted(out | {f[2] for f in FRAMES})


if __name__ == '__main__':
    N = names()
    print('%d candidate names' % len(N))
    for ln, frame, pub in FRAMES:
        A, B = PAIRS[ln - 1]
        base = mech.cost(frame.format(pub), A, B)
        fits = []
        for n in N:
            c = mech.cost(frame.format(n), A, B, sub=False) if len(n) <= 14 else None
            if c and c[1] == 0 and c[0] <= base[0]:
                fits.append((c[0], n))
        fits.sort()
        print('\nline %d  %s  (published %s: %d omitted, %d misprints)' % (ln, frame, pub, base[0], base[1]))
        print('   %d names fit exactly with <= %d omissions: %s' % (len(fits), base[0], ', '.join('%s(%d)' % (n, o) for o, n in fits[:25])))
