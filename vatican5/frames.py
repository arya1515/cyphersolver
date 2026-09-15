"""Frame analysis: is the ciphertext a pure 2-digit code? Compare pair statistics at even vs odd offsets per run."""
import collections, math
from parse5 import load, digit_stream

def entropy(c):
    n = sum(c.values()); return -sum(v/n*math.log2(v/n) for v in c.values())

pages = load(); runs = digit_stream(pages, keep_marks=False)
for i, r in enumerate(runs):
    if len(r) < 100: continue
    s = ''.join(r)
    for f in (0, 1):
        pairs = collections.Counter(s[j:j+2] for j in range(f, len(s)-1, 2))
        print(f'run {i} len {len(s)} frame {f}: distinct={len(pairs)} H={entropy(pairs):.2f} top={pairs.most_common(8)}')
# whole-text non-overlapping in each frame, using run-relative frames
allp = [collections.Counter(), collections.Counter()]
for r in runs:
    s = ''.join(r)
    for f in (0, 1):
        allp[f].update(s[j:j+2] for j in range(f, len(s)-1, 2))
for f in (0, 1):
    print(f'\nALL frame {f}: distinct={len(allp[f])} H={entropy(allp[f]):.2f}')
    print(' ', allp[f].most_common(40))
# overlapping bigrams overall for comparison
ov = collections.Counter()
for r in runs:
    s = ''.join(r); ov.update(s[j:j+2] for j in range(len(s)-1))
print(f'\nOVERLAPPING: distinct={len(ov)} H={entropy(ov):.2f}')
print(' ', ov.most_common(40))
