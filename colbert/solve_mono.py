"""Monotone-vocabulary annealer for the Charost / Gravel-Maulevrier key (Mel. Colbert 172 f.23 and 168bis ff.553-554).

Hypothesis: a one-part (alphabetically ordered) key in two regions. Numbers below SPLIT are one vocabulary, numbers
from SPLIT up are the other; each region's numbers map monotonically (non-decreasing) onto an ordered vocabulary.
Vocabularies: 'S' = syllables in consonant blocks, vowels a e i o u in order (b..z); 'L' = letters a..z (v->u, j->i)
with free homophone counts. REGION=SL means low numbers syllables, high numbers letters; LS the reverse.
Clear French in [brackets] is fixed context. LM: ../ducroc/frn5.npy (5-gram, 26 = word boundary, unused here).

usage: python solve_mono.py ct.txt [more ct files]   env: SPLIT=400 REGION=SL ITERS=200000 SEED=1 CRIB=file
"""
import numpy as np, random, math, sys, re, unicodedata, os, collections
lp = np.load(os.environ.get('LM', '../ducroc/frn5.npy')); V = 27
SPLIT = int(os.environ.get('SPLIT', '400')); REGION = os.environ.get('REGION', 'SL')
ITERS = int(os.environ.get('ITERS', '200000')); SEED = int(os.environ.get('SEED', '1'))
LET = 'abcdefghilmnopqrstuxyz'
CONS = 'bcdfghlmnpqrstxz'
VOW = 'aeiou'
SYL = [c + v for c in CONS for v in VOW]           # 80 syllables in block order
VOCAB = {'L': [(ord(c) - 97,) for c in LET], 'S': [(ord(s[0]) - 97, ord(s[1]) - 97) for s in SYL]}

def clean(t):
    t = unicodedata.normalize('NFKD', t.lower()); t = ''.join(c for c in t if not unicodedata.combining(c))
    t = t.replace('v', 'u').replace('j', 'i').replace('k', 'c').replace('w', 'u')
    return re.sub(r'[^a-z]', '', t)

def parse(files):
    """items: ('C', number) cipher token, ('P', letter index) fixed plaintext."""
    items = []
    for fn in files:
        for line in open(fn, encoding='utf-8'):
            if line.startswith('#'): continue
            for part in re.split(r'(\[[^\]]*\])', line):
                if part.startswith('['):
                    for ch in clean(part[1:-1]): items.append(('P', ord(ch) - 97))
                else:
                    for t in part.split():
                        t = t.rstrip('?.,;')
                        if t.isdigit(): items.append(('C', int(t)))
    return items

class Model:
    def __init__(self, items):
        self.items = items
        nums = sorted({n for k, n in items if k == 'C'})
        self.regions = []   # list of (numbers sorted, vocab list)
        lo = [n for n in nums if n < SPLIT]; hi = [n for n in nums if n >= SPLIT]
        self.regions.append((lo, VOCAB[REGION[0]])); self.regions.append((hi, VOCAB[REGION[1]]))
        self.symreg = {}; self.symidx = {}
        for r, (ns, voc) in enumerate(self.regions):
            for i, n in enumerate(ns): self.symreg[n] = r; self.symidx[n] = i
    def init_key(self, rnd):
        key = []
        for ns, voc in self.regions:
            # spread evenly over the vocabulary, then jitter
            k = [min(len(voc) - 1, int(i * len(voc) / max(1, len(ns)))) for i in range(len(ns))]
            key.append(k)
        return key
    def render(self, key):
        out = []
        for k, a in self.items:
            if k == 'P': out.append(a)
            else:
                r = self.symreg[a]; voc = self.regions[r][1]; out.extend(voc[key[r][self.symidx[a]]])
        return np.array(out)
    def score(self, key):
        p = np.concatenate([[26] * 4, self.render(key)])
        q = ((((p[:-4] * V + p[1:-3]) * V + p[2:-2]) * V + p[3:-1]) * V + p[4:])
        return float(lp[q].sum())
    def text(self, key):
        s = []
        for k, a in self.items:
            if k == 'P': s.append(chr(97 + a).upper())
            else:
                r = self.symreg[a]; voc = self.regions[r][1]
                s.append(''.join(chr(97 + x) for x in voc[key[r][self.symidx[a]]]) + ' ')
        return ''.join(s)
    def keytable(self, key):
        rows = []
        for r, (ns, voc) in enumerate(self.regions):
            for i, n in enumerate(ns): rows.append((n, ''.join(chr(97 + x) for x in voc[key[r][i]])))
        return rows

def anneal(m, rnd, iters, t0=3.0, t1=0.05):
    key = m.init_key(rnd); cur = m.score(key); best = cur; bestkey = [k[:] for k in key]
    for it in range(iters):
        T = t0 * (t1 / t0) ** (it / iters)
        r = rnd.randrange(len(m.regions)); ns, voc = m.regions[r]
        if not ns: continue
        i = rnd.randrange(len(ns)); k = key[r]
        lo = k[i - 1] if i > 0 else 0; hi = k[i + 1] if i + 1 < len(k) else len(voc) - 1
        if rnd.random() < 0.7:
            # move one symbol within its monotone window
            if lo == hi: continue
            new = rnd.randint(lo, hi)
            if new == k[i]: continue
            old = k[i]; k[i] = new
            s = m.score(key)
            if s >= cur or rnd.random() < math.exp((s - cur) / T): cur = s
            else: k[i] = old
        else:
            # shift a whole run of symbols by +-1 (keeps monotonicity if room)
            j = min(len(k), i + rnd.randint(1, 6)); d = rnd.choice((-1, 1))
            seg = k[i:j]
            if d < 0 and (i > 0 and seg[0] - 1 < k[i - 1] or seg[0] - 1 < 0): continue
            if d > 0 and (j < len(k) and seg[-1] + 1 > k[j] or seg[-1] + 1 >= len(voc)): continue
            k[i:j] = [x + d for x in seg]
            s = m.score(key)
            if s >= cur or rnd.random() < math.exp((s - cur) / T): cur = s
            else: k[i:j] = seg
        if cur > best: best = cur; bestkey = [kk[:] for kk in key]
    return best, bestkey

if __name__ == '__main__':
    files = sys.argv[1:]
    items = parse(files); m = Model(items)
    print('tokens', sum(1 for k, _ in items if k == 'C'), 'plain letters', sum(1 for k, _ in items if k == 'P'),
          'regions', [len(ns) for ns, _ in m.regions], 'SPLIT', SPLIT, 'REGION', REGION)
    rnd = random.Random(SEED)
    best, key = anneal(m, rnd, ITERS)
    print('score', round(best, 1))
    print(m.text(key))
    print(' '.join(f'{n}={v}' for n, v in m.keytable(key)))
