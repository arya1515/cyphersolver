"""Extra statistics for (a): IC, doublets, per-passage symbol sets; compare to expectations."""
import re, collections, os
HERE = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(HERE, "a_beverning_1653.txt"), encoding="utf-8").read()
segs = re.findall(r"--- CIPHER passage \d ---\n(.*?)\n--- clear", t, re.S)
low = [int(g) for s in segs for g in re.findall(r"\d+", s) if int(g) < 100]
N = len(low); c = collections.Counter(low)
ic = sum(v * (v - 1) for v in c.values()) / (N * (N - 1))
print(f"N={N} distinct={len(c)} IC={ic:.4f}  (uniform over 25 symbols: {1/25:.4f}; Dutch plain ~0.079, French ~0.078, English ~0.066)")
print("frequencies:", sorted(c.items(), key=lambda kv: -kv[1]))
dbl = [(low[i], i) for i in range(N - 1) if low[i] == low[i + 1]]
print(f"doublets: {len(dbl)} ({100*len(dbl)/(N-1):.1f}% of adjacent pairs; Dutch plaintext ~3-4%, homophonic cipher ~1%)", dbl)
# if 20 and 22 were both 'e' (13+12 = 25 = 19.5% ~ Dutch e), what does IC of the merged text look like?
m = [20 if x == 22 else x for x in low]; cm = collections.Counter(m)
print(f"merge 22->20: IC={sum(v*(v-1) for v in cm.values())/(N*(N-1)):.4f}")
# gaps: symbols never used
print("unused in 6..33:", [n for n in range(6, 34) if n not in c])
# passage-by-passage
for i, s in enumerate(segs, 1):
    g = [int(x) for x in re.findall(r"\d+", s)]
    print(f"passage {i}: {len(g)} groups, codes {[x for x in g if x >= 100]}, letters {len([x for x in g if x < 100])}")
