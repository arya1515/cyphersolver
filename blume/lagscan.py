"""Lag scan: for each lag 1..599 score the Spanish bigram log-probability of every ciphertext pair (i, i+lag), both
orders, against a shuffled baseline. Single columnar (either direction), reversed-direction double columnar
(neighbours land w1*w2 apart) and the rows-then-columns mixed convention all put plaintext neighbours at a fixed lag.
Planted controls print their z at the expected lag. Run: python lagscan.py"""
from collections import Counter
import math, re, random
import os; HERE = os.path.dirname(os.path.abspath(__file__))
ct = open(HERE + '/ct1.txt').read().strip(); n = len(ct)
txt = open(HERE + '/corpus/es_2000.txt', encoding='utf8', errors='ignore').read().lower()
for a, b in zip('áéíóúñü', 'aeiounu'): txt = txt.replace(a, b)
txt = re.sub('[^a-z]', '', txt)
bg = Counter(txt[i:i + 2] for i in range(len(txt) - 1)); T = sum(bg.values())
lp = {k: math.log10(v / T) for k, v in bg.items()}; fl = math.log10(0.5 / T)
def bscore(s, lag): return sum(lp.get(s[i] + s[i + lag], fl) for i in range(len(s) - lag)) / (len(s) - lag)
random.seed(1)
l = list(ct); vals = []
for _ in range(300):
    random.shuffle(l); vals.append(bscore(''.join(l), 1))
mu = sum(vals) / 300; sd1 = (sum((x - mu) ** 2 for x in vals) / 300) ** .5
def scan(s):
    out = []
    for lag in range(1, 600):
        sd = sd1 * math.sqrt((n - 1) / (n - lag))
        f = bscore(s, lag); r = bscore(s[::-1], lag)
        out.append((max((f - mu) / sd, (r - mu) / sd), lag, f, r))
    return sorted(out, reverse=True)
print('baseline per-pair mean %.3f, sd at 614 pairs %.3f' % (mu, sd1))
res = scan(ct)
print('real telegram, top lags:')
for z, lag, f, r in res[:8]: print('  lag %3d fwd %.3f rev %.3f z=%.1f' % (lag, f, r, z))
def colmap(n, order, w):
    rows, rem = divmod(n, w); m = [0] * n; pos = 0
    for k in range(w):
        c = order[k]; L = rows + (1 if c < rem else 0)
        for r in range(L): m[r * w + c] = pos; pos += 1
    return m
def undoF(x, order, w):  # written into columns in key order, read off by rows (the reversed direction)
    m = colmap(len(x), order, w); return ''.join(x[m[i]] for i in range(len(x)))
def encF(x, order, w):   # written in rows, read by columns in key order (the forward direction)
    m = colmap(len(x), order, w); out = [''] * len(x)
    for i, ch in enumerate(x): out[m[i]] = ch
    return ''.join(out)
random.seed(5); pt = txt[7000:7615]
for w1, w2 in [(19, 8), (23, 9), (17, 29)]:
    k1 = list(range(w1)); random.shuffle(k1); k2 = list(range(w2)); random.shuffle(k2)
    c = undoF(undoF(pt, k1, w1), k2, w2); best = scan(c)[0]
    print('control reversed %dx%d: best lag %d z=%.1f (expected %d)' % (w1, w2, best[1], best[0], w1 * w2))
    c = undoF(encF(pt, k1, w1), k2, w2); best = scan(c)[0]
    print('control rows-then-columns %dx%d: best lag %d z=%.1f (expected %d or %d)' % (w1, w2, best[1], best[0], (n // w1) * w2, (n // w1 + 1) * w2))
    c = encF(encF(pt, k1, w1), k2, w2); best = scan(c)[0]
    print('control forward %dx%d: best lag %d z=%.1f (no fixed lag expected)' % (w1, w2, best[1], best[0]))
