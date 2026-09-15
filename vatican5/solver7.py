"""solver7: structured lattice solver for Vatican Challenge Part 5.

Structure (from digit-class analysis: adjacent digits alternate between classes {0,1,2,7,9} and {3,4,5,6,8} 64% of the time,
i.e. like vowel/consonant alternation in Italian):
  * vowel digits  V = one class  -> a permutation of a e i o u
  * consonant digits C = other class -> each a SET of 1..3 consonants (polyphonic; Viterbi picks per occurrence)
  * two-digit codes  -> CV syllable / short word or UNUSED
  * dotted codes ('·xy', '·x', 'x·') -> word/syllable or UNUSED
Scored by no-space Italian 5-gram LM (Viterbi over chunks), + unigram KL penalty. Simulated annealing.
"""
import math, random, argparse, pathlib, collections, time, itertools
from parse5 import load, digit_stream
from solver6 import LM, options, kl_penalty, EXPECT

HERE = pathlib.Path(__file__).parent
VOW = 'aeiou'; CONS = 'bcdfghlmnpqrstz'
SYL = [c + v for c in CONS for v in VOW] + ['qua', 'que', 'qui', 'che', 'chi', 'gli', 'non', 'per', 'con', 'et', 'ns', 'sm']
UNUSED = ()

class Chunk:
    def __init__(self, tokens, lm):
        self.tokens = tokens; self.lm = lm
        self.opts = [options(tokens, i) for i in range(len(tokens))]
        self.symbols = {s for o in self.opts for s, _ in o}
        self.score = -1e9; self.path = None; self.letters = collections.Counter()
    def viterbi(self, key, beam=10):
        n = len(self.tokens)
        layers = [dict() for _ in range(n + 1)]
        layers[0][''] = (0.0, None)
        for i in range(n):
            L = layers[i]
            if not L: continue
            if len(L) > beam:
                L = dict(sorted(L.items(), key=lambda x: -x[1][0])[:beam]); layers[i] = L
            for hist, (sc, _) in L.items():
                for sym, k in self.opts[i]:
                    for v in key.get(sym, UNUSED):
                        e, nh = self.lm.emit(hist, v)
                        ns = sc + e
                        cur = layers[i + k].get(nh)
                        if cur is None or ns > cur[0]:
                            layers[i + k][nh] = (ns, (i, hist, sym, v))
        end = layers[n]
        if not end:
            self.score = -12.0 * n; self.path = None; self.letters = collections.Counter(); return self.score
        hist, (sc, bp) = max(end.items(), key=lambda x: x[1][0])
        path = []; i = n; h = hist
        while i > 0:
            pi, ph, sym, v = layers[i][h][1]
            path.append((sym, v)); i, h = pi, ph
        self.path = path[::-1]; self.score = sc
        self.letters = collections.Counter(ch for _, v in self.path for ch in v)
        return sc

