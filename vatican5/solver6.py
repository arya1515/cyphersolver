"""Lattice solver for Vatican Challenge Part 5: joint segmentation (1/2-digit symbols, dotted variants) +
substitution, scored by a no-space Italian letter 5-gram LM via Viterbi over chunks. Single digits -> 1 letter;
two-digit codes -> 2-3 letter syllable/word or unused. Simulated annealing over the key with incremental
re-scoring of affected chunks.
"""
import json, math, random, argparse, pathlib, collections, time, sys
from parse5 import load, digit_stream

HERE = pathlib.Path(__file__).parent
ALPHA = 'abcdefghilmnopqrstuz'
VOW = 'aeiou'; CONS = 'bcdfghlmnpqrstz'
SYL = [c + v for c in CONS for v in VOW] + ['qua', 'que', 'qui', 'che', 'chi', 'gli', 'non', 'per', 'con', 'et', 'ss', 'nt', 'st', 'sc', 'gn', 'gl']
UNUSED = ''
# Italian letter frequencies (normalised alphabet, u=u+v, i=i+j), from corpus_it.txt
EXPECT = {'a': .117, 'b': .009, 'c': .045, 'd': .037, 'e': .118, 'f': .010, 'g': .016, 'h': .015, 'i': .113, 'l': .065,
          'm': .025, 'n': .069, 'o': .098, 'p': .031, 'q': .005, 'r': .064, 's': .050, 't': .056, 'u': .051, 'z': .005}

def kl_penalty(counts, mu):
    n = sum(counts.values())
    if n == 0 or mu == 0: return 0.0
    kl = 0.0
    for l, c in counts.items():
        if c: kl += (c / n) * math.log((c / n) / EXPECT.get(l, 1e-3))
    return -mu * n * kl

# ---------------- LM (no spaces) ----------------
class LM:
    def __init__(self, N=5):
        p = HERE / 'it_nospace.json'
        if not p.exists():
            text = (HERE / 'corpus_it.txt').read_text(encoding='utf-8').replace(' ', '')
            g = {}
            for n in range(1, N + 1):
                c = collections.Counter(text[i:i+n] for i in range(len(text) - n + 1))
                g[n] = {k: v for k, v in c.items() if v >= (1 if n < 4 else 2)}
            json.dump(g, open(p, 'w'))
        g = json.load(open(p)); self.N = N
        self.c = [None] + [g[str(n)] for n in range(1, N + 1)]
        self.tot1 = sum(self.c[1].values())
        self.ctx = [None, None] + [collections.Counter() for _ in range(2, N + 1)]
        for n in range(2, N + 1):
            for k, v in self.c[n].items(): self.ctx[n][k[:-1]] += v
        self.cache = {}
    def lp(self, hist, ch):
        key = hist + ch
        v = self.cache.get(key)
        if v is not None: return v
        p = None; w = 1.0
        for n in range(min(self.N, len(hist) + 1), 0, -1):
            h = hist[len(hist) - (n - 1):] if n > 1 else ''
            num = self.c[n].get(h + ch)
            if num:
                den = self.ctx[n][h] if n > 1 else self.tot1
                p = w * num / den; break
            w *= 0.4
        if p is None: p = w * 1e-7
        v = math.log(p); self.cache[key] = v; return v
    def emit(self, hist, s):
        """log prob of string s given history; returns (score, new_hist)"""
        tot = 0.0
        for ch in s:
            tot += self.lp(hist, ch); hist = (hist + ch)[-(self.N - 1):]
        return tot, hist

# ---------------- lattice ----------------
def options(tokens, i):
    """Symbol options starting at token index i: list of (symbol, ntokens)."""
    t = tokens[i]; n = len(tokens); out = []
    if '^' in t:
        out.append((t[0] + '·', 1))                                    # dotted digit as its own symbol
        if i + 1 < n and '^' not in tokens[i+1]: out.append(('·' + tokens[i+1][0], 2))
        if i + 2 < n and '^' not in tokens[i+1] and '^' not in tokens[i+2]: out.append(('·' + tokens[i+1][0] + tokens[i+2][0], 3))
    else:
        out.append((t[0], 1))
        if i + 1 < n and '^' not in tokens[i+1]: out.append((t[0] + tokens[i+1][0], 2))
    return out

