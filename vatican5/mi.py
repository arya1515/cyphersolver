"""Mutual information between digits adjacent vs. across a candidate null digit."""
import collections, math, sys
from parse5 import load, digit_stream
runs = digit_stream(load(), keep_marks=False)
text = [''.join(r) for r in runs]
def mi(pairs):
    n = sum(pairs.values()); px = collections.Counter(); py = collections.Counter()
    for (x, y), c in pairs.items(): px[x] += c; py[y] += c
    return sum(c/n * math.log2((c/n) / ((px[x]/n) * (py[y]/n))) for (x, y), c in pairs.items())
for d in '0123456789':
    across = collections.Counter(); adjacent = collections.Counter()
    for s in text:
        for i in range(len(s) - 2):
            if s[i+1] == d and s[i] != d and s[i+2] != d: across[(s[i], s[i+2])] += 1
        for i in range(len(s) - 1):
            if s[i] != d and s[i+1] != d: adjacent[(s[i], s[i+1])] += 1
    gap2 = collections.Counter()
    for s in text:
        for i in range(len(s) - 2):
            if d not in s[i:i+3]: gap2[(s[i], s[i+2])] += 1
    print(f'{d}: n={sum(across.values()):4d}  MI across {d}: {mi(across):.3f}   MI adjacent(no {d}): {mi(adjacent):.3f}   MI skip-one(no {d}): {mi(gap2):.3f}')
