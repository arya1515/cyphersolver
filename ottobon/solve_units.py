"""Unit-level homophonic annealer: each distinct token maps to one Italian letter, one CV syllable or a word wildcard.
Score = sum of 5-gram log-probs + BETA per plaintext character - NULLPEN per wildcard token.
python solve_units.py target <seeds>            -> ct_all.txt
python solve_units.py control <seeds> <noise>   -> synthetic Italian text with the same token profile, recovery reported"""
import numpy as np, random, math, sys, re, collections, unicodedata
sys.path.insert(0, '../lucca'); from lm import clean, strip_gut
lp = np.load('../lucca/it5.npy'); A = 'abcdefghilmnopqrstuz'
CONS = 'bcdfghlmnpqrstz'; VOW = 'aeiou'
UNITS = list(A) + ['']   # letters + wildcard only (syllable units made the control degenerate to syllable soup)
BETA, NULLPEN = 0.0, 3.0
def enc(s): return np.array([ord(ch) - 97 for ch in s], dtype=np.int64)
def lmscore(s):
    p = enc(s)
    if len(p) < 5: return 0.0
    q = p[:-4] * 456976 + p[1:-3] * 17576 + p[2:-2] * 676 + p[3:-1] * 26 + p[4:]
    return float(lp[q].sum())
def total(key, toks):
    s = ''.join(UNITS[key[t]] for t in toks); nulls = sum(1 for t in toks if UNITS[key[t]] == '')
    return lmscore(s) + BETA * len(s) - NULLPEN * nulls, s
def anneal(toks, nsym, seed, iters=120000, T0=15.0, init=None):
    rnd = random.Random(seed); key = np.array(init if init is not None else [rnd.randrange(len(UNITS)) for _ in range(nsym)])
    cur, _ = total(key, toks); best = (cur, key.copy())
    for it in range(iters):
        T = max(0.1, T0 * (1 - it / iters)); s = rnd.randrange(nsym); old = key[s]
        r = rnd.random()
        key[s] = rnd.randrange(20) if r < 0.9 else len(UNITS) - 1
        new, _ = total(key, toks)
        if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
        else: key[s] = old
        if cur > best[0]: best = (cur, key.copy())
    return best
def make_control(seed, n_tokens, noise):
    rnd = random.Random(seed)
    text = clean(strip_gut(open('../lucca/corpus/61704.txt', encoding='utf-8', errors='ignore').read()))
    start = rnd.randrange(50000, len(text) - 20000); pos = start; units = []
    while len(units) < n_tokens:
        r = rnd.random()
        if r < 0.62: units.append(('L', text[pos])); pos += 1
        elif r < 0.85 and text[pos] in CONS and text[pos + 1] in VOW: units.append(('S', text[pos:pos + 2])); pos += 2
        else:
            k = rnd.randrange(3, 8); units.append(('W', text[pos:pos + k])); pos += k
    # symbols: 6 homophones per letter, one symbol per syllable, 25 word symbols
    hom = {ch: ['L%s%d' % (ch, i) for i in range(6)] for ch in A}
    words = ['W%d' % i for i in range(25)]; toks = []; truth = []
    for kind, u in units:
        if kind == 'L': toks.append(rnd.choice(hom[u])); truth.append(u)
        elif kind == 'S': toks.append('S' + u); truth.append(u)
        else: toks.append(rnd.choice(words)); truth.append('')
    syms = sorted(set(toks))
    for i in range(len(toks)):
        if rnd.random() < noise: toks[i] = rnd.choice(syms)
    return toks, truth, syms
if __name__ == '__main__':
    mode = sys.argv[1]; n = int(sys.argv[2])
    if mode == 'target':
        toks = [t for l in open('ct_all.txt') for t in l.split()]; truth = None
    else:
        toks, truth, _ = make_control(7, 1528, float(sys.argv[3]))
    syms = sorted(set(toks)); pos = {s: i for i, s in enumerate(syms)}; ti = [pos[t] for t in toks]
    print('symbols', len(syms), 'tokens', len(toks), flush=True)
    for seed in range(n):
        sc, key = anneal(ti, len(syms), seed); _, s = total(key, ti)
        print('seed', seed, 'score', round(sc, 1), 'chars', len(s), 'per-char', round(lmscore(s) / max(len(s), 1), 3), flush=True)
        print(s[:500], flush=True)
        if truth is not None:
            ok = sum(1 for t, u in zip(ti, truth) if u and len(u) <= 2 and UNITS[key[t]] == u); tot = sum(1 for u in truth if u and len(u) <= 2)
            okl = sum(1 for t, u in zip(ti, truth) if len(u) == 1 and UNITS[key[t]] == u); totl = sum(1 for u in truth if len(u) == 1)
            print('recovery letters %d/%d = %.0f%%  letters+syllables %d/%d = %.0f%%' % (okl, totl, 100.0 * okl / totl, ok, tot, 100.0 * ok / tot), flush=True)
        else:
            print('KEY', {s_: UNITS[key[i]] for i, s_ in enumerate(syms)}, flush=True)
