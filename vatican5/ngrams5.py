"""Repeated n-grams in the digit stream (marks stripped), with contexts."""
import collections, sys
from parse5 import load, digit_stream
runs = [''.join(r) for r in digit_stream(load(), keep_marks=False)]
big = '|'.join(runs)
for n in (8, 7, 6, 5):
    c = collections.Counter()
    for s in runs:
        for i in range(len(s) - n + 1): c[s[i:i+n]] += 1
    top = [(k, v) for k, v in c.most_common(400) if v >= (3 if n >= 6 else 5)]
    print(f'\n=== {n}-grams repeated: {len(top)}')
    for k, v in top[:40]:
        # left/right contexts
        L = collections.Counter(); R = collections.Counter()
        for s in runs:
            i = s.find(k)
            while i >= 0:
                L[s[max(0, i-2):i]] += 1; R[s[i+n:i+n+2]] += 1; i = s.find(k, i + 1)
        print(f'{k}: {v:3d}  L={dict(L.most_common(4))}  R={dict(R.most_common(4))}')
