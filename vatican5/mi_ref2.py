import collections, math, random
text = open('corpus_it.txt', encoding='utf8').read(2500000)
rnd = random.Random(0)
def mi(pairs):
    c = collections.Counter(pairs); n = sum(c.values())
    a = collections.Counter(); b = collections.Counter()
    for (x, y), v in c.items(): a[x] += v; b[y] += v
    return sum(v / n * math.log(v / n / (a[x] / n * b[y] / n)) for (x, y), v in c.items())
def mi_corr(pairs, k=5):
    m = mi(pairs); ys = [y for _, y in pairs]; base = 0
    for _ in range(k):
        rnd.shuffle(ys); base += mi([(x, y) for (x, _), y in zip(pairs, ys)])
    return m - base / k
# text with spaces as a symbol
t = ' ' + text.replace('\n', ' ') + ' '
freq = collections.Counter(t)
print('I(x;y | middle=d) in Italian letters (space = word boundary null):')
res = []
for d, f in freq.most_common(22):
    trip = [(t[i-1], t[i+1]) for i in range(1, len(t) - 1) if t[i] == d][:20000]
    res.append((d, f / len(t), mi_corr(trip)))
for d, p, m in sorted(res, key=lambda x: x[2]):
    print(f"  {d!r}: freq={p:.3f}  across={m:.3f}")
# same after collapsing letters into 10 classes with the real-cipher-like frequencies? just random classes
letters = [ch for ch in freq if ch != ' ']
cls = {ch: rnd.randrange(9) for ch in letters}; cls[' '] = 9
c = [cls[ch] for ch in t]
print('\n10-class collapse (class 9 = space):')
for d in range(10):
    trip = [(c[i-1], c[i+1]) for i in range(1, len(c) - 1) if c[i] == d][:20000]
    print(f'  class {d}: across={mi_corr(trip):.3f}  members={"".join(k for k, v in cls.items() if v == d)}')
