"""Exact mechanics for the Catokwacopa pair: how well does a proposed plaintext explain a line?

Model (the one everyone now works with): the plaintext of line i, after W. dropped some letters, was
split into two order-preserving streams; stream A went into the 8 May ad, stream B into the 20 May ad.
So a reading P explains (A, B) exactly when some interleaving of A and B is a subsequence of P.

cost(P, A, B) returns (omitted, errors):
    omitted - plaintext letters that appear in neither stream (W.'s abbreviation)
    errors  - cipher letters that must be misprints (substituted, or with no plaintext letter at all)
Errors are what distinguish a mechanical reading from an emendation; omissions are free in the model,
which is exactly why they need a control.

Usage: python mech.py        - length-pairing test, and every published reading scored
"""
import random, re
from functools import lru_cache
from ads import PAIRS, LETTER_LINES

BIG = 10 ** 6


def cost(P, A, B, sub=True):
    P = re.sub('[^a-z]', '', P.lower()); A = A.lower(); B = B.lower()
    n, a, b = len(P), len(A), len(B)
    # dp over (k, i, j) = min errors*BIG + omitted, via forward relaxation
    INF = float('inf')
    cur = {(0, 0): 0}
    for k in range(n + 1):
        # cipher letters with no plaintext letter (pure insertion errors) can be absorbed at any k
        frontier = dict(cur)
        changed = True
        while changed:
            changed = False
            for (i, j), v in list(frontier.items()):
                for ni, nj in ((i + 1, j), (i, j + 1)):
                    if ni <= a and nj <= b:
                        nv = v + BIG
                        if nv < frontier.get((ni, nj), INF):
                            frontier[(ni, nj)] = nv; changed = True
        if k == n:
            v = frontier.get((a, b), INF)
            return (int(v % BIG), int(v // BIG)) if v < INF else None
        nxt = {}
        c = P[k]
        for (i, j), v in frontier.items():
            cand = [((i, j), v + 1)]                                   # omitted by W.
            if i < a: cand.append(((i + 1, j), v + (0 if A[i] == c else (BIG if sub else INF))))
            if j < b: cand.append(((i, j + 1), v + (0 if B[j] == c else (BIG if sub else INF))))
            for s, nv in cand:
                if nv < nxt.get(s, INF): nxt[s] = nv
        cur = nxt


def interleave(P, A, B):
    """For an exact (0-error) reading, show which stream supplied each plaintext letter."""
    P = re.sub('[^a-z]', '', P.lower())
    @lru_cache(None)
    def go(k, i, j):
        if k == len(P): return '' if (i == len(A) and j == len(B)) else None
        opts = []
        if i < len(A) and A[i] == P[k]:
            r = go(k + 1, i + 1, j)
            if r is not None: opts.append(P[k].upper() + r)          # upper = 8 May stream
        if j < len(B) and B[j] == P[k]:
            r = go(k + 1, i, j + 1)
            if r is not None: opts.append(P[k] + r)                  # lower = 20 May stream
        r = go(k + 1, i, j)
        if r is not None: opts.append('.' + r)                       # . = omitted
        return min(opts, key=lambda s: s.count('.')) if opts else None
    return go(0, 0, 0)


READINGS = {
    1: ['SUMMER TERM'],
    3: ['CAP TOOK AWAY AT COLLEGE PARTY'],
    4: ['OLD CAP BROKE AT CORNER LEFT INSTEAD'],
    5: ['CONINGTON MET ME IN GARDEN'],
    6: ['SAID SIMPLY YOUR CAP IS HONESTY IN CHARACTER'],
    7: ['REPEATED'],
    8: ['I ATTENDED CONINGTON LECTURES', 'I ATTENDED CONINGTON LECSURES'],
    9: ['MASTER PUPIL', 'MOISTENED PURL'],
    10: ['HE OFFERED SCHOLARSHIP EXAMINATION', 'HERTFORD SCHOLARSHIP EXAMINATION'],
    12: ['CANT SELECT MUCH FUND OR SEIZE A MOTTO'],
    14: ['MOTTO PROUDLY USED IN COLLEGE', 'MOTTO PREVIOUSLY USED IN COLLEGE',
         'MOTTO WAS PREVIOUSLY DISCLOSED IN COLLEGE'],
    15: ['CONINGTON TOLD US A SECOND MOTTO', 'CONINGTON TOLD US TO ADD A SECOND MOTTO'],
    16: ['I ADDED FIRST LINE IS ARTS', 'I ADDED FIRST LINE SATIRS', 'I ADDED FIRST LINE OF SATIRES'],
    17: ['QUIT', 'QUI FIT'],
    18: ['COUNTED CAP', 'CONINGTON DEPARTED'],
    19: ['BALLIOL MAN POSTED'],
    21: ['HAD EXAMINATION', 'HOSTED MY EXAMINATION'],
    24: ['TOLD SHIRLEY'],
    25: ['I ATTENDED JOWETT LECTURES', 'I ATTENDED JOWETT LECSURS'],
    26: ['MASTER PUPIL', 'MOISTENED PURL'],
    27: ['DYING', 'DOING', 'SIGNED'],
    28: ['DECLARATION'],
    29: ['RELIGIONEM CONFIRMARE'],
}


def length_test(trials=100000):
    L = [(len(PAIRS[i - 1][0]), len(PAIRS[i - 1][1])) for i in LETTER_LINES]
    def stat(pairs): return sum(abs(x - y) for x, y in pairs)
    obs = stat(L)
    xs = [x for x, _ in L]; ys = [y for _, y in L]
    rnd = random.Random(1); hits = 0
    for _ in range(trials):
        rnd.shuffle(ys)
        if stat(zip(xs, ys)) <= obs: hits += 1
    print('line-length pairing: sum |len A - len B| over %d letter lines = %d; '
          'random re-pairings reach that in %d of %d' % (len(L), obs, hits, trials))


if __name__ == '__main__':
    length_test()
    print('\n%-4s %-44s %4s %4s  %s' % ('line', 'reading', 'omit', 'err', 'interleaving (UPPER 8 May, lower 20 May, . omitted)'))
    for ln, rs in READINGS.items():
        A, B = PAIRS[ln - 1]
        for r in rs:
            c = cost(r, A, B)
            il = interleave(r, A, B) if c and c[1] == 0 else ''
            print('%-4d %-44s %4s %4s  %s' % (ln, r, c[0] if c else '-', c[1] if c else '-', il))


def fit_rule(P, A, B):
    """Exact (0-error) fit under the word-initial rule: every plaintext word's first letter is present
    and comes from the 8 May stream. Returns (omitted, interleaving) or None."""
    words = re.findall('[a-z]+', P.lower()); A = A.lower(); B = B.lower()
    s = ''.join(words)
    starts = set(); k = 0
    for w in words:
        starts.add(k); k += len(w)
    @lru_cache(None)
    def go(k, i, j):
        if k == len(s): return '' if (i == len(A) and j == len(B)) else None
        opts = []
        if i < len(A) and A[i] == s[k]:
            r = go(k + 1, i + 1, j)
            if r is not None: opts.append(s[k].upper() + r)
        if k not in starts:
            if j < len(B) and B[j] == s[k]:
                r = go(k + 1, i, j + 1)
                if r is not None: opts.append(s[k] + r)
            r = go(k + 1, i, j)
            if r is not None: opts.append('.' + r)
        return min(opts, key=lambda x: x.count('.')) if opts else None
    r = go(0, 0, 0)
    if r is None: return None
    out, k = [], 0
    for w in words:
        out.append(r[k:k + len(w)]); k += len(w)
    return r.count('.'), ' '.join(out)


def rule_report():
    print('\nword-initial rule (each word begins with a letter of the 8 May stream):')
    for ln, rs in READINGS.items():
        A, B = PAIRS[ln - 1]
        for r in rs:
            c = cost(r, A, B)
            if not c or c[1]: continue
            f = fit_rule(r, A, B)
            print('   %-3d %-42s %s' % (ln, r, ('holds  ' + f[1]) if f else 'FAILS'))
