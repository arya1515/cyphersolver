"""Apply the Biermann-Bosbach 6956 key (DECODE R215, merged key D1508 + Biermann D1506) to a digit stream.
DP segmentation: nulls 1/8, two-digit homophones, three-digit nomenclator groups."""
import re, sys
sys.path.insert(0, '.')
from solve import load_doc
def load_key():
    k = {}
    for f in ('key6956/DOC_R215_D1506_1506.txt', 'key6956/DOC_R215_D1508_1508.txt'):
        t = open(f, encoding='utf-8', errors='replace').read()
        for c, v in re.findall(r'(?:^|(?<=[^\d]))(\d{2,4})\s+([^\d\n\t]+?)(?=\s*\d{2,4}\s|\n|$)', t):
            v = v.strip()
            if c not in k and v: k[c] = v
    return k
KEY = load_key()
def decode(d):
    n = len(d); INF = -1e9
    best = [INF]*(n+1); back = [None]*(n+1); best[0] = 0
    for i in range(n):
        if best[i] == INF: continue
        cands = []
        if d[i] in '18': cands.append((1, 0.2, '|'))
        for L in (2, 3):
            c = d[i:i+L]
            if len(c) < L: continue
            if c in KEY: cands.append((L, 1.0 if L == 2 else 1.3, KEY[c] if L == 2 else '[' + KEY[c] + ']'))
            elif L == 3 and c[0] not in '018': cands.append((3, -1.5, '[' + c + ']'))
        cands.append((1, -3, '?' + d[i]))
        for L, s, out in cands:
            if best[i] + s > best[i+L]: best[i+L] = best[i] + s; back[i+L] = (i, out)
    toks = []; j = n
    while j: i, o = back[j]; toks.append(o); j = i
    return ''.join(reversed(toks)).replace('|', ' ')
if __name__ == '__main__':
    for p in sys.argv[1:]:
        d, _ = load_doc(p); print('==', p, len(d)); print(decode(d))
