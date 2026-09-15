"""Find the 2-class partition of digits (vowel-like vs consonant-like) maximizing alternation in adjacent digits."""
import itertools, collections
from parse5 import load, digit_stream
runs = [''.join(r) for r in digit_stream(load(), keep_marks=False)]
bg = collections.Counter()
for s in runs:
    for a, b in zip(s, s[1:]): bg[a + b] += 1
tot = sum(bg.values())
res = []
for mask in range(1, 512):           # digit '0' fixed in class A to avoid symmetric duplicates
    V = {'0'} | {str(d) for d in range(1, 10) if mask >> (d - 1) & 1}
    alt = sum(c for p, c in bg.items() if (p[0] in V) != (p[1] in V))
    res.append((alt / tot, ''.join(sorted(V))))
res.sort(reverse=True)
for r in res[:15]: print(f'{r[0]:.3f}  class A = {r[1]}   class B = {"".join(d for d in "0123456789" if d not in r[1])}')
