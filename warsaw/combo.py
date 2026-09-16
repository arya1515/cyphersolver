"""Combined 5-gram + dictionary-coverage annealer for R1408.
Score = sum log5(p) over segments + W * (letters covered by lexicon words of length >= 3).
Core symbols 12-33 keep distinct letters (swap only among core); other symbols are free homophones."""
import numpy as np, random, math, sys, json
sys.argv_saved = sys.argv
from wordsolve import load_words, syms, segi, LET, MAXW, segment
import collections
_cnt = collections.Counter(x for sg in segi for x in sg)
core = [i for i, x in enumerate(syms) if x.isdigit() and 12 <= int(x) <= 33 and _cnt[i] >= 2]
assert len(core) <= 20, len(core)

lp5 = np.load('../lucca/it5.npy')
lex = load_words()
lex3 = {w for w in lex if len(w) >= 3}
W = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
segarr = [np.array(sg) for sg in segi]
noncore = [i for i in range(len(syms)) if i not in core]

def cover(txt):
    n = len(txt); best = [0] * (n + 1)
    for i in range(1, n + 1):
        b = best[i - 1]
        for j in range(max(0, i - MAXW), i - 2):
            if txt[j:i] in lex3 and best[j] + (i - j) > b: b = best[j] + (i - j)
        best[i] = b
    return best[n]

def score(key):
    tot = 0.0
    karr = np.array([ord(k) - 97 for k in key])
    for sg in segarr:
        p = karr[sg]
        if len(p) >= 5:
            q = p[:-4] * 456976 + p[1:-3] * 17576 + p[2:-2] * 676 + p[3:-1] * 26 + p[4:]
            tot += float(lp5[q].sum())
        tot += W * cover(''.join(chr(97 + x) for x in p))
    return tot

def anneal(seed, iters=30000, T0=10.0, init=None):
    rnd = random.Random(seed)
    if init: key = list(init)
    else:
        key = [rnd.choice(LET) for _ in syms]
        perm = list(LET); rnd.shuffle(perm)
        for k, i in enumerate(core): key[i] = perm[k]
    cur = score(key); best = (cur, key[:])
    for it in range(iters):
        T = max(0.1, T0 * (1 - it / iters))
        if rnd.random() < 0.6:
            a, b = rnd.sample(core, 2); key[a], key[b] = key[b], key[a]
            new = score(key)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: key[a], key[b] = key[b], key[a]
        else:
            a = rnd.choice(noncore); old = key[a]; key[a] = rnd.choice(LET); new = score(key)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: key[a] = old
        if cur > best[0]: best = (cur, key[:])
    return best

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    init = None
    if len(sys.argv) > 2 and sys.argv[2] != '-':
        k = json.load(open(sys.argv[2])); init = [k.get(x, 'e') for x in syms]
        # repair distinctness on the core
        used = set(); free = [c for c in LET]
        for i in core:
            if init[i] in used: continue
            used.add(init[i])
        free = [c for c in LET if c not in used]
        seen = set()
        for i in core:
            if init[i] in seen: init[i] = free.pop(0)
            seen.add(init[i])
    res = []
    for seed in range(n):
        b = anneal(seed, init=init); res.append(b)
        print(seed, round(b[0], 1), ' | '.join(segment(''.join(b[1][x] for x in sg), lex) for sg in segi), flush=True)
    b = max(res)
    key = {x: b[1][i] for i, x in enumerate(syms)}
    out = sys.argv[4] if len(sys.argv) > 4 else 'key_combo.json'
    json.dump(key, open(out, 'w')); print('KEY', key)
