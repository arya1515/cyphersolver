"""Joint segmentation + substitution solver for Vatican Challenge Part 5.

Model (from Meister's 1539-1548 'cifre vecchie' family):
  * digit NULLD (default '7') is a null / word separator
  * remaining single digits = letters
  * two-digit groups = letters or syllables (1-3 plaintext chars)
  * a dot over a digit ('^') marks the following code: we model '·x' and '·xy' as separate symbols
Search: simulated annealing over the key (symbol -> plaintext string); each word is parsed by exhaustive
segmentation into 1/2-digit symbols and scored by a character 5-gram LM (with spaces) built from
16th-c. papal Italian. Incremental re-scoring of only the affected words.
"""
import json, math, random, sys, argparse, pathlib, collections, time
from parse5 import load, digit_stream

HERE = pathlib.Path(__file__).parent
ALPHA = 'abcdefghilmnopqrstuz'
VOWELS = 'aeiou'
CONS = 'bcdfghlmnpqrstz'
SYLLS = [c + v for c in CONS for v in VOWELS] + ['qua', 'que', 'qui', 'che', 'chi', 'gli', 'gn', 'sc', 'st', 'non', 'per', 'con', 'et']
VALUES = list(ALPHA) + SYLLS          # candidate plaintext values for a symbol
UNUSED = ''                            # symbol may be unused (parse will avoid it: score -inf)
LAMBDA = 1.6                           # per-output-char reward (~ mean |log p|), so longer parses are not penalised

# ---------------- LM ----------------
class LM:
    def __init__(self, path=HERE / 'it_ngrams.json', N=5):
        g = json.load(open(path)); self.N = N
        self.c = [None] + [g[str(n)] for n in range(1, N + 1)]
        self.tot1 = sum(self.c[1].values())
        # precompute context totals for n>=2
        self.ctx = [None, None] + [collections.Counter() for _ in range(2, N + 1)]
        for n in range(2, N + 1):
            for k, v in self.c[n].items(): self.ctx[n][k[:-1]] += v
        self.cache = {}
        self.scache = {}
    def logp_char(self, hist, ch):
        key = hist + ch
        if key in self.cache: return self.cache[key]
        # interpolated backoff (stupid backoff with 0.4)
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
    def score(self, s):
        """score ' word ' with leading/trailing space context (cached by string)."""
        v = self.scache.get(s)
        if v is not None: return v
        t = ' ' + s + ' '
        tot = 0.0
        for i in range(1, len(t)):
            tot += self.logp_char(t[max(0, i - self.N + 1):i], t[i])
        if len(self.scache) > 3_000_000: self.scache.clear()
        self.scache[s] = tot
        return tot

# ---------------- ciphertext ----------------
def words_from_runs(runs, nulld):
    """Split runs on the null digit; keep marks. Each word = list of tokens (digit[+marks])."""
    words = []
    for r in runs:
        cur = []
        for t in r:
            if t[0] == nulld and '^' not in t:      # undotted null = separator
                if cur: words.append(cur); cur = []
            else:
                cur.append(t)
        if cur: words.append(cur)
    return words

def segmentations(word, maxlen=2):
    """All ways to split token list into symbols of 1..maxlen digits; a dotted token starts a dotted symbol
    '·x'/'·xy' where the dotted digit itself is dropped (dot marks the following code) -- and alternatively
    is kept as a plain digit. Yields list of symbol strings."""
    n = len(word)
    out = []
    def rec(i, acc):
        if len(out) >= 400: return
        if i == n: out.append(tuple(acc)); return
        t = word[i]; dotted = '^' in t
        if dotted:
            # option A: dot marks following code -> '·' + next 1 or 2 digits (skip the dotted digit)
            for L in (1, 2):
                if i + L < n and all('^' not in x for x in word[i+1:i+1+L]):
                    rec(i + 1 + L, acc + ['·' + ''.join(x[0] for x in word[i+1:i+1+L])])
            # option B: dotted digit is itself a (special) single symbol
            rec(i + 1, acc + [t[0] + '·'])
        else:
            for L in range(1, maxlen + 1):
                if i + L <= n and all('^' not in x for x in word[i:i+L]):
                    rec(i + L, acc + [''.join(x[0] for x in word[i:i+L])])
    rec(0, [])
    return out

