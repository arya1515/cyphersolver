import collections, math
text = open('corpus_it.txt', encoding='utf8').read(3000000)
words = text.split()
def mi(pairs):
    c = collections.Counter(pairs); n = sum(c.values())
    a = collections.Counter(); b = collections.Counter()
    for (x, y), v in c.items(): a[x] += v; b[y] += v
    return sum(v / n * math.log(v / n / (a[x] / n * b[y] / n)) for (x, y), v in c.items())
adj = [(w[i], w[i+1]) for w in words for i in range(len(w) - 1)]
skip = [(w[i], w[i+2]) for w in words for i in range(len(w) - 2)]
cross = [(words[i][-1], words[i+1][0]) for i in range(len(words) - 1)]
print(f'within-word adjacent MI = {mi(adj):.3f}  within-word skip-1 MI = {mi(skip):.3f}  across word boundary MI = {mi(cross):.3f}')
# same but after collapsing letters into 10 random classes (polyphony-like) to see the digit-level scale
import random
rnd = random.Random(1)
letters = sorted(set(''.join(words)))
for trial in range(3):
    cls = {ch: rnd.randrange(10) for ch in letters}
    f = lambda prs: mi([(cls[x], cls[y]) for x, y in prs])
    print(f'10-class collapse: adjacent {f(adj):.3f} skip-1 {f(skip):.3f} across-boundary {f(cross):.3f}')
