"""Design-constrained annealer: the letter figures LO..HI are homophones in ALPHABETICAL ORDER (the chancery pattern of
the ff. 233 and f. 321 keys), so the letter part of the key is a vector of homophone counts, one per slot of the
alphabet, summing to HI-LO+1. Syllables from BLOCK0 in blocks of five (consonant per block, vowels a e i o u).
usage: LO=12 HI=62 BLOCK0=63 NBLK=16 MAXNULL=4 python solve_mono.py ct_333.txt [nseeds] [iters]
Slots in order: a leading null slot (doubles/nulls before a), a b c d e f g h i l m n o p q r s t u x y z, 'et', a
trailing null slot. Each letter slot has 0..MAXH homophones; the two null slots together at most MAXNULL figures, and
every letter token rendered null costs NULLPEN nats (a no-space model otherwise prefers dropping letters).
"""
import numpy as np, random, math, sys, os, re
from solve import clean, CONSI, VOW, NULL, lp, V
LO = int(os.environ.get('LO', '12')); HI = int(os.environ.get('HI', '62'))
BLOCK0 = int(os.environ.get('BLOCK0', '63')); NBLK = int(os.environ.get('NBLK', '16'))
MAXH = int(os.environ.get('MAXH', '4')); MAXNULL = int(os.environ.get('MAXNULL', '4'))
NULLPEN = float(os.environ.get('NULLPEN', '6.0'))
ALPHA = 'abcdefghilmnopqrstuxyz'
SLOTS = ['-'] + list(ALPHA) + ['et', '-']
NS = len(SLOTS); NFIG = HI - LO + 1

