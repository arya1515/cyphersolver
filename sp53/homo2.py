# Stronger homophonic solver: frequency-ranked initialisation, incremental scoring of only the affected
# positions, many iterations with restarts, and a pass that tries every letter for every symbol at the end.
import re, random, math, sys, collections, time
from homo import LM, ALPHA, load_tokens

class Homo2:
    def __init__(self, toks, lm, alpha=ALPHA, lang_freq=None):
        self.toks = toks; self.lm = lm; self.alpha = alpha; self.N = lm.N
        self.syms = sorted(set(toks), key=lambda s: -toks.count(s))
        self.pos = collections.defaultdict(list)
        for i, t in enumerate(toks): self.pos[t].append(i)
        self.lang_freq = lang_freq or alpha
        self.init()
    def init(self):
        # frequency-ranked: most frequent symbols get the most frequent letters, cycling with noise
        self.map = {}
        order = list(self.lang_freq)
        k = 0
        for s in self.syms:
            self.map[s] = order[min(len(order) - 1, int(k))]
            k += len(order) / max(1, len(self.syms) / 2.2)
            if k >= len(order): k = random.random() * 3
        self.text = [self.map[t] for t in self.toks]
        self.total = self.full_score()
    def full_score(self):
        return self.lm.score(''.join(self.text))
    def local(self, positions):
        # score contributions of windows touched by the given positions
        s = 0.0; n = len(self.text); N = self.N; txt = self.text
        seen = set()
        for p in positions:
            for i in range(p, min(n, p + N)):
                if i in seen: continue
                seen.add(i)
                ctx = ''.join(txt[max(0, i - N + 1):i])
                s += self.lm.logp(ctx, txt[i])
        return s
    def try_change(self, changes, T):
        positions = sorted(set(p for s in changes for p in self.pos[s]))
        before = self.local(positions)
        old = {s: self.map[s] for s in changes}
        for s, u in changes.items():
            self.map[s] = u
            for p in self.pos[s]: self.text[p] = u
        after = self.local(positions)
        d = after - before
        if d >= 0 or (T > 0 and random.random() < math.exp(d / T)):
            self.total += d; return True
        for s, u in old.items():
            self.map[s] = u
            for p in self.pos[s]: self.text[p] = u
        return False
    def anneal(self, iters, T0=3.0, T1=0.05, log=0):
        best = self.total; bestmap = dict(self.map); t0 = time.time()
        for it in range(iters):
            T = T0 * (T1 / T0) ** (it / iters)
            s = random.choice(self.syms)
            if random.random() < 0.85:
                u = random.choice(self.alpha)
                if u == self.map[s]: continue
                self.try_change({s: u}, T)
            else:
                s2 = random.choice(self.syms)
                if s2 == s or self.map[s2] == self.map[s]: continue
                self.try_change({s: self.map[s2], s2: self.map[s]}, T)
            if self.total > best: best = self.total; bestmap = dict(self.map)
            if log and it % log == 0:
                print(f'it {it} T {T:.2f} cur {self.total:.1f} best {best:.1f} {time.time()-t0:.0f}s', flush=True)
        self.set(bestmap)
        # greedy polish
        improved = True
        while improved:
            improved = False
            for s in self.syms:
                for u in self.alpha:
                    if u != self.map[s] and self.try_change({s: u}, 0): improved = True
        return self.total
    def set(self, m):
        self.map = dict(m); self.text = [self.map[t] for t in self.toks]; self.total = self.full_score()
    def render(self): return ''.join(self.text)

if __name__ == '__main__':
    lmfile, path, iters, restarts, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    random.seed(seed)
    lm = LM(lmfile); toks = load_tokens(path)
    freq = {'en': 'etaoinshrdlucmfwypvbgk', 'fr': 'esaitnrulodcpmvqfgbhxyz', 'es': 'eaosrnidltcumpbgvyqhfz', 'it': 'eaionlrtscdupmvghfbqz'}
    lang = re.match(r'([a-z]+)', lmfile).group(1)
    H = Homo2(toks, lm, lang_freq=[c for c in freq.get(lang, ALPHA) if c in ALPHA])
    best = -1e9; bestmap = None
    for r in range(restarts):
        if r: H.init()
        sc = H.anneal(iters, log=0)
        print(f'restart {r} score {sc:.1f} per-letter {sc/len(toks):.3f}', flush=True)
        if sc > best: best = sc; bestmap = dict(H.map)
    H.set(bestmap)
    print('BEST', round(best, 1), 'per-letter', round(best / len(toks), 3)); print(H.render())
    print('MAP', sorted(H.map.items(), key=lambda x: (len(x[0]), x[0])))
