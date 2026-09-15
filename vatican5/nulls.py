"""Hypothesis: digit 7 is a null used as word delimiter. Examine segments between 7s."""
import collections, sys
from parse5 import load, digit_stream
D = sys.argv[1] if len(sys.argv) > 1 else '7'
runs = digit_stream(load(), keep_marks=False)
segs = []
for r in runs:
    s = ''.join(r)
    segs += [x for x in s.split(D)]
lens = collections.Counter(len(x) for x in segs)
print(f'delimiter {D}: {len(segs)} segments; length dist:', sorted(lens.items()))
c = collections.Counter(segs)
print('most common segments:', c.most_common(60))
# first digit / last digit of segments
print('first digit:', collections.Counter(x[0] for x in segs if x).most_common())
print('last digit :', collections.Counter(x[-1] for x in segs if x).most_common())
