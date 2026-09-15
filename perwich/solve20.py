"""Perwich 1670 - reproduction of the published break (TNA, 14 Oct 2025) from Tomokiyo's transcription.

Structure: transcribed rows 2-21 are the 20 columns of a columnar transposition, each written out as a
line and padded at its right-hand end with nulls. Rows 1 and 22 are whole null lines framing the block.
Plaintext is read across the columns, depth by depth, in key order.

The key (column order) is found by hill-climbing against English quadgrams alone - the published
plaintext is used only afterwards, to check the result.

Usage: python solve20.py [restarts]
"""
import random, re, sys
import grid, masc
from rebreak import EXP

def columns():
    rows = [[grid.norm(c) for c in r if grid.norm(c)] for r in grid.load()]
    return rows[1:21]

def depth_read(C, order):
    out = []
    for k in range(max(len(c) for c in C)):
        for i in order:
            if k < len(C[i]):
                out.append(C[i][k])
    return out

def text(toks):
    return ''.join('' if (t.isdigit() or t == 'likelyhood') else re.sub('[^a-z]', '', EXP.get(t, t.lower())) for t in toks)

def climb(C, q, rnd, rows=19):
    """Score only the first `rows` depths, where no column has run into its trailing nulls."""
    n = len(C)
    order = list(range(n)); rnd.shuffle(order)
    f = lambda o: q.score(text([C[i][k] for k in range(rows) for i in o]))
    best = f(order); imp = True
    while imp:
        imp = False
        for a in range(n):
            for b in range(n):
                if a != b:
                    o = order[:]; x = o.pop(a); o.insert(b, x)
                    v = f(o)
                    if v > best: best, order, imp = v, o, True
    return best, order

if __name__ == "__main__" and (len(sys.argv) < 2 or sys.argv[1] != "report"):
    q = masc.Q(); C = columns()
    res = []
    for r in range(int(sys.argv[1]) if len(sys.argv) > 1 else 10):
        res.append(climb(C, q, random.Random(r)))
        print('restart %2d  %.0f  %s' % (r, res[-1][0], [i + 2 for i in res[-1][1]]), flush=True)
    res.sort(reverse=True)
    best = res[0][1]
    agree = sum(1 for s, o in res if o == best)
    print('\n%d of %d restarts reach the same key' % (agree, len(res)))
    print('key (transcribed row numbers, in plaintext column order):', [i + 2 for i in best])
    print('\ndepth matrix:')
    for k in range(max(len(c) for c in C)):
        print('%2d  %s' % (k, ' '.join('%-3s' % (C[i][k] if k < len(C[i]) else '.') for i in best)))


# ---------------------------------------------------------------------------------------------------
# The climber finds the cyclic sequence of columns; where it starts is fixed by the plaintext itself
# (depth 0 ends "...grumble m", depth 1 begins "uch"), and independently by the column lengths: the
# columns holding one more plaintext cell than the rest must come first.
KEY = [15, 20, 19, 17, 18, 21, 16, 14, 2, 4, 3, 5, 6, 7, 13, 12, 11, 10, 9, 8]
PLAIN_CELLS = 20 * 20 + 14      # 20 full depths plus 14 cells of a 21st


def report():
    import collections, math
    C = columns()
    o = [k - 2 for k in KEY]
    toks = depth_read(C, o)
    pt = []
    for k in range(21):
        for j, i in enumerate(o):
            if k * 20 + j < PLAIN_CELLS:
                pt.append(C[i][k])
    print('plaintext, %d cells, read in key order:\n' % len(pt))
    line = ''
    for t in pt:
        w = t if len(t) == 1 else '[%s]' % t
        line += w
        if len(line) > 90:
            print('   ' + line); line = ''
    print('   ' + line)
    nulls = [c for i in o for c in C[i][(21 if o.index(i) < 14 else 20):]]
    rows = [[grid.norm(c) for c in r if grid.norm(c)] for r in grid.load()]
    print('\ncolumn-tail nulls: %d  %s' % (len(nulls), ' '.join(nulls)))
    print('null lines: row 1 (%d cells) %s' % (len(rows[0]), ' '.join(rows[0])))
    print('            row 22 (%d cells) %s' % (len(rows[21]), ' '.join(rows[21])))

    eng = dict(zip('etaoinshrdlcumwfgypbvkjxqz', [12.7, 9.1, 8.2, 7.5, 7.0, 6.7, 6.3, 6.1, 6.0, 4.3, 4.0,
               2.8, 2.8, 2.4, 2.4, 2.2, 2.0, 2.0, 1.9, 1.5, 1.0, .8, .15, .15, .1, .07]))
    def chi(s):
        c = collections.Counter(s); n = len(s)
        return sum((c[l] - n * p / 100) ** 2 / (n * p / 100) for l, p in eng.items())
    whole = text([c for r in rows for c in r])
    clean = text(pt)
    print('\nchi-squared in place: whole grid %.1f (%d letters), plaintext cells only %.1f (%d letters)'
          % (chi(whole), len(whole), chi(clean), len(clean)))
    qq = collections.Counter(whole)['q']
    print('q alone contributes %.1f of the whole-grid figure' % ((qq - len(whole) * .001) ** 2 / (len(whole) * .001)))


if __name__ == '__main__' and len(sys.argv) > 1 and sys.argv[1] == 'report':
    report()