class Chunk:
    def __init__(self, tokens, lm):
        self.tokens = tokens; self.lm = lm
        self.opts = [options(tokens, i) for i in range(len(tokens))]
        self.symbols = {s for o in self.opts for s, _ in o}
        self.score = -1e9; self.path = None
    def viterbi(self, key, lam):
        n = len(self.tokens)
        # states: dict hist -> (score, backpointer)
        layers = [dict() for _ in range(n + 1)]
        layers[0][''] = (0.0, None)
        for i in range(n):
            if not layers[i]: continue
            for hist, (sc, _) in layers[i].items():
                for sym, k in self.opts[i]:
                    v = key.get(sym, UNUSED)
                    if v == UNUSED: continue
                    e, nh = self.lm.emit(hist, v)
                    ns = sc + e + lam * len(v)
                    cur = layers[i + k].get(nh)
                    if cur is None or ns > cur[0]:
                        layers[i + k][nh] = (ns, (i, hist, sym))
            # beam: keep best 12 states
            if len(layers[i + 1]) > 12:
                layers[i + 1] = dict(sorted(layers[i + 1].items(), key=lambda x: -x[1][0])[:12])
        end = layers[n]
        if not end:
            self.score = -12.0 * n; self.path = None; self.letters = collections.Counter(); return self.score
        hist, (sc, bp) = max(end.items(), key=lambda x: x[1][0])
        # backtrack
        path = []; i = n; h = hist
        while i > 0:
            pi, ph, sym = layers[i][h][1]
            path.append(sym); i, h = pi, ph
        self.path = path[::-1]; self.score = sc
        self.letters = collections.Counter(ch for sym in self.path for ch in key[sym])
        return sc

