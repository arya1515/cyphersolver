"""Candidate word units: frequent n-grams with high branching entropy on both sides."""
import collections, math
from parse5 import load, digit_stream
runs = [''.join(r) for r in digit_stream(load(), keep_marks=False)]
def H(c):
    n = sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values()) if n else 0
rows = []
for n in (3, 4, 5, 6):
    c = collections.Counter()
    for s in runs:
        for i in range(len(s) - n + 1): c[s[i:i+n]] += 1
    for g, v in c.items():
        if v < (30 if n == 3 else 12 if n == 4 else 6):
            continue
        L = collections.Counter(); R = collections.Counter()
        for s in runs:
            i = s.find(g)
            while i >= 0:
                if i > 0: L[s[i-1]] += 1
                if i + n < len(s): R[s[i+n]] += 1
                i = s.find(g, i + 1)
        rows.append((min(H(L), H(R)), v, g, H(L), H(R)))
rows.sort(reverse=True)
for m, v, g, hl, hr in rows[:70]:
    print(f'{g:7} n={v:3d}  H_left={hl:.2f} H_right={hr:.2f}')
