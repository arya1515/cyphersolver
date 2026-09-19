"""Crib-anchored search over the 42 cipher signs of ACA reg. 3225 f. 59r.

Model: each alphabet sign = one letter (homophones allowed: several signs may map to one letter);
the dotted signs sq, bp, O are nomenclator words and are scored as unknown word boundaries (skipped).
Score = Catalan letter n-gram log-probability of the decrypted runs, each run scored with its known
clear context on either side.  Cribs pin some signs; the rest are searched by simulated annealing.

usage: python solve.py lm/catalan.txt [crib=...]
"""
import sys, math, random, re, json, collections

RUNS = [
    # (clear before, signs, clear after)
    ("instancia dels", "ff 6 8L tri 8 sq bp 8R 6 t 8R".split(), "los daquest regne"),
    ("he treballat que", "z a ff 8R 9 d 3 8R v 8R 6 8L 2 O".split(), "es continuada daci a tots sants"),
    ("e", "E n 8R a 8 3 2 8R d ff 8 6 8L E2 8R M z".split(), "stat exseguit e complit"),
]
NOMEN = {"sq", "bp", "O"}          # dotted word signs
ALPHA = "abcdefghilmnopqrstuvxyz"

def load_lm(path, n=4):
    txt = open(path, encoding="utf8", errors="ignore").read().lower()
    txt = re.sub(r"[àá]", "a", txt); txt = re.sub(r"[èé]", "e", txt); txt = re.sub(r"[íï]", "i", txt)
    txt = re.sub(r"[òó]", "o", txt); txt = re.sub(r"[úü]", "u", txt); txt = txt.replace("ç", "c").replace("·", "")
    txt = re.sub(r"[^a-z ]+", " ", txt); txt = re.sub(r"\s+", " ", txt)
    counts = collections.Counter(txt[i:i+n] for i in range(len(txt)-n+1))
    total = sum(counts.values()); floor = math.log(0.01/total)
    return {k: math.log(v/total) for k, v in counts.items()}, floor, n

def score(text, lm):
    tab, floor, n = lm
    return sum(tab.get(text[i:i+n], floor) for i in range(len(text)-n+1))

def decrypt(key):
    out = []
    for before, signs, after in RUNS:
        s = ""
        for g in signs:
            if g in NOMEN: s += " "
            else: s += key.get(g, "?")
        out.append((before, s, after))
    return out

def total_score(key, lm):
    t = 0
    for before, s, after in decrypt(key):
        for chunk in (before[-4:] + s + after[:4]).split(" "):
            if len(chunk) >= 2: t += score(chunk, lm)
    return t

def anneal(lm, fixed, iters=200000, seed=0):
    rnd = random.Random(seed)
    signs = sorted({g for _, s, _ in RUNS for g in s if g not in NOMEN})
    free = [g for g in signs if g not in fixed]
    key = dict(fixed)
    for g in free: key[g] = rnd.choice(ALPHA)
    cur = total_score(key, lm); best = (cur, dict(key)); T = 3.0
    for i in range(iters):
        g = rnd.choice(free); old = key[g]; key[g] = rnd.choice(ALPHA)
        new = total_score(key, lm)
        if new >= cur or rnd.random() < math.exp((new-cur)/T): cur = new
        else: key[g] = old
        if cur > best[0]: best = (cur, dict(key))
        T = max(0.05, 3.0 * (1 - i/iters))
    return best

if __name__ == "__main__":
    lm = load_lm(sys.argv[1])
    fixed = {}
    for a in sys.argv[2:]:
        if a.startswith("crib="):
            for kv in a[5:].split(","):
                k, v = kv.split(":"); fixed[k] = v
    results = []
    for seed in range(int(20)):
        results.append(anneal(lm, fixed, seed=seed))
    results.sort(key=lambda x: -x[0])
    for sc, key in results[:8]:
        print(round(sc, 1), " | ".join(f"{b[-8:]} [{s}] {a[:10]}" for b, s, a in decrypt(key)))
        print("    ", " ".join(f"{k}={v}" for k, v in sorted(key.items())))
