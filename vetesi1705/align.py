"""Rebuild the R473 key: hard-EM alignment of each cipher run with the contemporary interlinear gloss (DECODE DOC transcription)."""
import re, math, collections, json, unicodedata
from pathlib import Path
ROOT = Path(__file__).resolve().parent
def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    return ''.join(ch for ch in s if ch.isalpha()).replace('j', 'i').replace('f', 's').replace('v','u')
def nums(s):
    s = re.sub(r'<[^>]*>', ' | ', s); out = []
    for seg in s.split('|'):
        for t in seg.split('.'):
            t = t.replace(' ', '')
            if t.isdigit(): out.append(t)
    return out
L = open(ROOT/'DOC_R473_D3610_3610.txt', encoding='utf-8-sig').read().splitlines()
runs = []
for i, l in enumerate(L):
    if l.startswith('<PLAINTEXT') and i+1 < len(L):
        g = nums(L[i+1])
        if g: runs.append((i+2, g, norm(l[len('<PLAINTEXT HU '):])))
prob = collections.defaultdict(collections.Counter)
def cost(c, s, it):
    lp = {0: 5.0, 1: 1.0, 2: 0.8, 3: 1.6, 4: 3.0, 5: 4, 6: 4, 7: 4, 8: 4}[len(s)]
    k = prob[c]; t = sum(k.values())
    if it == 0 or t == 0: return lp + 1
    return -math.log((k[s]+0.05)/(t+2)) + 0.3*lp
def vit(g, x, it):
    n, m = len(g), len(x); INF = 1e18
    D = [[INF]*(m+1) for _ in range(n+1)]; B = {}; D[0][0] = 0
    for i in range(n):
        for j in range(m+1):
            if D[i][j] >= INF: continue
            for k in range(0, min(8, m-j)+1):
                v = D[i][j] + cost(g[i], x[j:j+k], it)
                if v < D[i+1][j+k]: D[i+1][j+k] = v; B[i+1, j+k] = j
    out = []; j = m
    for i in range(n, 0, -1):
        pj = B[i, j]; out.append((g[i-1], x[pj:j])); j = pj
    return out[::-1]
for it in range(8):
    al = [vit(g, x, it) for _, g, x in runs]
    prob = collections.defaultdict(collections.Counter)
    for a in al:
        for c, s in a: prob[c][s] += 1
key = {c: prob[c].most_common() for c in sorted(prob, key=int)}
json.dump(key, open(ROOT/'key_rebuilt.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
for c, v in key.items(): print(c, v)
