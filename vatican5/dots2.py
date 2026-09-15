import collections, sys
from parse5 import load, digit_stream
pages = load()
runs = digit_stream(pages, keep_marks=True)
# dotted contexts
ctx = collections.Counter()
after1 = collections.Counter(); after2 = collections.Counter(); before1 = collections.Counter()
lines = []
for r in runs:
    d = [t[0] for t in r]
    for i, t in enumerate(r):
        if '^' in t:
            pre = ''.join(d[max(0, i-4):i]); post = ''.join(d[i+1:i+6])
            lines.append(f'{pre:>4} [{t}] {post}')
            after1[t[0] + '^' + d[i+1] if i+1 < len(d) else 'END'] += 1
            after2[t[0] + '^' + ''.join(d[i+1:i+3])] += 1
            before1[(d[i-1] if i else 'BEG') + '_' + t[0] + '^'] += 1
print('dotted count', len(lines))
print('after1', sorted(after1.items(), key=lambda x: -x[1])[:30])
print('after2', sorted(after2.items(), key=lambda x: -x[1])[:40])
print('before1', sorted(before1.items(), key=lambda x: -x[1])[:30])
for l in lines: print(l)
