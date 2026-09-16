"""Homophonic anneal on the letter layer of a token file; marked tokens (target: mark suffix; control: Y*) and numbers are
wildcards that break the n-gram context. Scores 5-grams inside letter runs with the spaced du Croc French model
(../ducroc/fr5.npy), padding run starts with word-boundary context.
Usage: python solve.py FILE [nseeds] [iters]   env MODE=target|control  KEY=control_key.txt (for scoring accuracy)"""
import numpy as np, random, math, sys, os, re, collections
V = 27
lp = np.load('../ducroc/fr5.npy')
LET = [ord(c) - 97 for c in 'abcdefghilmnopqrstuxyz']
isnum = lambda t: re.fullmatch(r'\d+', t) is not None
def iswild(t, mode):
    if isnum(t): return True
    if mode == 'control': return t.startswith('Y')
    return bool(re.search(r'[.:+#^_]$', t)) or t.endswith('++')
def load(fn, mode):
    toks = []
    for line in open(fn, encoding='utf-8'):
        if line.startswith('#'): continue
        toks += [t for t in line.split() if t != '|']
    return toks
def prep(toks, mode):
    syms = sorted(set(t for t in toks if not iswild(t, mode))); pos = {s: i for i, s in enumerate(syms)}
    seq = np.array([(-1 if iswild(t, mode) else pos[t]) for t in toks])
    return syms, seq
def score(key, seq):
    p = np.where(seq < 0, 26, key[np.maximum(seq, 0)])
    p = np.concatenate([[26] * 4, p, [26]])
    q = ((((p[:-4] * V + p[1:-3]) * V + p[2:-2]) * V + p[3:-1]) * V + p[4:])
    return float(lp[q].sum())
def anneal(syms, seq, seed, iters=60000, T0=4.0):
    rnd = random.Random(seed)
    cnt = collections.Counter(seq[seq >= 0].tolist()); order = [s for s, _ in cnt.most_common()]
    fr = 'eaisntrulodcmpqugbfhxyz'
    key = np.array([rnd.choice(LET) for _ in syms])
    if seed % 2 == 0:
        for r, sidx in enumerate(order): key[sidx] = ord(fr[min(r, len(fr) - 1)]) - 97
    cur = score(key, seq); best = (cur, key.copy())
    n = len(syms)
    for it in range(iters):
        T = max(0.05, T0 * (1 - it / iters))
        s = rnd.randrange(n); old = key[s]
        if rnd.random() < 0.3:
            t = rnd.randrange(n); key[s], key[t] = key[t], key[s]
            new = score(key, seq)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: key[s], key[t] = key[t], key[s]
        else:
            key[s] = rnd.choice(LET); new = score(key, seq)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: key[s] = old
        if cur > best[0]: best = (cur, key.copy())
    return best
def render(key, seq, toks):
    out = []
    for x, t in zip(seq, toks):
        out.append('_' if x < 0 else chr(97 + key[x]))
    return ''.join(out)
if __name__ == '__main__':
    fn = sys.argv[1]; n = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    iters = int(sys.argv[3]) if len(sys.argv) > 3 else 60000
    mode = os.environ.get('MODE', 'target')
    toks = load(fn, mode); syms, seq = prep(toks, mode)
    print('tokens', len(toks), 'letter tokens', int((seq >= 0).sum()), 'letter symbols', len(syms), flush=True)
    truth = None
    if os.environ.get('KEY'):
        truth = {}
        for line in open(os.environ['KEY'], encoding='utf-8'):
            a, b = line.split(); truth[a] = b
    res = []
    for seed in range(n):
        b = anneal(syms, seq, seed, iters); res.append(b)
        line = f'{seed} {b[0]:.1f} {render(b[1], seq, toks)}'
        if truth:
            ok = sum(1 for x in seq if x >= 0 and truth.get(syms[x]) == chr(97 + b[1][x]))
            line += f'  ACC {ok}/{int((seq >= 0).sum())} = {ok / max(1, int((seq >= 0).sum())):.2f}'
        print(line, flush=True)
    b = max(res, key=lambda r: r[0])
    print('BESTKEY', {s: chr(97 + b[1][i]) for i, s in enumerate(syms)})
