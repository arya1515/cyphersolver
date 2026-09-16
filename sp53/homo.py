# Homophonic substitution solver (symbols -> single letters, optional nulls) with simulated annealing and a
# spaceless char n-gram LM. 'blocks' mode: integer symbols in alphabetical blocks of consecutive numbers
# (monotone map), searched over block boundaries; 'blocksp' also permutes the letter order.
import re, random, math, sys, collections, time, pickle

class LM:
    def __init__(self, path, order=None):
        self.N, self.cnts, self.total = pickle.load(open(path, 'rb'))
        if order: self.N = min(order, self.N)
        self.cache = {}
    def logp(self, ctx, ch):
        key = ctx + ch
        v = self.cache.get(key)
        if v is None:
            v = math.log(self._p(ctx, ch, len(ctx) + 1)); self.cache[key] = v
        return v
    def _p(self, ctx, ch, n):
        if n == 1:
            return (self.cnts[1][ch] + 1) / (self.total + 26)
        den = self.cnts[n-1][ctx]
        lower = self._p(ctx[1:], ch, n - 1)
        if den == 0: return lower
        num = self.cnts[n][ctx + ch]; d = 0.75
        return max(num - d, 0) / den + (d * max(1, min(den, 10)) / den) * lower
    def score(self, text):
        s = 0.0
        for i in range(len(text)):
            s += self.logp(text[max(0, i - self.N + 1):i], text[i])
        return s

def train(corpus_path, out, N=6):
    t = open(corpus_path, encoding='utf-8', errors='ignore').read().lower()
    t = re.sub(r'[^a-z]', '', t)
    cnts = [collections.Counter() for _ in range(N + 1)]
    for n in range(1, N + 1):
        c = cnts[n]
        for i in range(len(t) - n + 1): c[t[i:i+n]] += 1
    pickle.dump((N, cnts, len(t)), open(out, 'wb'))
    return len(t)

ALPHA = 'abcdefghiklmnopqrstuvxyz'   # 24-letter early-modern alphabet (i/j, u/v merged)

def load_tokens(path, keep_blank=False):
    toks = []
    for line in open(path, encoding='utf-8'):
        if line.startswith('#'): continue
        parts = [x.strip() for x in line.strip().split(';')]
        toks += [x if x else '?' for x in parts if x or keep_blank]
    return toks

class Homo:
    def __init__(self, toks, lm, alpha=ALPHA, allow_null=False, lam=0.0):
        self.toks = toks; self.lm = lm; self.alpha = alpha
        self.syms = sorted(set(toks), key=lambda s: (len(s), s))
        self.units = list(alpha) + ([''] if allow_null else [])
        self.lam = lam
        self.map = {s: random.choice(alpha) for s in self.syms}
    def render(self, m=None):
        m = m or self.map
        return ''.join(m[t] for t in self.toks)
    def score(self, m=None):
        t = self.render(m)
        return self.lm.score(t) + self.lam * len(t)
    def anneal(self, iters=100000, T0=2.0, T1=0.1, log=0):
        cur = self.score(); best = cur; bestmap = dict(self.map); t0 = time.time()
        for it in range(iters):
            T = T0 * (T1 / T0) ** (it / iters)
            s = random.choice(self.syms)
            if random.random() < 0.9:
                new = random.choice(self.units)
                if new == self.map[s]: continue
                changed = {s: self.map[s]}; self.map[s] = new
            else:
                s2 = random.choice(self.syms)
                if s2 == s or self.map[s2] == self.map[s]: continue
                changed = {s: self.map[s], s2: self.map[s2]}
                self.map[s], self.map[s2] = self.map[s2], self.map[s]
            sc = self.score(); d = sc - cur
            if d >= 0 or random.random() < math.exp(d / T):
                cur = sc
                if cur > best: best = cur; bestmap = dict(self.map)
            else:
                self.map.update(changed)
            if log and it % log == 0:
                print(f'it {it} T {T:.2f} cur {cur:.1f} best {best:.1f} {time.time()-t0:.0f}s', flush=True)
        self.map = bestmap
        return best

class Blocks:
    def __init__(self, toks, lm, alpha=ALPHA, permute=False, lam=0.0):
        self.toks = [int(re.match(r'\d+', t).group()) for t in toks if t != '?']
        self.lm = lm; self.alpha = alpha; self.lam = lam
        self.vals = sorted(set(self.toks)); self.n = len(self.vals)
        k = len(alpha)
        self.cuts = sorted(random.sample(range(1, self.n), k - 1))
        self.order = list(alpha); self.permute = permute
    def mapping(self):
        m = {}; b = 0; bounds = self.cuts + [self.n]
        for i, v in enumerate(self.vals):
            while i >= bounds[b]: b += 1
            m[v] = self.order[b]
        return m
    def score(self):
        m = self.mapping(); t = ''.join(m[v] for v in self.toks)
        return self.lm.score(t) + self.lam * len(t)
    def anneal(self, iters=50000, T0=2.0, T1=0.1, log=0):
        cur = self.score(); best = cur; bestc = list(self.cuts); besto = list(self.order)
        for it in range(iters):
            T = T0 * (T1 / T0) ** (it / iters)
            oldc = list(self.cuts); oldo = list(self.order)
            if random.random() < 0.8 or not self.permute:
                j = random.randrange(len(self.cuts))
                lo = self.cuts[j-1] + 1 if j > 0 else 1
                hi = self.cuts[j+1] - 1 if j + 1 < len(self.cuts) else self.n - 1
                if hi < lo: continue
                self.cuts[j] = random.randint(lo, hi) if random.random() < 0.5 else min(hi, max(lo, self.cuts[j] + random.choice([-2, -1, 1, 2])))
            else:
                a, b = random.sample(range(len(self.order)), 2)
                self.order[a], self.order[b] = self.order[b], self.order[a]
            sc = self.score(); d = sc - cur
            if d >= 0 or random.random() < math.exp(d / T):
                cur = sc
                if cur > best: best = cur; bestc = list(self.cuts); besto = list(self.order)
            else:
                self.cuts = oldc; self.order = oldo
            if log and it % log == 0:
                print(f'it {it} T {T:.2f} cur {cur:.1f} best {best:.1f}', flush=True)
        self.cuts = bestc; self.order = besto
        return best

if __name__ == '__main__':
    mode, lmfile, path, iters, seed = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    random.seed(seed)
    lm = LM(lmfile); toks = load_tokens(path)
    if mode == 'homo':
        H = Homo(toks, lm)
        best = H.anneal(iters, log=iters // 10)
        t = H.render(); print('BEST', round(best, 1), 'per-letter', round(best / len(t), 3)); print(t)
        print('MAP', sorted(H.map.items(), key=lambda x: (len(x[0]), x[0])))
    else:
        B = Blocks(toks, lm, permute=(mode == 'blocksp'))
        best = B.anneal(iters, log=iters // 10)
        m = B.mapping(); t = ''.join(m[v] for v in B.toks)
        print('BEST', round(best, 1), 'per-letter', round(best / len(t), 3)); print(t)
        print('BLOCKS', [(B.order[k], B.vals[(B.cuts[k-1] if k else 0)], B.vals[(B.cuts[k] if k < len(B.cuts) else B.n) - 1]) for k in range(len(B.order))])
