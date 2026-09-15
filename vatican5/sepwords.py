import collections, sys
from parse5 import load, digit_stream
sep = sys.argv[1] if len(sys.argv) > 1 else '3'
runs = digit_stream(load(), keep_marks=True)
segs = []
for r in runs:
    cur = []
    for t in r:
        if t[0] == sep and len(t) == 1:
            segs.append(''.join(cur)); cur = []
        else:
            cur.append(t.replace('^.', '^').replace('^,', '^'))
    segs.append(''.join(cur))
segs = [s for s in segs]
c = collections.Counter(segs)
print('separator', sep, 'segments', len(segs), 'empty', c[''])
lens = collections.Counter(len(s) for s in segs)
print('length distribution:', sorted(lens.items()))
print('mean len', sum(len(s) for s in segs) / len(segs))
print('\nmost common segments:')
for s, n in c.most_common(80):
    print(f'{s:>12} {n}')
# first / last digits of segments
first = collections.Counter(s[0] for s in segs if s); last = collections.Counter(s[-1] for s in segs if s)
print('\nfirst digit:', sorted(first.items(), key=lambda x: -x[1]))
print('last digit :', sorted(last.items(), key=lambda x: -x[1]))
# print a stretch of segmented text
print('\nsample:')
print(' '.join(segs[:120]))
