"""Perwich 1670 as a columnar transposition with an unknown period.

The first attempt treated the transcription's layout as the cipher grid. That was wrong. The
manuscript is written in aligned columns because that is how the clerk laid it out, and the
transcribed lines run from 21 to 27 cells, which no columnar transposition produces. The ciphertext is
a stream; the period has to be found.

Two measurements support a transposition and rule out much else. The index of coincidence of the
single-letter cells is **0.0636**, against 0.0667 for English and 0.0385 for random - so the letters
are English letters, merely out of order. And sorting the observed frequencies against sorted English
lines up closely, which is what a transposition does and a substitution does not.

The deviations that remain are informative rather than fatal. **l** is at 1.08% where English gives
4.03%, and **u** at 4.33% where English gives 2.76%. Tomokiyo, who made the transcription, flags
exactly this in his own notes - "I'm still wondering whether U is actually ll". Reading his U as a
doubled l moves both letters the right way at once.

So: take the cells in reading order as a stream, try every period, and for each one hill-climb the
column order against an English model. A transposition that is really there converges; restarts agree.

Usage:
    python stream.py [minperiod] [maxperiod] [restarts]
"""
import collections, math, random, re, sys

import grid
import solve as S


def stream(expand_u=False):
    rows = grid.load()
    out = []
    for r in rows:
        for c in r:
            c = grid.norm(c)
            if not c:
                continue
            low = c.lower()
            if low in S.EXPAND:
                out.append(S.EXPAND[low])
            elif c.isdigit():
                out.append('')
            elif c == 'U' and expand_u:
                out.append('ll')
            else:
                out.append(re.sub(r'[^A-Za-z]', '', c).lower())
    return [x for x in out if x]


def columnise(units, period):
    """Split the stream into columns as a columnar transposition would have produced them."""
    L = len(units)
    rows, rem = divmod(L, period)
    heights = [rows + 1 if c < rem else rows for c in range(period)]
    cols, i = [], 0
    for h in heights:
        cols.append(units[i:i + h])
        i += h
    return cols


def read(cols, order):
    """Read the grid back row-wise under a column order."""
    inv = [0] * len(order)
    for pos, c in enumerate(order):
        inv[c] = pos
    arranged = [cols[c] for c in order]
    maxh = max(len(c) for c in arranged)
    out = []
    for r in range(maxh):
        for c in arranged:
            if r < len(c):
                out.append(c[r])
    return ''.join(out)


def anneal(cols, lm, iters, rnd):
    n = len(cols)
    order = list(range(n))
    rnd.shuffle(order)
    cur = lm.score(read(cols, order))
    best = (cur, list(order))
    T = 0.6
    for _ in range(iters):
        a, b = rnd.randrange(n), rnd.randrange(n)
        if a == b:
            continue
        order[a], order[b] = order[b], order[a]
        v = lm.score(read(cols, order))
        if v > cur or rnd.random() < math.exp((v - cur) / max(T, 1e-9)):
            cur = v
            if v > best[0]:
                best = (v, list(order))
        else:
            order[a], order[b] = order[b], order[a]
        T = max(0.02, T * 0.9994)
    return best


def main():
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 26
    restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    lm = S.LM()
    for expand_u in (False, True):
        units = stream(expand_u)
        flat = ''.join(units)
        print('\n=== U read as %s : %d units, %d letters' %
              ('ll' if expand_u else 'u', len(units), len(flat)))
        rows = []
        for period in range(lo, hi + 1):
            cols = columnise(units, period)
            best = None
            for r in range(restarts):
                rnd = random.Random(period * 1000 + r)
                sc, order = anneal(cols, lm, 2500, rnd)
                if best is None or sc > best[0]:
                    best = (sc, order)
            txt = read(cols, best[1])
            rows.append((best[0], period, txt))
            print('   period %2d  %.4f  %s' % (period, best[0], txt[:74]), flush=True)
        rows.sort(reverse=True)
        print('   BEST period %d at %.4f' % (rows[0][1], rows[0][0]))
        print('   %s' % rows[0][2][:400])


if __name__ == '__main__':
    main()
