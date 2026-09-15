import collections, math
from parse5 import load, digit_stream
runs = digit_stream(load(), keep_marks=False)
def mi(pairs):
    c = collections.Counter(pairs); n = sum(c.values())
    if n == 0: return 0
    a = collections.Counter(); b = collections.Counter()
    for (x, y), v in c.items(): a[x] += v; b[y] += v
    return sum(v / n * math.log(v / n / (a[x] / n * b[y] / n)) for (x, y), v in c.items()), n
adj = [(r[i], r[i+1]) for r in runs for i in range(len(r) - 1)]
skip = [(r[i], r[i+2]) for r in runs for i in range(len(r) - 2)]
print('adjacent MI %.3f (n=%d)   skip-1 MI %.3f' % (mi(adj) + mi(skip)[:1]))
print('\nper middle digit d: MI(x,y) over x d y; and MI(x,d)=how predictable d is from x; MI(d,y)')
for d in '0123456789':
    trip = [(r[i], r[i+2]) for r in runs for i in range(len(r) - 2) if r[i+1] == d]
    left = [(r[i], r[i+1]) for r in runs for i in range(len(r) - 1) if r[i+1] == d]
    right = [(r[i], r[i+1]) for r in runs for i in range(len(r) - 1) if r[i] == d]
    m, n = mi(trip)
    print(f'{d}: across={m:.3f} (n={n})')
# also: for each pair xy, MI between the digit before x and the digit after y (unit test): high => xy behaves like a unit
print('\nMI(prev, next) around frequent pairs xy (higher than skip-2 baseline => xy is a unit):')
skip2 = [(r[i], r[i+3]) for r in runs for i in range(len(r) - 3)]
print('skip-2 baseline MI %.3f' % mi(skip2)[0])
bg = collections.Counter(r[i] + r[i+1] for r in runs for i in range(len(r) - 1))
for pair, cnt in bg.most_common(25):
    prs = [(r[i-1], r[i+2]) for r in runs for i in range(1, len(r) - 2) if r[i] + r[i+1] == pair]
    m, n = mi(prs)
    print(f'{pair} ({cnt}): MI(prev,next)={m:.3f} n={n}')
