"""Columnar transposition attack on BLUME SALAMANCA telegram 1 (615 letters), Spanish quadgram scoring.

Model: plaintext written in rows under a key of width W; columns read off in key order (complete or incomplete
columns, i.e. the last row may be short). Hill-climb the column permutation with swaps and block moves,
restarts, for every width. Calibration: real Spanish of the same length scores ~ -3.0 per quadgram;
random-order letters of the same text ~ -4.5.

Usage: python trans.py [wmin wmax restarts]
"""
import collections, glob, math, os, random, re, sys
from tg import CT

HERE = os.path.dirname(os.path.abspath(__file__))


def clean(t):
    t = t.lower()
    for a, b in (('á', 'a'), ('é', 'e'), ('í', 'i'), ('ó', 'o'), ('ú', 'u'), ('ü', 'u'), ('ñ', 'n')):
        t = t.replace(a, b)
    return re.sub('[^a-z]', '', t)


class Q:
    def __init__(self):
        cache = os.path.join(HERE, 'corpus', 'q4_es.tsv')
        if os.path.exists(cache):
            d = dict((k, float(v)) for k, v in (l.split('\t') for l in open(cache)))
            self.floor = d.pop('__floor__'); self.d = d; return
        cnt = collections.Counter()
        for f in glob.glob(os.path.join(HERE, 'corpus', 'es*.txt')):
            t = open(f, encoding='utf-8', errors='ignore').read()
            s = t.find('*** START'); e = t.find('*** END')
            x = clean(t[s:e])
            cnt.update(x[i:i + 4] for i in range(len(x) - 3))
        tot = sum(cnt.values())
        self.d = {k: math.log10(v / tot) for k, v in cnt.items()}; self.floor = math.log10(0.01 / tot)
        with open(cache, 'w') as fh:
            for k, v in self.d.items(): fh.write('%s\t%f\n' % (k, v))
            fh.write('__floor__\t%f\n' % self.floor)

    def score(self, s):
        d, f = self.d, self.floor
        return sum(d.get(s[i:i + 4], f) for i in range(len(s) - 3))


def col_lengths(n, w):
    rows, rem = divmod(n, w)
    return [rows + (1 if i < rem else 0) for i in range(w)]


def decrypt(ct, order):
    """order[k] = plaintext column index that was read k-th."""
    w = len(order); n = len(ct)
    lens = col_lengths(n, w)
    cols = [None] * w; pos = 0
    for col in order:
        L = lens[col]; cols[col] = ct[pos:pos + L]; pos += L
    return ''.join(cols[c][r] for r in range(max(lens)) for c in range(w) if r < len(cols[c]))


def climb(ct, w, q, rnd, iters=4000):
    order = list(range(w)); rnd.shuffle(order)
    cur = q.score(decrypt(ct, order)); best = (cur, order[:])
    T = 20.0
    for it in range(iters):
        o = order[:]
        r = rnd.random()
        if r < 0.5:
            a, b = rnd.sample(range(w), 2); o[a], o[b] = o[b], o[a]
        elif r < 0.8:
            a, b = sorted(rnd.sample(range(w + 1), 2)); blk = o[a:b]; del o[a:b]
            k = rnd.randrange(len(o) + 1); o[k:k] = blk
        else:
            k = rnd.randrange(1, w); o = o[k:] + o[:k]
        v = q.score(decrypt(ct, o))
        if v > cur or rnd.random() < math.exp((v - cur) / T):
            order, cur = o, v
            if v > best[0]: best = (v, o[:])
        T = max(0.5, T * 0.9993)
    return best


def main():
    wmin, wmax, R = (int(x) for x in (sys.argv[1:4] if len(sys.argv) > 3 else (4, 20, 6)))
    q = Q()
    n = len(CT)
    print('ciphertext as-is: %.3f per quadgram' % (q.score(CT) / (n - 3)))
    rnd = random.Random(1)
    res = []
    for w in range(wmin, wmax + 1):
        best = max((climb(CT, w, q, rnd) for _ in range(R)), key=lambda x: x[0])
        pt = decrypt(CT, best[1])
        res.append((best[0] / (n - 3), w, best[1], pt))
        print('W=%2d  %.3f  %s' % (w, best[0] / (n - 3), pt[:80]), flush=True)
    res.sort(reverse=True)
    print('\nbest W=%d %.3f\n%s\norder %s' % (res[0][1], res[0][0], res[0][3], res[0][2]))


if __name__ == '__main__':
    main()
