"""Simple-substitution hill climb (quadgram) on a ciphertext string; '?' = unknown symbol kept as-is."""
import random, math, re, sys
import bookcipher as bc
lm = bc.LM()
AL = bc.AL
def score(s):
    return lm.quad_score(s)
def solve(ct, restarts=20, iters=4000, seed=0):
    rnd = random.Random(seed)
    syms = sorted(set(ct) - {'?'})
    best_all = (-1e9, None)
    for r in range(restarts):
        key = {s: AL[i % 26] for i, s in enumerate(syms)}
        vals = list(AL); rnd.shuffle(vals)
        key = {s: vals[i % 26] for i, s in enumerate(syms)}
        cur = ''.join(key.get(c, '?') for c in ct); cs = score(cur)
        for it in range(iters):
            a, b = rnd.sample(syms, 2)
            key[a], key[b] = key[b], key[a]
            new = ''.join(key.get(c, '?') for c in ct); ns = score(new)
            if ns > cs or rnd.random() < math.exp((ns - cs) * 200):
                cur, cs = new, ns
            else:
                key[a], key[b] = key[b], key[a]
        if cs > best_all[0]:
            best_all = (cs, cur)
    return best_all
if __name__ == '__main__':
    ct = sys.argv[1]
    s, pt = solve(ct)
    print(round(s, 3)); print(pt)
