# Alphabetical-blocks hypothesis solver, version 2: coordinate descent with an exhaustive scan of each cut
# position, random restarts, optional letter-order permutation moves. Integer symbols only.
import re, random, math, sys, time
from homo import LM, ALPHA, load_tokens

class Blocks2:
    def __init__(self, toks, lm, alpha=ALPHA):
        self.toks = [int(re.match(r'\d+', t).group()) for t in toks if t != '?']
        self.lm = lm; self.alpha = list(alpha)
        self.vals = sorted(set(self.toks)); self.n = len(self.vals)
        self.idx = {v: i for i, v in enumerate(self.vals)}
        self.tokidx = [self.idx[v] for v in self.toks]
        self.k = len(self.alpha)
        self.random_cuts()
    def random_cuts(self):
        self.cuts = sorted(random.sample(range(1, self.n), self.k - 1))
    def letters(self):
        # letter for each sorted value index
        out = []; b = 0; bounds = self.cuts + [self.n]
        for i in range(self.n):
            while i >= bounds[b]: b += 1
            out.append(self.alpha[b])
        return out
    def score(self):
        L = self.letters()
        return self.lm.score(''.join(L[i] for i in self.tokidx))
    def sweep(self):
        improved = False
        for j in random.sample(range(len(self.cuts)), len(self.cuts)):
            lo = self.cuts[j-1] + 1 if j > 0 else 1
            hi = self.cuts[j+1] - 1 if j + 1 < len(self.cuts) else self.n - 1
            best = None
            for p in range(lo, hi + 1):
                self.cuts[j] = p; s = self.score()
                if best is None or s > best[0]: best = (s, p)
            self.cuts[j] = best[1]
            if best[0] > self.cur + 1e-9: improved = True
            self.cur = best[0]
        return improved
    def perm_sweep(self):
        improved = False
        for a in range(self.k):
            for b in range(a + 1, self.k):
                self.alpha[a], self.alpha[b] = self.alpha[b], self.alpha[a]
                s = self.score()
                if s > self.cur + 1e-9: self.cur = s; improved = True
                else: self.alpha[a], self.alpha[b] = self.alpha[b], self.alpha[a]
        return improved
    def solve(self, restarts=20, permute=False, log=True):
        best = -1e18; bestc = None; besta = None; t0 = time.time()
        for r in range(restarts):
            self.random_cuts(); self.cur = self.score()
            while True:
                imp = self.sweep()
                if permute: imp = self.perm_sweep() or imp
                if not imp: break
            if self.cur > best: best = self.cur; bestc = list(self.cuts); besta = list(self.alpha)
            if log: print(f'restart {r} score {self.cur:.1f} best {best:.1f} {time.time()-t0:.0f}s', flush=True)
        self.cuts = bestc; self.alpha = besta; self.cur = best
        return best
    def render(self):
        L = self.letters(); return ''.join(L[i] for i in self.tokidx)
    def table(self):
        L = self.letters(); out = []
        for ch in self.alpha:
            vs = [self.vals[i] for i in range(self.n) if L[i] == ch]
            out.append((ch, vs[0] if vs else None, vs[-1] if vs else None))
        return out

if __name__ == '__main__':
    lmfile, path, restarts, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    permute = len(sys.argv) > 5 and sys.argv[5] == 'p'
    random.seed(seed)
    lm = LM(lmfile); toks = load_tokens(path)
    B = Blocks2(toks, lm)
    best = B.solve(restarts, permute=permute)
    t = B.render(); print('BEST', round(best, 1), 'per-letter', round(best / len(t), 3)); print(t); print('TABLE', B.table())