def parse_fixed(files):
    items = []
    for fn in files:
        for line in open(fn, encoding='utf-8'):
            if line.startswith('#'): continue
            line = line.replace('INS', ' ').replace('/INS', ' ')
            for part in re.split(r'(\[[^\]]*\])', line):
                if part.startswith('['):
                    for ch in clean(part[1:-1]): items.append(('P', ord(ch) - 97))
                else:
                    for t in part.split():
                        t = t.rstrip('?')
                        if t.isdigit():
                            n = int(t)
                            if LO <= n <= HI: items.append(('L', n - LO))
                            elif BLOCK0 <= n < BLOCK0 + 5 * NBLK: items.append(('S', (n - BLOCK0) // 5, (n - BLOCK0) % 5))
                            else: items.append(('N',))
                        else: items.append(('N',))
    return items

class MonoModel:
    def __init__(self, items):
        self.items = items
        kind, a, b = [], [], []
        for it in items:
            if it[0] == 'L': kind.append(0); a.append(it[1]); b.append(0)
            elif it[0] == 'S': kind.append(1); a.append(it[1]); b.append(it[2])
            elif it[0] == 'P': kind.append(2); a.append(it[1]); b.append(0)
            else: kind.append(3); a.append(0); b.append(0)
        self.kind = np.array(kind); self.a = np.array(a); self.b = np.array(b)
        sk, sa = [], []
        for k, aa, bb in zip(self.kind, self.a, self.b):
            if k == 0: sk.append(0); sa.append(aa)
            elif k == 1: sk.append(1); sa.append(aa); sk.append(4); sa.append(VOW[bb])
            elif k == 2: sk.append(2); sa.append(aa)
        self.sk = np.array(sk); self.sa = np.array(sa)
        self.m0 = self.sk == 0; self.m1 = self.sk == 1
        self.letter_figs = self.sa[self.m0]

def counts_to_key(counts):
    key = np.full(NFIG, NULL); et = np.zeros(NFIG, bool); pos = 0
    for s, c in enumerate(counts):
        for _ in range(c):
            if pos >= NFIG: break
            lab = SLOTS[s]
            if lab == '-': key[pos] = NULL
            elif lab == 'et': key[pos] = ord('e') - 97; et[pos] = True
            else: key[pos] = ord(lab) - 97
            pos += 1
    return key, et

class Scorer:
    def __init__(self, m): self.m = m
    def render(self, key, et, cons):
        m = self.m; base = m.sa.copy()
        base[m.m0] = key[m.sa[m.m0]]
        base[m.m1] = cons[m.sa[m.m1]]
        ets = np.zeros(len(base), bool); ets[m.m0] = et[m.sa[m.m0]]
        if ets.any():
            pieces = []
            for v, e in zip(base, ets):
                if v == NULL: continue
                pieces.append(v)
                if e: pieces.append(ord('t') - 97)
            return np.array(pieces)
        return base[base != NULL]
    def score(self, counts, cons):
        key, et = counts_to_key(counts)
        p = self.render(key, et, cons)
        p = np.concatenate([[26, 26, 26, 26], p])
        q = ((((p[:-4] * V + p[1:-3]) * V + p[2:-2]) * V + p[3:-1]) * V + p[4:])
        dropped = int((key[self.m.letter_figs] == NULL).sum())
        return float(lp[q].sum()) - NULLPEN * dropped
    def text(self, counts, cons):
        key, et = counts_to_key(counts); m = self.m; s = []
        for k, a, b in zip(m.kind, m.a, m.b):
            if k == 0: s.append('_' if key[a] == NULL else ('et' if et[a] else chr(97 + key[a])))
            elif k == 1: s.append(chr(97 + cons[a]) + chr(97 + VOW[b]))
            elif k == 2: s.append(chr(97 + a).upper())
            else: s.append('#')
        return ''.join(s)

def nulls(counts): return counts[0] + counts[-1]

def anneal(sc, seed, iters):
    rnd = random.Random(seed)
    counts = [0] + [max(1, NFIG // 24)] * len(ALPHA) + [1, 0]
    while sum(counts) < NFIG:
        i = rnd.randrange(1, NS - 1)
        if counts[i] < MAXH: counts[i] += 1
        elif nulls(counts) < MAXNULL: counts[-1] += 1
    while sum(counts) > NFIG:
        i = rnd.randrange(1, NS - 1)
        if counts[i] > 0: counts[i] -= 1
    cons = np.array([rnd.choice(CONSI) for _ in range(NBLK)])
    cur = sc.score(counts, cons); best = (cur, list(counts), cons.copy())
    for it in range(iters):
        T = max(0.03, 4.0 * (1 - it / iters))
        r = rnd.random()
        if r < 0.7:
            i, j = rnd.randrange(NS), rnd.randrange(NS)
            if i == j or counts[i] == 0: continue
            if SLOTS[j] == '-':
                if nulls(counts) >= MAXNULL: continue
            elif counts[j] >= MAXH: continue
            counts[i] -= 1; counts[j] += 1
            new = sc.score(counts, cons)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: counts[i] += 1; counts[j] -= 1
        elif r < 0.9:
            bl = rnd.randrange(NBLK); old = cons[bl]; cons[bl] = rnd.choice(CONSI)
            new = sc.score(counts, cons)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: cons[bl] = old
        else:
            b1, b2 = rnd.randrange(NBLK), rnd.randrange(NBLK)
            cons[b1], cons[b2] = cons[b2], cons[b1]; new = sc.score(counts, cons)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: cons[b1], cons[b2] = cons[b2], cons[b1]
        if cur > best[0]: best = (cur, list(counts), cons.copy())
    return best

def describe(counts):
    out = []; pos = LO
    for s, c in enumerate(counts):
        if c: out.append(f"{SLOTS[s]} {pos}" + (f"-{pos + c - 1}" if c > 1 else '')); pos += c
    return ', '.join(out)

if __name__ == '__main__':
    files = sys.argv[1].split(','); nseeds = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    iters = int(sys.argv[3]) if len(sys.argv) > 3 else 150000
    items = parse_fixed(files); m = MonoModel(items); sc = Scorer(m)
    print('items', len(items), 'letter tokens', int((m.kind == 0).sum()), 'syll tokens', int((m.kind == 1).sum()),
          'figures', LO, '-', HI, 'blocks from', BLOCK0, 'x', NBLK, 'MAXNULL', MAXNULL, 'NULLPEN', NULLPEN, flush=True)
    res = []
    for seed in range(nseeds):
        b = anneal(sc, seed, iters); res.append(b)
        print(seed, round(b[0], 1), '|', describe(b[1]), flush=True)
        print('  BLOCKS', {BLOCK0 + 5 * k: chr(97 + b[2][k]) for k in range(NBLK)}, flush=True)
        print('  ', sc.text(b[1], b[2])[:2500], flush=True)
    b = max(res, key=lambda r: r[0])
    print('BEST', round(b[0], 1)); print('KEY', describe(b[1])); print('BLOCKS', {BLOCK0 + 5 * k: chr(97 + b[2][k]) for k in range(NBLK)})