# ---------------- solver ----------------
class Solver:
    def __init__(self, words, lm, seed=1):
        self.lm = lm; self.rnd = random.Random(seed)
        self.words = words
        self.segs = [segmentations(w) for w in words]
        self.symbols = sorted({s for segs in self.segs for seg in segs for s in seg})
        self.sym_words = collections.defaultdict(set)
        for wi, segs in enumerate(self.segs):
            for seg in segs:
                for s in seg: self.sym_words[s].add(wi)
        self.freq = collections.Counter(s for segs in self.segs for seg in segs for s in seg)
        self.key = {}
        self.wscore = [0.0] * len(words)
        self.wbest = [None] * len(words)
    def init_key(self, init=None):
        for s in self.symbols:
            if init and s in init: self.key[s] = init[s]; continue
            if len(s.replace('·', '')) == 1: self.key[s] = self.rnd.choice(ALPHA)
            else: self.key[s] = self.rnd.choice(VALUES + [UNUSED] * 30)
        for wi in range(len(self.words)): self.score_word(wi)
    def score_word(self, wi):
        best, bseg = -1e9, None
        for seg in self.segs[wi]:
            pl = []
            ok = True
            for s in seg:
                v = self.key.get(s, UNUSED)
                if v == UNUSED: ok = False; break
                pl.append(v)
            if not ok: continue
            sc = self.lm.score(''.join(pl)) + LAMBDA * (sum(map(len, pl)) + 1)   # length-normalized
            if sc > best: best, bseg = sc, seg
        if bseg is None: best = -8.0 * len(self.words[wi])
        self.wscore[wi] = best; self.wbest[wi] = bseg
        return best
    def total(self): return sum(self.wscore)
    def anneal(self, iters, T0=8.0, T1=0.2, fixed=(), log=None):
        cur = self.total(); best = cur; bestkey = dict(self.key)
        syms = [s for s in self.symbols if s not in fixed]
        weights = [math.sqrt(self.freq[s] + 1) for s in syms]
        t0 = time.time()
        for it in range(iters):
            T = T0 * (T1 / T0) ** (it / iters)
            s = self.rnd.choices(syms, weights)[0]
            old = self.key[s]
            swap = None
            r = self.rnd.random()
            if r < 0.2:
                # swap values of two symbols of the same length class
                s2 = self.rnd.choice(syms)
                if s2 == s or (len(s.replace('·', '')) == 1) != (len(s2.replace('·', '')) == 1): continue
                swap = s2; new = self.key[s2]
            elif r < 0.32 and len(s.replace('·', '')) > 1:
                new = UNUSED
            elif len(s.replace('·', '')) == 1 or self.rnd.random() < 0.6:
                new = self.rnd.choice(ALPHA)
            else:
                new = self.rnd.choice(VALUES)
            if new == old: continue
            self.key[s] = new
            if swap: self.key[swap] = old
            affected = set(self.sym_words[s]) | (set(self.sym_words[swap]) if swap else set())
            saved = {wi: (self.wscore[wi], self.wbest[wi]) for wi in affected}
            delta = 0.0
            for wi in affected:
                delta += self.score_word(wi) - saved[wi][0]
            if delta > 0 or self.rnd.random() < math.exp(delta / T):
                cur += delta
                if cur > best: best = cur; bestkey = dict(self.key)
            else:
                self.key[s] = old
                if swap: self.key[swap] = new
                for wi, (sc, bs) in saved.items(): self.wscore[wi] = sc; self.wbest[wi] = bs
            if log and it % log == 0:
                print(f'  it {it:7d} T={T:5.2f} cur={cur:9.1f} best={best:9.1f}  {time.time()-t0:.0f}s', flush=True)
        self.key = bestkey
        for wi in range(len(self.words)): self.score_word(wi)
        return best
    def plaintext(self):
        out = []
        for wi, seg in enumerate(self.wbest):
            out.append(''.join(self.key[s] for s in seg) if seg else '?' * len(self.words[wi]))
        return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--null', default='7'); ap.add_argument('--iters', type=int, default=200000)
    ap.add_argument('--restarts', type=int, default=3); ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--fix', default='', help='sym=val,sym=val (val may be empty for unused)')
    ap.add_argument('--out', default='result5.txt')
    ap.add_argument('--maxword', type=int, default=14)
    a = ap.parse_args()
    lm = LM()
    runs = digit_stream(load())
    words = [w for w in words_from_runs(runs, a.null) if len(w) <= a.maxword]
    print(f'{len(words)} words (<= {a.maxword} digits), avg len {sum(map(len, words))/len(words):.1f}')
    init = {}
    for kv in a.fix.split(','):
        if '=' in kv: k, v = kv.split('='); init[k] = v
    results = []
    for r in range(a.restarts):
        S = Solver(words, lm, seed=a.seed + r)
        S.init_key(init)
        print(f'restart {r}: {len(S.symbols)} symbols; start {S.total():.1f}')
        t0 = time.time()
        best = S.anneal(a.iters, fixed=set(init), log=max(1, a.iters // 20))
        print(f'restart {r}: best {best:.1f} ({time.time()-t0:.0f}s)')
        results.append((best, dict(S.key), S.plaintext()))
    results.sort(key=lambda x: -x[0])
    best, key, pt = results[0]
    with open(HERE / a.out, 'w', encoding='utf-8') as f:
        f.write(f'BEST {best:.1f}\nKEY:\n')
        for s in sorted(key, key=lambda x: (len(x), x)):
            if key[s] != UNUSED: f.write(f'  {s:4} = {key[s]}\n')
        f.write('\nPLAINTEXT:\n' + ' '.join(pt) + '\n')
    print(open(HERE / a.out, encoding='utf-8').read()[:6000])

if __name__ == '__main__':
    main()
