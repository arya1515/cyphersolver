"""(a) Beverning/Vande Perre 1653: hill-climb a (possibly homophonic) substitution on numbers 6..33.
usage: solve_a.py [nl|fr|en] [restarts] [seed]"""
import re, json, math, os, random, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__))
lang = sys.argv[1] if len(sys.argv) > 1 else "nl"
RESTARTS = int(sys.argv[2]) if len(sys.argv) > 2 else 40
random.seed(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
txt = open(os.path.join(HERE, "a_beverning_1653.txt"), encoding="utf-8").read()
segs = re.findall(r"--- CIPHER passage \d ---\n(.*?)\n--- clear", txt, re.S)
groups = [g for s in segs for g in re.findall(r"\d+", s)]
low = [int(g) for g in groups if int(g) < 100]          # 3-digit groups are code words: skipped
syms = sorted(set(low))
lmpath = os.path.join(HERE, f"lm_{lang}.json") if lang != "en" else os.path.join(HERE, "..", "beale", "en_lm.json")
J = json.load(open(lmpath))["quad"]; TOT = sum(J.values())
LM = {k: math.log10(v / TOT) for k, v in J.items()}; FLOOR = math.log10(0.01 / TOT)
ALPH = "abcdefghijklmnopqrstuvwxyz"
def score(key):
    pt = "".join(key[n] for n in low)
    return sum(LM.get(pt[i:i+4], FLOOR) for i in range(len(pt) - 3))
def climb():
    # init: frequency-ordered symbols -> frequency-ordered letters of the language
    order = [s for s, _ in collections.Counter(low).most_common()]
    freq = collections.Counter(); 
    for q, v in J.items(): freq[q[0]] += v
    letters = [l for l, _ in freq.most_common()]
    key = {s: letters[i % 26] for i, s in enumerate(order)}
    best = score(key); T = 2.0
    for it in range(20000):
        k2 = dict(key)
        if random.random() < 0.5:                       # reassign one symbol to any letter (allows homophones)
            k2[random.choice(syms)] = random.choice(ALPH)
        else:                                           # swap two symbols
            a, b = random.sample(syms, 2); k2[a], k2[b] = key[b], key[a]
        sc = score(k2)
        if sc > best or random.random() < math.exp((sc - best) / T):
            key, best = k2, sc
        T = max(0.05, T * 0.9997)
    return best, key
results = []
for r in range(RESTARTS):
    results.append(climb())
results.sort(key=lambda x: -x[0])
print(f"lang={lang} letters={len(low)} symbols={len(syms)}  (score = sum log10 quadgram; per-quad avg shown)")
for sc, key in results[:5]:
    pt = "".join(key[n] for n in low)
    print(f"\n{sc/ (len(low)-3):.3f}  key: " + " ".join(f"{s}={key[s]}" for s in syms))
    pos = 0
    for s in segs:
        gs = re.findall(r"\d+", s)
        print("   " + "".join((key[int(g)] if int(g) < 100 else f"[{g}]") for g in gs))
