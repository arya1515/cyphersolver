"""Perwich 1670: reproduce the published break from Tomokiyo's transcription.

Each transcribed ROW is one COLUMN of a columnar transposition; the plaintext is read across the
rows by depth (cell k of every row in key order). Hill-climb the row order against English quadgrams.
"""
import random, re, sys
import grid, masc

EXP = {'ye': 'the', 'yt': 'that', 'ym': 'them', 'wt': 'with', '&': 'and', 'U': 'll'}


def cols():
    out = []
    for r in grid.load():
        c = [grid.norm(x) for x in r]
        out.append([x for x in c if x])
    return out


def read(C, order, expand=True, sep=''):
    depth = max(len(c) for c in C)
    toks = []
    for k in range(depth):
        for i in order:
            if k < len(C[i]):
                toks.append(C[i][k])
    if not expand:
        return sep.join(toks)
    s = []
    for t in toks:
        if t.isdigit():
            s.append('')
        elif t == 'likelyhood':
            s.append('')
        else:
            s.append(EXP.get(t, t.lower()))
    return ''.join(re.sub('[^a-z]', '', x) for x in s)


def climb(C, q, rnd):
    n = len(C)
    order = list(range(n)); rnd.shuffle(order)
    best = q.score(read(C, order))
    imp = True
    while imp:
        imp = False
        for a in range(n):
            for b in range(n):
                if a == b: continue
                o = order[:]; x = o.pop(a); o.insert(b, x)
                v = q.score(read(C, o))
                if v > best:
                    best, order, imp = v, o, True
    return best, order


if __name__ == '__main__':
    q = masc.Q()
    C = cols()
    res = []
    for r in range(int(sys.argv[1]) if len(sys.argv) > 1 else 8):
        sc, o = climb(C, q, random.Random(r))
        res.append((sc, o))
        print('%3d %.0f %s' % (r, sc, read(C, o)[:90]), flush=True)
    res.sort(reverse=True)
    sc, o = res[0]
    print('\nbest %.0f order (1-based rows): %s' % (sc, [i + 1 for i in o]))
    print(read(C, o, expand=False, sep=' '))