class Solver:
    def __init__(self, runs, lm, vowels, chunk=80, seed=1, mu=0.5):
        self.lm = lm; self.rnd = random.Random(seed); self.mu = mu
        self.V = set(vowels); self.C = set('0123456789') - self.V
        self.chunks = [Chunk(r[i:i+chunk], lm) for r in runs for i in range(0, len(r), chunk) if len(r[i:i+chunk]) >= 6]
        self.symbols = sorted({s for c in self.chunks for s in c.symbols}, key=lambda s: (len(s), s))
        self.sym_chunks = collections.defaultdict(list)
        for ci, c in enumerate(self.chunks):
            for s in c.symbols: self.sym_chunks[s].append(ci)
        self.freq = collections.Counter(s for c in self.chunks for o in c.opts for s, _ in o)
        self.key = {}
    def kind(self, s):
        d = s.replace('·', '')
        if len(d) == 1: return 'V' if d in self.V else 'C'
        return 'P'
    def init_key(self, init):
        perm = list(VOW); self.rnd.shuffle(perm)
        vd = sorted(self.V)
        for s in self.symbols:
            if s in init: self.key[s] = tuple(init[s].split('/')); continue
            k = self.kind(s)
            if k == 'V':
                self.key[s] = (perm[vd.index(s[0])],) if s in vd else (self.rnd.choice(VOW),)
            elif k == 'C':
                self.key[s] = tuple(self.rnd.sample(CONS, 2))
            else:
                self.key[s] = (self.rnd.choice(SYL),) if self.rnd.random() < 0.3 else UNUSED
        self.rescore_all()
    def rescore_all(self):
        for c in self.chunks: c.viterbi(self.key)
        self.letters = sum((c.letters for c in self.chunks), collections.Counter())
    def total(self): return sum(c.score for c in self.chunks) + kl_penalty(self.letters, self.mu)
    def propose(self, s):
        """return dict of {symbol: newvalue} changes"""
        k = self.kind(s); old = self.key[s]
        if k == 'V':
            # swap vowel with another vowel digit (keep permutation), or (rarely) set free
            others = [t for t in self.symbols if t != s and self.kind(t) == 'V' and len(t) == 1]
            t = self.rnd.choice(others)
            return {s: self.key[t], t: old}
        if k == 'C':
            cur = set(old); r = self.rnd.random()
            if r < 0.4 and len(cur) < 3: cur.add(self.rnd.choice([c for c in CONS if c not in cur]))
            elif r < 0.7 and len(cur) > 1: cur.discard(self.rnd.choice(list(cur)))
            else:
                if cur: cur.discard(self.rnd.choice(list(cur)))
                cur.add(self.rnd.choice([c for c in CONS if c not in cur]))
            return {s: tuple(sorted(cur))}
        # pair / dotted
        r = self.rnd.random()
        if old == UNUSED: return {s: (self.rnd.choice(SYL),)}
        if r < 0.3: return {s: UNUSED}
        if r < 0.5:
            others = [t for t in self.symbols if t != s and self.kind(t) == 'P' and self.key[t] != UNUSED]
            if others:
                t = self.rnd.choice(others); return {s: self.key[t], t: old}
        return {s: (self.rnd.choice(SYL),)}
    def anneal(self, iters, T0=5.0, T1=0.1, fixed=(), log=1000, out=None):
        cur = self.total(); best = cur; bestkey = dict(self.key)
        syms = [s for s in self.symbols if s not in fixed]
        w = [math.sqrt(self.freq[s] + 1) for s in syms]
        t0 = time.time()
        for it in range(iters):
            T = T0 * (T1 / T0) ** (it / iters)
            s = self.rnd.choices(syms, w)[0]
            changes = self.propose(s)
            if any(t in fixed for t in changes): continue
            olds = {t: self.key[t] for t in changes}
            if all(self.key[t] == v for t, v in changes.items()): continue
            self.key.update(changes)
            affected = set().union(*(self.sym_chunks[t] for t in changes))
            saved = {ci: (self.chunks[ci].score, self.chunks[ci].path, self.chunks[ci].letters) for ci in affected}
            oldpen = kl_penalty(self.letters, self.mu); delta = 0.0
            for ci in affected:
                self.letters -= saved[ci][2]
                delta += self.chunks[ci].viterbi(self.key) - saved[ci][0]
                self.letters += self.chunks[ci].letters
            delta += kl_penalty(self.letters, self.mu) - oldpen
            if delta > 0 or self.rnd.random() < math.exp(delta / T):
                cur += delta
                if cur > best: best = cur; bestkey = dict(self.key)
            else:
                self.key.update(olds)
                for ci, (sc, p, le) in saved.items():
                    self.letters -= self.chunks[ci].letters
                    self.chunks[ci].score = sc; self.chunks[ci].path = p; self.chunks[ci].letters = le
                    self.letters += le
            if it % log == 0:
                print(f'  it {it:7d} T={T:5.2f} cur={cur:9.1f} best={best:9.1f} {time.time()-t0:.0f}s', flush=True)
                if out: self.dump(out, best, bestkey)
        self.key = bestkey; self.rescore_all()
        return best
    def plaintext(self):
        return ' | '.join(''.join(v for _, v in c.path) if c.path else '?' * len(c.tokens) for c in self.chunks)
    def dump(self, path, best, key):
        saved = dict(self.key); self.key = key; self.rescore_all()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f'BEST {best:.1f}\nVOWELS {"".join(sorted(self.V))}\nKEY:\n')
            for s in self.symbols:
                if key[s] != UNUSED: f.write(f'  {s:4} = {"/".join(key[s])}\n')
            f.write('\nPLAINTEXT:\n' + self.plaintext() + '\n')
        self.key = saved; self.rescore_all()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--vowels', default='01279'); ap.add_argument('--iters', type=int, default=60000)
    ap.add_argument('--seed', type=int, default=1); ap.add_argument('--mu', type=float, default=0.5)
    ap.add_argument('--chunk', type=int, default=80); ap.add_argument('--fix', default='')
    ap.add_argument('--out', default='result7.txt'); ap.add_argument('--T0', type=float, default=5.0)
    a = ap.parse_args()
    lm = LM(); runs = digit_stream(load())
    S = Solver(runs, lm, a.vowels, chunk=a.chunk, seed=a.seed, mu=a.mu)
    init = dict(kv.split('=') for kv in a.fix.split(',') if '=' in kv)
    S.init_key(init)
    print(f'{len(S.chunks)} chunks, {len(S.symbols)} symbols, vowels={a.vowels}, start {S.total():.1f}', flush=True)
    best = S.anneal(a.iters, T0=a.T0, fixed=set(init), log=max(1, a.iters // 40), out=HERE / a.out)
    S.dump(HERE / a.out, best, S.key)
    print(open(HERE / a.out, encoding='utf-8').read()[:4000])

if __name__ == '__main__':
    main()
