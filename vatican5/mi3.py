import collections, math, random
from parse5 import load, digit_stream
runs = digit_stream(load(), keep_marks=False)
rnd = random.Random(0)
def mi(pairs):
    c = collections.Counter(pairs); n = sum(c.values())
    a = collections.Counter(); b = collections.Counter()
    for (x, y), v in c.items(): a[x] += v; b[y] += v
    return sum(v / n * math.log(v / n / (a[x] / n * b[y] / n)) for (x, y), v in c.items())
def mi_corr(pairs, k=20):
    """MI minus permutation baseline (bias-corrected)."""
    m = mi(pairs); ys = [y for _, y in pairs]; base = 0
    for _ in range(k):
        rnd.shuffle(ys); base += mi([(x, y) for (x, _), y in zip(pairs, ys)])
    return m - base / k
adj = [(r[i], r[i+1]) for r in runs for i in range(len(r) - 1)]
skip = [(r[i], r[i+2]) for r in runs for i in range(len(r) - 2)]
skip2 = [(r[i], r[i+3]) for r in runs for i in range(len(r) - 3)]
print('corrected: adjacent %.3f  skip-1 %.3f  skip-2 %.3f' % (mi_corr(adj), mi_corr(skip), mi_corr(skip2)))
print('\nMI(x,y) across middle digit d (corrected). Null/separator => ~0; transparent letter => ~skip-1; tail of a pair code => high')
for d in '0123456789':
    trip = [(r[i], r[i+2]) for r in runs for i in range(len(r) - 2) if r[i+1] == d]
    print(f'  {d}: {mi_corr(trip):+.3f} (n={len(trip)})')
print('\nMI(prev,next) around pair xy (corrected); compare skip-2 baseline')
bg = collections.Counter(r[i] + r[i+1] for r in runs for i in range(len(r) - 1))
for pair, cnt in bg.most_common(30):
    prs = [(r[i-1], r[i+2]) for r in runs for i in range(1, len(r) - 2) if r[i] + r[i+1] == pair]
    print(f'  {pair} ({cnt}): {mi_corr(prs):+.3f}')
