"""Region-structured annealer for the Charost / Gravel-Maulevrier key.

REGIONS env, e.g. "52-99:Lf,100-399:Sc,400-489:La"  (ranges inclusive, applied to the numbers seen in the text)
  La = letters, alphabetical (monotone) with free homophone counts
  Ma = Conde-type series: letters and their syllables interleaved alphabetically (a, b, ba..bu, c, ca..), monotone
  Lf = letters, free homophonic
  Sa = syllables, strict block order (consonants b..z, vowels a e i o u in order), monotone
  Sc = syllables, consonant blocks in order (monotone), vowel free per symbol
  Sf = syllables, free (any CV)
  N  = null (dropped)
Clear French in [brackets] is fixed context. LM ../ducroc/frn5.npy (5-gram, v->u, j->i).
usage: python solve_regions.py ct.txt ...    env: REGIONS ITERS SEED
"""
import numpy as np, random, math, sys, re, unicodedata, os
lp = np.load(os.environ.get('LM', '../ducroc/frn5.npy')); V = 27
ITERS = int(os.environ.get('ITERS', '300000')); SEED = int(os.environ.get('SEED', '1'))
REGIONS = os.environ.get('REGIONS', '52-399:Sa,400-489:La')
LET = 'abcdefghilmnopqrstuxyz'; LETI = [ord(c) - 97 for c in LET]
CONS = 'bcdfghlmnpqrstxz'; CONSI = [ord(c) - 97 for c in CONS]
VOWI = [ord(c) - 97 for c in 'aeiou']
# 'Ma' = Conde-type single series: each letter followed by its syllables, all in alphabetical order
MIX = []
for c in LET:
    MIX.append((ord(c) - 97,))
    if c in CONS: MIX += [(ord(c) - 97, v) for v in VOWI]

def clean(t):
    t = unicodedata.normalize('NFKD', t.lower()); t = ''.join(c for c in t if not unicodedata.combining(c))
    t = t.replace('v', 'u').replace('j', 'i').replace('k', 'c').replace('w', 'u')
    return re.sub(r'[^a-z]', '', t)

def parse(files):
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

def parse_regions(spec):
    out = []
    for part in spec.split(','):
        rng, kind = part.split(':'); lo, hi = map(int, rng.split('-')); out.append((lo, hi, kind))
    return out

class Model:
    def __init__(self, items, spec):
        self.items = items
        nums = sorted({n for k, n in items if k == 'C'})
        self.regs = []   # dict(kind, nums, mono(list idx), free(list idx))
        self.where = {}
        for lo, hi, kind in parse_regions(spec):
            ns = [n for n in nums if lo <= n <= hi]
            r = {'kind': kind, 'nums': ns}
            self.regs.append(r)
            for i, n in enumerate(ns): self.where[n] = (len(self.regs) - 1, i)
        unassigned = [n for n in nums if n not in self.where]
        if unassigned: raise SystemExit(f'numbers outside regions: {unassigned}')
    def monolen(self, r):
        return {'La': len(LETI), 'Sa': len(CONSI) * 5, 'Sc': len(CONSI), 'Ma': len(MIX)}.get(r['kind'], 0)
    def init_key(self, rnd):
        key = []
        for r in self.regs:
            n = len(r['nums']); L = self.monolen(r)
            mono = [min(L - 1, int(i * L / max(1, n))) for i in range(n)] if L else [0] * n
            if r['kind'] == 'Lf': free = [rnd.randrange(len(LETI)) for _ in range(n)]
            elif r['kind'] == 'Sc': free = [rnd.randrange(5) for _ in range(n)]
            elif r['kind'] == 'Sf': free = [rnd.randrange(len(CONSI) * 5) for _ in range(n)]
            else: free = [0] * n
            key.append([mono, free])
        return key
    def unit(self, r, mono, free):
        k = r['kind']
        if k == 'La': return (LETI[mono],)
        if k == 'Ma': return MIX[mono]
        if k == 'Lf': return (LETI[free],)
        if k == 'Sa': return (CONSI[mono // 5], VOWI[mono % 5])
        if k == 'Sc': return (CONSI[mono], VOWI[free])
        if k == 'Sf': return (CONSI[free // 5], VOWI[free % 5])
        return ()
    def render(self, key):
        out = []
        for k, a in self.items:
            if k == 'P': out.append(a)
            else:
                ri, i = self.where[a]; r = self.regs[ri]
                out.extend(self.unit(r, key[ri][0][i], key[ri][1][i]))
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
                ri, i = self.where[a]; r = self.regs[ri]
                u = self.unit(r, key[ri][0][i], key[ri][1][i])
                s.append((''.join(chr(97 + x) for x in u) or '_') + ' ')
        return ''.join(s)
    def keytable(self, key):
        rows = []
        for ri, r in enumerate(self.regs):
            for i, n in enumerate(r['nums']):
                u = self.unit(r, key[ri][0][i], key[ri][1][i]); rows.append((n, ''.join(chr(97 + x) for x in u) or '-'))
        return rows

def anneal(m, rnd, iters, t0=3.0, t1=0.05):
    key = m.init_key(rnd); cur = m.score(key); best = cur; bestkey = [[k[0][:], k[1][:]] for k in key]
    for it in range(iters):
        T = t0 * (t1 / t0) ** (it / iters)
        ri = rnd.randrange(len(m.regs)); r = m.regs[ri]; ns = r['nums']
        if not ns: continue
        i = rnd.randrange(len(ns)); mono, free = key[ri]; L = m.monolen(r); kind = r['kind']
        undo = None
        u = rnd.random()
        if L and u < 0.5:
            lo = mono[i - 1] if i > 0 else 0; hi = mono[i + 1] if i + 1 < len(mono) else L - 1
            if lo == hi: continue
            new = rnd.randint(lo, hi)
            if new == mono[i]: continue
            undo = ('m', i, mono[i]); mono[i] = new
        elif L and u < 0.65:
            j = min(len(mono), i + rnd.randint(1, 6)); d = rnd.choice((-1, 1)); seg = mono[i:j]
            if d < 0 and ((i > 0 and seg[0] - 1 < mono[i - 1]) or seg[0] - 1 < 0): continue
            if d > 0 and ((j < len(mono) and seg[-1] + 1 > mono[j]) or seg[-1] + 1 >= L): continue
            undo = ('s', i, j, seg[:]); mono[i:j] = [x + d for x in seg]
        else:
            if kind == 'Lf': new = rnd.randrange(len(LETI))
            elif kind == 'Sc': new = rnd.randrange(5)
            elif kind == 'Sf': new = rnd.randrange(len(CONSI) * 5)
            else: continue
            if new == free[i]: continue
            undo = ('f', i, free[i]); free[i] = new
        s = m.score(key)
        if s >= cur or rnd.random() < math.exp((s - cur) / T): cur = s
        else:
            if undo[0] == 'm': mono[undo[1]] = undo[2]
            elif undo[0] == 's': mono[undo[1]:undo[2]] = undo[3]
            else: free[undo[1]] = undo[2]
        if cur > best: best = cur; bestkey = [[k[0][:], k[1][:]] for k in key]
    return best, bestkey

if __name__ == '__main__':
    files = sys.argv[1:]
    items = parse(files); m = Model(items, REGIONS)
    print('tokens', sum(1 for k, _ in items if k == 'C'), 'regions', [(r['kind'], len(r['nums'])) for r in m.regs])
    rnd = random.Random(SEED)
    best, key = anneal(m, rnd, ITERS)
    print('score', round(best, 1))
    print(m.text(key))
    print(' '.join(f'{n}={v}' for n, v in m.keytable(key)))
