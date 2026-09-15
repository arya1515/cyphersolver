"""Recovering the column order of Perwich's 1670 transposition.

The grid parses to 22 rows of 21 to 27 cells. Read straight down the columns it is not English, so
the columns are permuted - which is what a columnar transposition is. The permutation is the whole
secret, and it can be searched, because the plaintext is ordinary English and an n-gram model will
tell a right order from a wrong one.

Two things make this easier than the usual case. The cells are not all single letters: **ye**, **yt**,
**wt** and **ym** are the period abbreviations for *the*, *that*, *with* and *them*, and expanding
them before scoring hands the language model real words instead of noise. And one cell is the plain
English word *likelyhood*, sitting at the end of the passage, which tells us roughly where the text
ends.

The search is simulated annealing over column orders, scored with English quadgrams built from the
local corpus. Every run is reported, because a transposition that is genuinely solved converges: the
restarts agree. If they disagree, the answer is that the grid as transcribed is not a plain columnar
transposition, and that is worth knowing too.

Usage:
    python solve.py [restarts] [iters]
"""
import collections, glob, math, os, random, re, sys

import grid

CORPUS = os.path.join('..', 'beale', 'lmcorpus')

EXPAND = {'ye': 'the', 'yt': 'that', 'wt': 'with', 'ym': 'them', 'wch': 'which'}


def cells_to_text(cells):
    out = []
    for c in cells:
        c = c.strip()
        if not c:
            continue
        low = c.lower()
        if low in EXPAND:
            out.append(EXPAND[low])
        elif c.isdigit():
            out.append(' ')            # nomenclator code: unknown word
        else:
            out.append(re.sub(r'[^A-Za-z]', '', c).lower())
    return ''.join(out)


def build_lm(n=4, max_files=18):
    cnt = collections.Counter()
    ctx = collections.Counter()
    for f in sorted(glob.glob(os.path.join(CORPUS, '*.txt')))[:max_files]:
        txt = open(f, encoding='utf-8', errors='ignore').read().lower()
        txt = re.sub('[^a-z]', '', txt)
        for i in range(len(txt) - n):
            g = txt[i:i + n]
            cnt[g] += 1
            ctx[g[:-1]] += 1
    return cnt, ctx, n


class LM:
    def __init__(self):
        self.cnt, self.ctx, self.n = build_lm()
        self.floor = math.log(0.01 / 26)

    def score(self, s):
        s = re.sub('[^a-z]', '', s)
        if len(s) < self.n:
            return -999.0
        tot = 0.0
        n = self.n
        for i in range(len(s) - n + 1):
            g = s[i:i + n]
            c = self.cnt.get(g, 0)
            d = self.ctx.get(g[:-1], 0)
            tot += math.log((c + 0.1) / (d + 2.6)) if d else self.floor
        return tot / (len(s) - n + 1)


def read_order(cols, order):
    return ''.join(cells_to_text(cols[i]) for i in order)


def anneal(cols, lm, iters, rnd):
    n = len(cols)
    order = list(range(n))
    rnd.shuffle(order)
    cur = lm.score(read_order(cols, order))
    best = (cur, list(order))
    T = 1.0
    for it in range(iters):
        a, b = rnd.randrange(n), rnd.randrange(n)
        if a == b:
            continue
        order[a], order[b] = order[b], order[a]
        v = lm.score(read_order(cols, order))
        if v > cur or rnd.random() < math.exp((v - cur) / max(T, 1e-9)):
            cur = v
            if v > best[0]:
                best = (v, list(order))
        else:
            order[a], order[b] = order[b], order[a]
        T = max(0.02, T * 0.9995)
    return best


def main():
    restarts = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    iters = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
    rows = grid.load()
    cols = grid.columns(rows)
    lm = LM()
    print('%d columns, %d cells' % (len(cols), sum(len(c) for c in cols)))
    nat = read_order(cols, list(range(len(cols))))
    print('natural order  %.4f  %s' % (lm.score(nat), nat[:90]))
    # calibration: what does real English score, and what does a shuffle score?
    eng = re.sub('[^a-z]', '', open(os.path.join(CORPUS, 'pg1342.txt'), encoding='utf-8',
                                    errors='ignore').read().lower())[:len(nat)]
    print('real English   %.4f' % lm.score(eng))
    rnd = random.Random(7)
    sh = list(nat)
    rnd.shuffle(sh)
    print('shuffled       %.4f' % lm.score(''.join(sh)))

    print('\nannealing:')
    results = []
    for r in range(restarts):
        rnd2 = random.Random(100 + r)
        sc, order = anneal(cols, lm, iters, rnd2)
        txt = read_order(cols, order)
        results.append((sc, order, txt))
        print('   run %d  %.4f  %s' % (r + 1, sc, txt[:86]))
    results.sort(reverse=True)
    print('\nbest:\n%s' % results[0][2][:600])
    # agreement between runs
    if len(results) > 1:
        a = results[0][1]
        agree = []
        for sc, o, t in results[1:]:
            agree.append(sum(1 for i in range(len(a)) if a[i] == o[i]) / len(a))
        print('\npositional agreement of other runs with the best: %s'
              % ' '.join('%.2f' % x for x in agree))


if __name__ == '__main__':
    main()
