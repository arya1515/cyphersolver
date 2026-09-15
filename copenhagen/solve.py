"""solve.py -- simple-substitution attack on the Copenhagen cryptogram in several languages.

Builds a no-space character 5-gram LM per language from Gutenberg texts (corp_<lang>_*.txt in --corpus dir),
then anneals an injective symbol->letter mapping for each language and each token-convention variant:
  full      : every symbol is a letter (20 symbols); | is a sentence boundary
  nodot     : the free dot D is dropped
  dotsp     : the free dot D is a boundary
  dotattach : the free dot D fuses with the following stroke (DB, DF become symbols of their own)
  barletter : the long stroke | is a letter too, no boundaries
  Nn        : the dotted n is the same letter as n
Each run keeps the best result of every restart; the top candidates are re-ranked by dictionary coverage
(fraction of letters covered by corpus words of 3+ letters, greedy longest match), which the annealer does
not optimise and which therefore acts as an independent check.

usage: python solve.py --corpus DIR [--langs da,sv,de,no,nl,fr,en,la] [--variants full,nodot,...]
                       [--restarts 60] [--iters 20000] [--tag name]
"""
import sys, re, math, random, collections, pathlib, unicodedata, pickle
HERE = pathlib.Path(__file__).parent

def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default
CORPUS = pathlib.Path(arg('--corpus', '.'))
LANGS = arg('--langs', 'da,sv,de,no,nl,fr,en,la').split(',')
VARIANTS = arg('--variants', 'full,nodot,dotsp,dotattach,barletter,Nn').split(',')
RESTARTS = int(arg('--restarts', 60)); ITERS = int(arg('--iters', 20000))
N = 5; D = 0.75

ALPHA = {'da': 'abcdefghijklmnopqrstuvwxyzæøå', 'no': 'abcdefghijklmnopqrstuvwxyzæøå', 'sv': 'abcdefghijklmnopqrstuvwxyzåäö',
         'de': 'abcdefghijklmnopqrstuvwxyzäöüß', 'nds': 'abcdefghijklmnopqrstuvwxyzäöüß', 'nl': 'abcdefghijklmnopqrstuvwxyz',
         'fr': 'abcdefghijklmnopqrstuvwxyz', 'en': 'abcdefghijklmnopqrstuvwxyz', 'la': 'abcdefghiklmnopqrstuvxyz',
         'is': 'abcdefghijklmnopqrstuvwxyzáéíóúýþæöð', 'fi': 'abcdefghijklmnopqrstuvwxyzäö'}

def normalize(text, lang):
    text = text.lower(); keep = ALPHA[lang]; out = []
    for ch in text:
        if ch in keep or ch == ' ' or ch == '\n': out.append(ch if ch != '\n' else ' ')
        else:
            base = unicodedata.normalize('NFKD', ch); base = ''.join(c for c in base if not unicodedata.combining(c))
            out.append(base if base and base in keep else ' ')
    return re.sub(r'\s+', ' ', ''.join(out))

class LM:
    def __init__(self, text):
        ns = text.replace(' ', '')
        self.counts = collections.Counter(); self.ctxtot = collections.Counter(); self.ctxtypes = collections.Counter()
        for n in range(2, N + 1):
            for i in range(len(ns) - n + 1): self.counts[ns[i:i+n]] += 1
        for g, c in self.counts.items(): self.ctxtot[g[:-1]] += c; self.ctxtypes[g[:-1]] += 1
        uni = collections.Counter(ns); tot = sum(uni.values())
        self.uni = {c: (v + 1) / (tot + 40) for c, v in uni.items()}
        self.letters = sorted(uni, key=lambda c: -uni[c])
        words = text.split()
        ini = collections.Counter(w[0] for w in words if w); fin = collections.Counter(w[-1] for w in words if w)
        self.ini = {c: (ini[c] + 1) / (sum(ini.values()) + 40) for c in self.uni}
        self.fin = {c: (fin[c] + 1) / (sum(fin.values()) + 40) for c in self.uni}
        wc = collections.Counter(words)
        self.vocab = {w for w, c in wc.items() if c >= 3 and len(w) >= 3}
        self.memo = {}
        self.counts = {g: c for g, c in self.counts.items() if c >= 2 or len(g) <= 3}
    def prob(self, hist, c):
        key = hist + c; v = self.memo.get(key)
        if v is not None: return v
        if not hist: p = self.uni.get(c, 1e-6)
        else:
            tot = self.ctxtot.get(hist); lower = self.prob(hist[1:], c)
            p = lower if not tot else (max(self.counts.get(hist + c, 0) - D, 0) + D * self.ctxtypes[hist] * lower) / tot
        self.memo[key] = p; return p
    def logp(self, hist, c):
        if len(hist) > N - 1: hist = hist[-(N-1):]
        return math.log(self.prob(hist, c))
    def score(self, segments):
        s = 0.0
        for seg in segments:
            hist = ''
            for c in seg: s += self.logp(hist, c); hist = (hist + c)[-4:]
            if seg: s += math.log(self.ini.get(seg[0], 1e-4)) + math.log(self.fin.get(seg[-1], 1e-4)) - math.log(self.uni.get(seg[0], 1e-4)) - math.log(self.uni.get(seg[-1], 1e-4))
        return s
    def coverage(self, segments):
        cov = 0; tot = 0
        for seg in segments:
            tot += len(seg); i = 0
            while i < len(seg):
                for L in range(min(12, len(seg) - i), 2, -1):
                    if seg[i:i+L] in self.vocab: cov += L; i += L; break
                else: i += 1
        return cov / max(tot, 1)

