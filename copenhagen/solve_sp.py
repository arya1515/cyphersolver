"""solve_sp.py -- Copenhagen cryptogram under the hypothesis that the dotted strokes are WORD SEPARATORS.

Variants:
  strokesp    : B and F (\\. and /.) and | are word boundaries, the free dot D is dropped -> 17 letter symbols, 24 words
  strokesp_Nn : as above with the dotted n merged into n
  strokesp_D  : as above but the free dot is a letter
Scoring uses a character 5-gram LM trained WITH spaces, so word shapes count, plus dictionary coverage.
usage: python solve_sp.py --corpus DIR [--langs ...] [--restarts 60] [--iters 20000]
"""
import sys, re, math, random, collections, pathlib, pickle
HERE = pathlib.Path(__file__).parent
import solve as cp

class SpacedLM(cp.LM):
    def __init__(self, text):
        t = ' ' + re.sub(r'\s+', ' ', text).strip() + ' '
        self.counts = collections.Counter(); self.ctxtot = collections.Counter(); self.ctxtypes = collections.Counter()
        for n in range(2, cp.N + 1):
            for i in range(len(t) - n + 1): self.counts[t[i:i+n]] += 1
        for g, c in self.counts.items(): self.ctxtot[g[:-1]] += c; self.ctxtypes[g[:-1]] += 1
        uni = collections.Counter(t); tot = sum(uni.values())
        self.uni = {c: (v + 1) / (tot + 40) for c, v in uni.items()}
        self.letters = [c for c in sorted(uni, key=lambda c: -uni[c]) if c != ' ']
        words = t.split(); wc = collections.Counter(words)
        self.vocab = {w for w, c in wc.items() if c >= 3 and len(w) >= 3}
        self.wordset = {w for w, c in wc.items() if c >= 2}
        self.memo = {}
        self.counts = {g: c for g, c in self.counts.items() if c >= 2 or len(g) <= 3}
    def score(self, segments):
        t = ' ' + ' '.join(segments) + ' '
        s = 0.0; hist = ''
        for c in t[1:]:
            s += self.logp(hist, c); hist = (hist + c)[-4:]
        return s
    def wordhits(self, segments):
        return sum(1 for w in segments if w in self.wordset), len(segments)

def build(lang):
    cache = HERE / f'lmsp_{lang}.bin'
    if cache.exists():
        d = pickle.load(open(cache, 'rb')); lm = SpacedLM.__new__(SpacedLM); lm.__dict__.update(d); lm.memo = {}; return lm
    text = ''
    for f in sorted(cp.CORPUS.glob(f'corp_{lang}_*.txt')):
        raw = f.read_text(encoding='utf-8', errors='ignore')
        m = re.search(r'\*\*\* ?START OF.*?\*\*\*', raw); raw = raw[m.end():] if m else raw
        m = re.search(r'\*\*\* ?END OF', raw); raw = raw[:m.start()] if m else raw
        text += cp.normalize(raw, lang) + ' '
    lm = SpacedLM(text); d = dict(lm.__dict__); d.pop('memo'); pickle.dump(d, open(cache, 'wb'))
    print(f'  spaced LM {lang}: {len(text)} chars', flush=True)
    return lm

def variant(tokens, name):
    out = []
    for t in tokens:
        if t in ('B', 'F', '|'): out.append('|')
        elif t == 'D': out.append('D' if name == 'strokesp_D' else None)
        elif t == 'N' and name == 'strokesp_Nn': out.append('n')
        else: out.append(t)
    return [t for t in out if t]

def solve(lm, tokens, rng, restarts, iters):
    syms = sorted(set(t for t in tokens if t != '|')); letters = lm.letters[:max(len(syms) + 3, 22)]
    def words(m):
        ws = []; cur = []
        for t in tokens:
            if t == '|':
                if cur: ws.append(''.join(cur)); cur = []
            else: cur.append(m[t])
        if cur: ws.append(''.join(cur))
        return ws
    finals = []
    for r in range(restarts):
        pool = letters[:]; rng.shuffle(pool); m = {s: pool[i] for i, s in enumerate(syms)}
        sc = lm.score(words(m)); best = (sc, dict(m))
        for it in range(iters):
            T = 3.0 * (0.05 / 3.0) ** (it / iters); m2 = dict(m); a = rng.choice(syms)
            if rng.random() < 0.5: b = rng.choice(syms); m2[a], m2[b] = m[b], m[a]
            else:
                un = [l for l in letters if l not in m.values()]
                if not un: continue
                m2[a] = rng.choice(un)
            s2 = lm.score(words(m2))
            if s2 >= sc or rng.random() < math.exp((s2 - sc) / T):
                m, sc = m2, s2
                if sc > best[0]: best = (sc, dict(m))
        finals.append(best)
    finals.sort(key=lambda x: -x[0]); out = []; seen = set()
    for sc, m in finals:
        ws = tuple(words(m))
        if ws in seen: continue
        seen.add(ws); out.append((sc, m, list(ws)));
        if len(out) >= 5: break
    return out

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    langs = cp.arg('--langs', 'da,sv,de,no,nl,fr,en,la,is,fi').split(',')
    restarts = int(cp.arg('--restarts', 60)); iters = int(cp.arg('--iters', 20000))
    tokens = cp.load_cipher(); rng = random.Random(int(cp.arg('--seed', 1)))
    results = []
    for lang in langs:
        lm = build(lang)
        for vname in ('strokesp', 'strokesp_Nn', 'strokesp_D'):
            toks = variant(tokens, vname); nl = sum(1 for t in toks if t != '|')
            for rank, (sc, m, ws) in enumerate(solve(lm, toks, rng, restarts, iters)):
                hits, nw = lm.wordhits(ws); cov = lm.coverage(ws)
                results.append((sc / nl, hits / nw, lang, vname, ws, m))
                print(f'{lang:3} {vname:11} #{rank+1} {sc:8.1f} {sc/nl:6.3f}/letter words {hits}/{nw} cov {cov:.2f}  ' + ' '.join(ws), flush=True)
    print('\nranked by whole-word hits then score:')
    for r in sorted(results, key=lambda r: (-r[1], -r[0]))[:10]:
        print(f'words {r[1]:.2f} {r[0]:6.3f} {r[2]} {r[3]:11} ' + ' '.join(r[4]))
        print('    key: ' + ' '.join(f'{k}={v}' for k, v in sorted(r[5].items())))
