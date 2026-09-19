"""kwic.py KEYJSON TOKEN [n]: decoded context around each occurrence of TOKEN (shown in [brackets])."""
import json, sys
from parse import load
from solve2 import value, half
k = json.load(open(sys.argv[1], encoding='utf-8'))
h = {int(a[1:]): b for a, b in k.items() if a.startswith('H')}
s = {a: b for a, b in k.items() if not a.startswith('H')}
runs, _ = load()
tgt = sys.argv[2]; n = int(sys.argv[3]) if len(sys.argv) > 3 else 15
c = 0
for f, r in runs:
    for i, t in enumerate(r):
        if t == tgt:
            L = ''.join(value(x, h, s) for x in r[max(0, i-8):i]); R = ''.join(value(x, h, s) for x in r[i+1:i+9])
            print(f'{L:>22}[{value(t,h,s)}]{R}')
            c += 1
            if c >= n: sys.exit()
