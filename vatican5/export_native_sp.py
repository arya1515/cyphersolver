"""Export lm5sp.bin: 5-gram LM over 21 symbols (20 letters + '_' = space), from it_ngrams.json (spaced corpus).
Layout: float32 [22^4 contexts][21 symbols], pad index 21."""
import json, itertools, array, math, pathlib, collections
HERE = pathlib.Path(__file__).parent
ALPHA = 'abcdefghilmnopqrstuz_'
L = len(ALPHA); PAD = L; N = 5
g = json.load(open(HERE / 'it_ngrams.json'))
def conv(k): return k.replace(' ', '_')
c = [None] + [{conv(k): v for k, v in g[str(n)].items() if all(ch in ALPHA for ch in conv(k))} for n in range(1, N + 1)]
tot1 = sum(c[1].values())
ctx = [None, None] + [collections.Counter() for _ in range(2, N + 1)]
for n in range(2, N + 1):
    for k, v in c[n].items(): ctx[n][k[:-1]] += v
def lp(hist, ch):
    w = 1.0
    for n in range(min(N, len(hist) + 1), 0, -1):
        h = hist[len(hist) - (n - 1):] if n > 1 else ''
        num = c[n].get(h + ch)
        if num:
            den = ctx[n][h] if n > 1 else tot1
            return math.log(w * num / den)
        w *= 0.4
    return math.log(w * 1e-7)
out = array.array('f'); n = 0
for h in itertools.product(range(L + 1), repeat=4):
    hs = ''.join(ALPHA[i] for i in h if i != PAD)
    for ch in ALPHA: out.append(lp(hs, ch))
    n += 1
(HERE / 'lm5sp.bin').write_bytes(out.tobytes())
print('contexts', n, 'floats', len(out), 'space share', c[1]['_'] / tot1)