def build_lm(lang):
    cache = HERE / f'lm_{lang}.bin'
    if cache.exists():
        d = pickle.load(open(cache, 'rb'))
        if 'vocab' in d:
            lm = LM.__new__(LM); lm.__dict__.update(d); lm.memo = {}; return lm
    text = ''
    for f in sorted(CORPUS.glob(f'corp_{lang}_*.txt')):
        raw = f.read_text(encoding='utf-8', errors='ignore')
        m = re.search(r'\*\*\* ?START OF.*?\*\*\*', raw); raw = raw[m.end():] if m else raw
        m = re.search(r'\*\*\* ?END OF', raw); raw = raw[:m.start()] if m else raw
        text += normalize(raw, lang) + ' '
    lm = LM(text)
    d = dict(lm.__dict__); d.pop('memo'); pickle.dump(d, open(cache, 'wb'))
    print(f'  LM {lang}: {len(text.replace(" ", ""))} letters, vocab {len(lm.vocab)}', flush=True)
    return lm

def load_cipher(path=None):
    path = pathlib.Path(arg('--cipher', str(HERE / 'cipher.txt'))) if path is None else path
    lines = [l.split() for l in path.read_text(encoding='utf-8').splitlines() if l.strip() and not l.startswith('#')]
    return [t for l in lines for t in l]

def variant(tokens, name):
    if name == 'full': return tokens
    if name == 'nodot': return [t for t in tokens if t != 'D']
    if name == 'dotsp': return ['|' if t == 'D' else t for t in tokens]
    if name == 'Nn': return ['n' if t == 'N' else t for t in tokens]
    if name == 'barletter': return ['L' if t == '|' else t for t in tokens]
    if name == 'dotattach':
        out = []; i = 0
        while i < len(tokens):
            if tokens[i] == 'D' and i + 1 < len(tokens) and tokens[i+1] in ('B', 'F'):
                out.append('D' + tokens[i+1]); i += 2
            else: out.append(tokens[i]); i += 1
        return out
    raise ValueError(name)

def solve(lm, tokens, rng):
    syms = sorted(set(t for t in tokens if t != '|'))
    letters = lm.letters[:max(len(syms) + 2, 22)]
    def segments(mapping):
        segs = []; cur = []
        for t in tokens:
            if t == '|': segs.append(''.join(cur)); cur = []
            else: cur.append(mapping[t])
        segs.append(''.join(cur)); return segs
    freq = collections.Counter(t for t in tokens if t != '|')
    finals = []
    for r in range(RESTARTS):
        order = sorted(syms, key=lambda s: -freq[s] + rng.random() * 3)
        pool = letters[:]
        if r % 2: rng.shuffle(pool)
        mapping = {}; used = set()
        for i, s in enumerate(order):
            cand = pool[i % len(pool)]
            if cand in used: cand = next(l for l in letters if l not in used)
            mapping[s] = cand; used.add(cand)
        sc = lm.score(segments(mapping)); best = (sc, dict(mapping))
        T0, T1 = 3.0, 0.05
        for it in range(ITERS):
            T = T0 * (T1 / T0) ** (it / ITERS)
            m2 = dict(mapping); a = rng.choice(syms)
            if rng.random() < 0.5:
                b = rng.choice(syms); m2[a], m2[b] = mapping[b], mapping[a]
            else:
                unused = [l for l in letters if l not in mapping.values()]
                if not unused: continue
                m2[a] = rng.choice(unused)
            sc2 = lm.score(segments(m2))
            if sc2 >= sc or rng.random() < math.exp((sc2 - sc) / T):
                mapping, sc = m2, sc2
                if sc > best[0]: best = (sc, dict(mapping))
        finals.append(best)
    finals.sort(key=lambda x: -x[0])
    out = []; seen = set()
    for sc, m in finals:
        segs = tuple(segments(m))
        if segs in seen: continue
        seen.add(segs); out.append((sc, m, list(segs), lm.coverage(segs)))
        if len(out) >= 5: break
    return out

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    tokens = load_cipher()
    print(f'{len(tokens)} tokens, {len(set(tokens))} distinct (incl. |)')
    rng = random.Random(int(arg('--seed', 1)))
    results = []
    for lang in LANGS:
        lm = build_lm(lang)
        for vname in VARIANTS:
            toks = variant(tokens, vname)
            n_letters = sum(1 for t in toks if t != '|')
            for rank, (sc, mapping, segs, cov) in enumerate(solve(lm, toks, rng)):
                results.append((sc / n_letters, cov, lang, vname, sc, segs, mapping))
                print(f'{lang:3} {vname:9} #{rank+1} {sc:8.1f} {sc/n_letters:6.3f}/letter cov {cov:.2f}  ' + ' | '.join(segs), flush=True)
    print('\nranked by per-letter score:')
    for r in sorted(results, reverse=True)[:10]:
        print(f'{r[0]:6.3f} cov {r[1]:.2f} {r[2]} {r[3]:9} ' + ' | '.join(r[5]))
        print('       key: ' + ' '.join(f'{k}={v}' for k, v in sorted(r[6].items())))
    print('\nranked by dictionary coverage:')
    for r in sorted(results, key=lambda r: (-r[1], -r[0]))[:10]:
        print(f'cov {r[1]:.2f} {r[0]:6.3f} {r[2]} {r[3]:9} ' + ' | '.join(r[5]))
