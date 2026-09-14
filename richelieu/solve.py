"""Homophonic-substitution hill-climber for the Richelieu 1629 cipher.

Symbols 10..40 (and '~'-marked variants) are treated as letter substitutes; codes >= 41 are
treated as nomenclature (unknown words) that break the n-gram context. Cleartext words in the
transcription are used as fixed known letters adjacent to the cipher.
"""
import json, math, random, re, sys, pathlib, argparse
from collections import Counter
from parse import load, is_cipher
from build_ngrams import normalize

HERE = pathlib.Path(__file__).parent
ALPHA = 'abcdefghilmnopqrstuxyz'          # 22-letter 17th-c. alphabet
NOMEN_MIN = 41                            # tokens >= this are word-codes

# ---------- language model ----------
_q = json.load(open(HERE / 'fr_quadgrams.json'))
_tot = sum(_q.values())
_floor = math.log10(0.01 / _tot)
LM = {k: math.log10(v / _tot) for k, v in _q.items()}
def qscore(s: str) -> float:
    return sum(LM.get(s[i:i+4], _floor) for i in range(len(s) - 3))

# ---------- build segments ----------
def build_segments(letters):
    """Return list of segments; each segment = list of items (kind, value): ('P', letter) fixed, ('C', symbol) variable."""
    segs = []
    for name, lines in letters.items():
        cur = []
        for toks in lines:
            for t in toks:
                if is_cipher(t):
                    n = int(t.lstrip('~'))
                    if n >= NOMEN_MIN:
                        if cur: segs.append(cur); cur = []
                    else:
                        cur.append(('C', t))
                else:
                    for ch in normalize(t.replace('_', '')):
                        cur.append(('P', ch))
        if cur: segs.append(cur)
    return segs

def sym_letters(key, v):
    """'~N' denotes the doubled letter of N."""
    if v.startswith('~'):
        base = key.get(v[1:], '?')
        return base * 2
    return key.get(v, '?')

def render(seg, key, upper_cipher=False):
    out = []
    for kind, v in seg:
        if kind == 'P': out.append(v)
        else:
            ch = sym_letters(key, v)
            out.append(ch.upper() if upper_cipher else ch)
    return ''.join(out)

# expected unigram frequencies from corpus (normalized alphabet)
_uni = Counter()
for k, v in _q.items(): _uni[k[0]] += v
_utot = sum(_uni.values())
EXPECT = {l: _uni[l] / _utot for l in ALPHA}

def unigram_penalty(segs, key, weight):
    if not weight: return 0.0
    c = Counter()
    for s in segs:
        for kind, v in s:
            if kind == 'C':
                for ch in sym_letters(key, v): c[ch] += 1
    n = sum(c.values())
    # KL(observed || expected) in nats, scaled by number of cipher letters
    kl = 0.0
    for l in ALPHA:
        p = c[l] / n
        if p > 0: kl += p * math.log(p / max(EXPECT[l], 1e-6))
    return -weight * n * kl

def total_score(segs, key, weight=0.0):
    return sum(qscore(render(s, key)) for s in segs) + unigram_penalty(segs, key, weight)

# ---------- annealing ----------
def anneal(segs, symbols, fixed, iters=60000, T0=3.0, seed=None, init=None, core=(), weight=0.0):
    """core: symbols constrained to a bijection with ALPHA (only swap moves among them)."""
    rnd = random.Random(seed)
    core = [s for s in core if s in symbols]
    key = dict(init) if init else {s: rnd.choice(ALPHA) for s in symbols}
    if core:
        perm = list(ALPHA); rnd.shuffle(perm)
        for s, l in zip(core, perm): key[s] = l
    key.update(fixed)
    free = [s for s in symbols if s not in fixed and s not in core]
    corefree = [s for s in core if s not in fixed]
    cur = total_score(segs, key, weight); best, bestkey = cur, dict(key)
    for i in range(iters):
        T = T0 * (1 - i / iters) + 0.05
        if corefree and (not free or rnd.random() < 0.7):
            s, s2 = rnd.sample(corefree, 2); old, old2 = key[s], key[s2]
            key[s], key[s2] = old2, old
            undo = lambda: (key.__setitem__(s, old), key.__setitem__(s2, old2))
        else:
            s = rnd.choice(free); old = key[s]
            key[s] = rnd.choice(ALPHA)
            undo = lambda: key.__setitem__(s, old)
        new = total_score(segs, key, weight)
        if new > cur or rnd.random() < math.exp((new - cur) / T):
            cur = new
            if cur > best: best, bestkey = cur, dict(key)
        else:
            undo()
    return best, bestkey

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--restarts', type=int, default=8)
    ap.add_argument('--iters', type=int, default=60000)
    ap.add_argument('--fix', default='', help='e.g. "14=l,19=a"')
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--core', default='', help='symbol range forced to be a bijection with the alphabet, e.g. 10-31')
    ap.add_argument('--weight', type=float, default=0.5, help='unigram KL penalty weight')
    args = ap.parse_args()
    letters = load()
    segs = build_segments(letters)
    symbols = sorted({v for s in segs for k, v in s if k == 'C' and not v.startswith('~')}, key=int)
    fixed = dict(kv.split('=') for kv in args.fix.split(',') if kv)
    core = []
    if args.core:
        a, b = map(int, args.core.split('-')); core = [str(n) for n in range(a, b + 1)]
    print(f'{len(segs)} segments, {len(symbols)} symbols, fixed={fixed}, core={len(core)}, weight={args.weight}')
    results = []
    for r in range(args.restarts):
        best, key = anneal(segs, symbols, fixed, iters=args.iters, seed=args.seed + r, core=core, weight=args.weight)
        results.append((best, key)); print(f'restart {r}: {best:.1f}', flush=True)
    results.sort(key=lambda x: -x[0])
    best, key = results[0]
    print('\nBEST', round(best, 1))
    print('KEY:', ' '.join(f'{s}={key[s]}' for s in symbols))
    # letter -> symbols
    inv = {}
    for s in symbols: inv.setdefault(key[s], []).append(s)
    print('INV:', ' '.join(f'{l}:{"/".join(inv[l])}' for l in ALPHA if l in inv))
    print('\nPLAINTEXT (cipher letters in CAPS, | = nomenclature code):')
    for name, lines in letters.items():
        print(f'--- {name}')
        for toks in lines:
            out = []
            for t in toks:
                if is_cipher(t):
                    n = int(t.lstrip('~'))
                    out.append(f'|{t}|' if n >= NOMEN_MIN else sym_letters(key, t).upper())
                else:
                    out.append(' ' + t.replace('_', ' ') + ' ')
            print(''.join(out))
    # agreement among top results
    if len(results) > 1:
        print('\nAgreement of top-3 keys per symbol:')
        for s in symbols:
            print(f'  {s}: ' + ' '.join(k[s] for _, k in results[:3]))

if __name__ == '__main__':
    main()
