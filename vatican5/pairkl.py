import collections, math
from parse5 import load, digit_stream
runs = digit_stream(load(), keep_marks=False)
big = collections.Counter(); nxt = collections.Counter(); nxt1 = collections.Counter(); prv = collections.Counter(); prv1 = collections.Counter()
uni = collections.Counter()
for r in runs:
    for i in range(len(r)):
        uni[r[i]] += 1
        if i + 1 < len(r):
            big[r[i] + r[i+1]] += 1
            nxt1[(r[i], r[i+1])] += 1
        if i + 2 < len(r):
            nxt[(r[i] + r[i+1], r[i+2])] += 1
        if i >= 2:
            prv[(r[i-1] + r[i], r[i-2])] += 1
        if i >= 1:
            prv1[(r[i], r[i-1])] += 1
def kl(pair):
    # P(next | pair) vs P(next | second digit)
    n = sum(nxt[(pair, d)] for d in '0123456789')
    m = sum(nxt1[(pair[1], d)] for d in '0123456789')
    if n < 20: return None, n
    s = 0
    for d in '0123456789':
        p = (nxt[(pair, d)] + 0.5) / (n + 5); q = (nxt1[(pair[1], d)] + 0.5) / (m + 5)
        s += p * math.log(p / q)
    return s, n
def klL(pair):
    n = sum(prv[(pair, d)] for d in '0123456789')
    m = sum(prv1[(pair[0], d)] for d in '0123456789')
    if n < 20: return None, n
    s = 0
    for d in '0123456789':
        p = (prv[(pair, d)] + 0.5) / (n + 5); q = (prv1[(pair[0], d)] + 0.5) / (m + 5)
        s += p * math.log(p / q)
    return s, n
rows = []
for pair, c in big.most_common(60):
    kr, n = kl(pair); kl_, n2 = klL(pair)
    exp = uni[pair[0]] * uni[pair[1]] / sum(uni.values())
    rows.append((pair, c, round(c / exp, 2), kr, kl_))
rows.sort(key=lambda x: -(x[3] or 0) - (x[4] or 0))
print('pair  count  obs/exp  KL(next|pair vs next|y)  KL(prev|pair vs prev|x)')
for pair, c, ratio, kr, kl_ in rows:
    print(f'{pair}   {c:4d}   {ratio:5.2f}   {kr if kr is None else round(kr, 3)!s:>7}   {kl_ if kl_ is None else round(kl_, 3)!s:>7}   next: ' + ' '.join(f'{d}:{nxt[(pair, d)]}' for d in '0123456789' if nxt[(pair, d)] > 0))
