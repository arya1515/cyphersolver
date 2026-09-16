"""Letter-only homophonic annealer on ct_all.txt (every distinct token a symbol, every symbol one Italian letter),
5-gram Italian LM (lucca/it5.npy). Baseline test only: syllable and word tokens will be forced into letters.
python solve_letters.py <seeds> [shuffle]  -> per-seed score per 5-gram and decoded text; shuffle = control."""
import numpy as np, random, math, sys, collections
lp = np.load('../lucca/it5.npy')
lines = [l.split() for l in open('ct_all.txt') if l.strip()]
toks = [t for l in lines for t in l]
syms = sorted(set(toks)); pos = {s: i for i, s in enumerate(syms)}
letters = [ord(ch) - 97 for ch in 'abcdefghilmnopqrstuvz']
seq = np.array([pos[t] for t in toks])
def score(key):
    p = key[seq]; q = p[:-4] * 456976 + p[1:-3] * 17576 + p[2:-2] * 676 + p[3:-1] * 26 + p[4:]
    return float(lp[q].sum())
def anneal(seed, iters=150000, T0=8.0, shuffle=False):
    global seq
    rnd = random.Random(seed)
    if shuffle:
        s2 = list(seq); rnd.shuffle(s2); seq = np.array(s2)
    key = np.array([rnd.choice(letters) for _ in syms]); cur = score(key); best = (cur, key.copy())
    for it in range(iters):
        T = max(0.05, T0 * (1 - it / iters)); s = rnd.randrange(len(syms)); old = key[s]
        if rnd.random() < 0.3:
            t = rnd.randrange(len(syms)); key[s], key[t] = key[t], key[s]; new = score(key)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: key[s], key[t] = key[t], key[s]
        else:
            key[s] = rnd.choice(letters); new = score(key)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: key[s] = old
        if cur > best[0]: best = (cur, key.copy())
    return best
if __name__ == '__main__':
    n = int(sys.argv[1]); shuffle = len(sys.argv) > 2 and sys.argv[2] == 'shuffle'
    ngr = len(seq) - 4; print('symbols', len(syms), 'tokens', len(seq), 'shuffle', shuffle, flush=True)
    for seed in range(n):
        sc, key = anneal(seed, shuffle=shuffle)
        txt = ''.join(chr(97 + key[pos[t]]) for t in toks)
        print(seed, round(sc / ngr, 3), txt[:400], flush=True)
        if not shuffle: print('KEY', {s: chr(97 + key[i]) for i, s in enumerate(syms)}, flush=True)
