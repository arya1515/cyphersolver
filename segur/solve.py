"""Structured homophonic annealer for the Navarre-Segur cipher (500 Colbert 401 ff.233, 239, 288v).

Model: numeric tokens 1..63 are letters/nulls (free homophones); 64..123 are syllables in blocks of five
(consonant per block, vowels a e i o u in order); anything else (inline glyphs, numbers >123) is an unknown
name token and is skipped. Clear French in [brackets] is kept as fixed plaintext context.
LM: ../ducroc/frn5.npy (French 5-gram, no spaces, v->u j->i, alphabet a-z with 26 = space unused here).
"""
import numpy as np, random, math, sys, re, unicodedata, os, collections
lp = np.load(os.environ.get('LM', '../ducroc/frn5.npy')); V = 27
LET = 'abcdefghilmnopqrstuxyz'
LETI = [ord(c) - 97 for c in LET]
NULL = -1
CONS = 'bcdfghlmnpqrstxz'          # candidate block consonants (v written u, j written i)
CONSI = [ord(c) - 97 for c in CONS]
VOW = [ord(c) - 97 for c in 'aeiou']
BLOCK0 = int(os.environ.get('BLOCK0', '54')); NBLK = int(os.environ.get('NBLK', '14'))
NULLPEN = float(os.environ.get('NULLPEN', '3.0')); MAXNULL = int(os.environ.get('MAXNULL', '8'))

def clean(t):
    t = unicodedata.normalize('NFKD', t.lower()); t = ''.join(c for c in t if not unicodedata.combining(c))
    t = t.replace('v', 'u').replace('j', 'i')
    return re.sub(r'[^a-z]', '', t)

def parse(files):
    """Return list of items: ('L',sym) letter symbol index, ('S',block,vowel), ('P',letter) fixed plaintext, ('N',) unknown."""
    items = []; syms = {}
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
                            if 1 <= n < BLOCK0:
                                if n not in syms: syms[n] = len(syms)
                                items.append(('L', syms[n]))
                            elif BLOCK0 <= n < BLOCK0 + 5 * NBLK:
                                items.append(('S', (n - BLOCK0) // 5, (n - BLOCK0) % 5))
                            else: items.append(('N',))
                        else: items.append(('N',))
    return items, syms

class Model:
    def __init__(self, items, nsym):
        self.items = items; self.nsym = nsym
        # arrays for fast rendering
        self.kind = np.array([{'L': 0, 'S': 1, 'P': 2, 'N': 3}[i[0]] for i in items])
        self.a = np.array([i[1] if i[0] in 'LSP' else 0 for i in items])
        self.b = np.array([i[2] if i[0] == 'S' else 0 for i in items])
        # output slots: letters -> 1 slot (kind0), syllables -> 2 slots (kind1 cons, kind4 vowel), plain -> kind2
        sk, sa = [], []
        for k, a, b in zip(self.kind, self.a, self.b):
            if k == 0: sk.append(0); sa.append(a)
            elif k == 1: sk.append(1); sa.append(a); sk.append(4); sa.append(VOW[b])
            elif k == 2: sk.append(2); sa.append(a)
        self.sk = np.array(sk); self.sa = np.array(sa)
        self.nletters = int((self.sk == 0).sum()); self.m0 = self.sk == 0; self.m1 = self.sk == 1
    def render(self, key, cons):
        out = self.sa.copy()
        out[self.m0] = key[self.sa[self.m0]]
        out[self.m1] = cons[self.sa[self.m1]]
        return out[out != NULL]
    def score(self, key, cons):
        p = self.render(key, cons)
        p = np.concatenate([[26, 26, 26, 26], p])
        q = ((((p[:-4] * V + p[1:-3]) * V + p[2:-2]) * V + p[3:-1]) * V + p[4:])
        dropped = self.nletters - int((key[self.sa[self.sk == 0]] != NULL).sum())
        return float(lp[q].sum()) - NULLPEN * dropped
    def text(self, key, cons, mark=True):
        s = []
        for k, a, b in zip(self.kind, self.a, self.b):
            if k == 0: s.append('_' if key[a] == NULL else chr(97 + key[a]))
            elif k == 1: s.append(chr(97 + cons[a]) + chr(97 + VOW[b]))
            elif k == 2: s.append(chr(97 + a).upper() if mark else chr(97 + a))
            else: s.append('#')
        return ''.join(s)

def anneal(m, seed, iters=150000, T0=4.0, pnull=0.08):
    rnd = random.Random(seed)
    key = np.array([rnd.choice(LETI) for _ in range(m.nsym)])
    cons = np.array([rnd.choice(CONSI) for _ in range(NBLK)])
    cur = m.score(key, cons); best = (cur, key.copy(), cons.copy())
    for it in range(iters):
        T = max(0.03, T0 * (1 - it / iters))
        r = rnd.random()
        if r < 0.55:
            s = rnd.randrange(m.nsym); old = key[s]
            key[s] = NULL if (rnd.random() < pnull and (key == NULL).sum() < MAXNULL) else rnd.choice(LETI)
            new = m.score(key, cons)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: key[s] = old
        elif r < 0.8:
            s, t = rnd.randrange(m.nsym), rnd.randrange(m.nsym)
            key[s], key[t] = key[t], key[s]; new = m.score(key, cons)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: key[s], key[t] = key[t], key[s]
        elif r < 0.93:
            bl = rnd.randrange(NBLK); old = cons[bl]; cons[bl] = rnd.choice(CONSI)
            new = m.score(key, cons)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: cons[bl] = old
        else:
            b1, b2 = rnd.randrange(NBLK), rnd.randrange(NBLK)
            cons[b1], cons[b2] = cons[b2], cons[b1]; new = m.score(key, cons)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: cons[b1], cons[b2] = cons[b2], cons[b1]
        if cur > best[0]: best = (cur, key.copy(), cons.copy())
    return best

if __name__ == '__main__':
    files = sys.argv[1].split(','); nseeds = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    iters = int(sys.argv[3]) if len(sys.argv) > 3 else 150000
    items, syms = parse(files); m = Model(items, len(syms))
    inv = {v: k for k, v in syms.items()}
    print('items', len(items), 'letter syms', len(syms), 'syll tokens', sum(1 for i in items if i[0] == 'S'),
          'letter tokens', sum(1 for i in items if i[0] == 'L'), flush=True)
    res = []
    for seed in range(nseeds):
        b = anneal(m, seed, iters); res.append(b)
        print(seed, round(b[0], 1), flush=True)
        print('  ', m.text(b[1], b[2])[:3000], flush=True)
    b = max(res, key=lambda r: r[0])
    print('BEST', round(b[0], 1))
    print('KEY', {inv[i]: ('-' if b[1][i] == NULL else chr(97 + b[1][i])) for i in range(len(syms))})
    print('BLOCKS', {BLOCK0 + 5 * k: chr(97 + b[2][k]) for k in range(NBLK)})