class Solver:
    def __init__(self, runs, lm, chunk=80, seed=1, lam=0.0, pairletters=False, mu=0.0):
        self.lm = lm; self.rnd = random.Random(seed); self.lam = lam; self.mu = mu
        self.pairvals = SYL + (list(ALPHA) * 3 if pairletters else [])
        self.chunks = []
        for r in runs:
            for i in range(0, len(r), chunk):
                c = r[i:i + chunk]
                if len(c) >= 6: self.chunks.append(Chunk(c, lm))
        self.symbols = sorted({s for c in self.chunks for s in c.symbols}, key=lambda s: (len(s), s))
        self.sym_chunks = collections.defaultdict(list)
        for ci, c in enumerate(self.chunks):
            for s in c.symbols: self.sym_chunks[s].append(ci)
        self.freq = collections.Counter()
        for c in self.chunks:
            for o in c.opts:
                for s, _ in o: self.freq[s] += 1
        self.key = {}
    def is_single(self, s): return len(s.replace('·', '')) == 1
    def init_key(self, init):
        for s in self.symbols:
            if s in init: self.key[s] = init[s]
            elif self.is_single(s): self.key[s] = self.rnd.choice(ALPHA)
            else: self.key[s] = self.rnd.choice(self.pairvals + [UNUSED] * 60)
        for c in self.chunks: c.viterbi(self.key, self.lam)
        self.letters = sum((c.letters for c in self.chunks), collections.Counter())
    def total(self): return sum(c.score for c in self.chunks) + kl_penalty(self.letters, self.mu)
    def propose(self, s):
        old = self.key[s]
        if self.is_single(s):
            return self.rnd.choice([a for a in ALPHA if a != old])
        r = self.rnd.random()
        if r < 0.25: return UNUSED if old != UNUSED else self.rnd.choice(self.pairvals)
        return self.rnd.choice(self.pairvals)
    def anneal(self, iters, T0=6.0, T1=0.15, fixed=(), log=1000, out=None):
        cur = self.total(); best = cur; bestkey = dict(self.key)
        syms = [s for s in self.symbols if s not in fixed]
        w = [math.sqrt(self.freq[s] + 1) for s in syms]
        t0 = time.time()
        for it in range(iters):
            T = T0 * (T1 / T0) ** (it / iters)
            s = self.rnd.choices(syms, w)[0]
            old = self.key[s]
            swap = None
            if self.rnd.random() < 0.2:
                s2 = self.rnd.choice(syms)
                if s2 == s or self.is_single(s) != self.is_single(s2): continue
                swap = s2; new = self.key[s2]
            else:
                new = self.propose(s)
            if new == old and not swap: continue
            self.key[s] = new
            if swap: self.key[swap] = old
            affected = set(self.sym_chunks[s]) | (set(self.sym_chunks[swap]) if swap else set())
            saved = {ci: (self.chunks[ci].score, self.chunks[ci].path, self.chunks[ci].letters) for ci in affected}
            oldpen = kl_penalty(self.letters, self.mu)
            delta = 0.0
            for ci in affected:
                self.letters -= saved[ci][2]
                delta += self.chunks[ci].viterbi(self.key, self.lam) - saved[ci][0]
                self.letters += self.chunks[ci].letters
            delta += kl_penalty(self.letters, self.mu) - oldpen
            if delta > 0 or self.rnd.random() < math.exp(delta / T):
                cur += delta
                if cur > best: best = cur; bestkey = dict(self.key)
            else:
                self.key[s] = old
                if swap: self.key[swap] = new
                for ci, (sc, p, le) in saved.items():
                    self.letters -= self.chunks[ci].letters
                    self.chunks[ci].score = sc; self.chunks[ci].path = p; self.chunks[ci].letters = le
                    self.letters += le
            if it % log == 0:
                print(f'  it {it:7d} T={T:5.2f} cur={cur:9.1f} best={best:9.1f} {time.time()-t0:.0f}s', flush=True)
                if out: self.dump(out, best, bestkey)
        self.key = bestkey
        for c in self.chunks: c.viterbi(self.key, self.lam)
        self.letters = sum((c.letters for c in self.chunks), collections.Counter())
        return best
    def plaintext(self):
        return ' | '.join(''.join(self.key[s] for s in c.path) if c.path else '?' * len(c.tokens) for c in self.chunks)
    def dump(self, path, best, key):
        saved = dict(self.key); self.key = key
        for c in self.chunks: c.viterbi(self.key, self.lam)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f'BEST {best:.1f}\nKEY:\n')
            for s in self.symbols:
                if key[s] != UNUSED: f.write(f'  {s:4} = {key[s]}\n')
            f.write('\nPLAINTEXT:\n' + self.plaintext() + '\n')
        self.key = saved
        for c in self.chunks: c.viterbi(self.key, self.lam)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--iters', type=int, default=100000); ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--chunk', type=int, default=80); ap.add_argument('--lam', type=float, default=0.0)
    ap.add_argument('--fix', default=''); ap.add_argument('--out', default='result6.txt')
    ap.add_argument('--T0', type=float, default=6.0)
    ap.add_argument('--pairletters', action='store_true', help='allow 2-digit codes to stand for single letters')
    ap.add_argument('--mu', type=float, default=1.0, help='unigram KL penalty weight')
    a = ap.parse_args()
    lm = LM()
    runs = digit_stream(load())
    S = Solver(runs, lm, chunk=a.chunk, seed=a.seed, lam=a.lam, pairletters=a.pairletters, mu=a.mu)
    init = dict(kv.split('=') for kv in a.fix.split(',') if '=' in kv)
    S.init_key(init)
    print(f'{len(S.chunks)} chunks, {len(S.symbols)} symbols, start {S.total():.1f}', flush=True)
    best = S.anneal(a.iters, T0=a.T0, fixed=set(init), log=max(1, a.iters // 50), out=HERE / a.out)
    S.dump(HERE / a.out, best, S.key)
    print(open(HERE / a.out, encoding='utf-8').read()[:5000])

if __name__ == '__main__':
    main()
