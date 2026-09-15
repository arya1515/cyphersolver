"""Context of dotted digits: what precedes/follows '^' marks."""
import collections
from parse5 import load, digit_stream
runs = digit_stream(load())
after1 = collections.Counter(); after2 = collections.Counter(); before = collections.Counter(); dotted = collections.Counter()
ctx = collections.defaultdict(list)
for r in runs:
    for i, t in enumerate(r):
        if '^' in t:
            dotted[t[0]] += 1
            nxt = ''.join(x[0] for x in r[i+1:i+3]); prv = ''.join(x[0] for x in r[max(0,i-2):i])
            after1[nxt[:1]] += 1; after2[nxt] += 1; before[prv] += 1
            ctx[t[0]].append(prv + '[' + t[0] + ']' + ''.join(x[0] for x in r[i+1:i+4]))
print('dotted digit:', dotted.most_common())
print('next digit  :', after1.most_common())
print('next 2 digits:', after2.most_common(30))
print('prev 2 digits:', before.most_common(20))
for d in '720':
    print(f'\n[{d}] contexts:', ' '.join(ctx[d][:60]))
