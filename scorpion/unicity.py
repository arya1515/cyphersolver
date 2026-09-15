"""unicity.py -- are the Scorpion ciphers solvable at all as homophonic substitutions?
(1) Shannon unicity: key information (each distinct symbol independently assigned one of 26 letters) against
    the redundancy of English (about 3.2 bits per letter for a 4.7-bit alphabet).
(2) Matched control: random 70- and 180-letter English passages enciphered with random homophonic keys that
    reproduce the observed number of distinct symbols, attacked with a 5-gram English LM annealer.
"""
import sys, math, random, collections, pickle, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'copenhagen'))
sys.argv = [sys.argv[0]]                       # keep solve.py's argument parsing quiet
import solve as cp
cp.CORPUS = pathlib.Path(r'C:/Users/DANIEL~1.BOU/AppData/Local/Temp/claude/C--Users-Daniel-Bourdeau-cipher/bfb7c2bf-254a-4a86-b088-f16d86b54a8f/scratchpad/t50')
lm = cp.build_lm('en')
for name, n, k in [('S1', 70, 53), ('S5', 180, 145)]:
    key_bits = k * math.log2(26); red = n * (math.log2(26) - 1.5)   # English ~1.5 bits/letter entropy
    print(f'{name}: {n} symbols, {k} distinct -> key {key_bits:.0f} bits vs redundancy {red:.0f} bits -> '
          f'{"below" if key_bits > red else "above"} unicity distance (ratio {key_bits/red:.2f})')
# control
rng = random.Random(3)
# build a plaintext pool from the cached English LM's source is not kept; use a fixed literary passage instead
pool = ("it was the best of times it was the worst of times it was the age of wisdom it was the age of foolishness "
        "it was the epoch of belief it was the epoch of incredulity it was the season of light it was the season of "
        "darkness it was the spring of hope it was the winter of despair we had everything before us we had nothing "
        "before us we were all going direct to heaven we were all going direct the other way in short the period was "
        "so far like the present period that some of its noisiest authorities insisted on its being received for good "
        "or for evil in the superlative degree of comparison only there were a king with a large jaw and a queen with "
        "a plain face on the throne of england there were a king with a large jaw and a queen with a fair face on the "
        "throne of france in both countries it was clearer than crystal to the lords of the state preserves of loaves "
        "and fishes that things in general were settled for ever").replace(' ', '')
def encipher(pt, k):
    # homophonic key with k distinct symbols: give each letter at least one symbol, distribute the rest by frequency
    letters = sorted(set(pt)); syms = {l: [l + '0'] for l in letters}
    extra = k - len(letters); freq = collections.Counter(pt)
    order = [l for l, _ in freq.most_common()]
    i = 0
    while extra > 0:
        l = order[i % len(order)]; i += 1
        if len(syms[l]) < freq[l]: syms[l].append(l + str(len(syms[l]))); extra -= 1
    ct = []; used = collections.defaultdict(int)
    for ch in pt:
        s = syms[ch][used[ch] % len(syms[ch])]; used[ch] += 1; ct.append(s)
    return ct
def anneal(ct, restarts=8, iters=15000):
    syms = sorted(set(ct)); letters = list('abcdefghijklmnopqrstuvwxyz')
    best_all = (-1e18, None)
    for r in range(restarts):
        m = {s: rng.choice(letters) for s in syms}
        def sc_of(mm): return lm.score([''.join(mm[s] for s in ct)])
        sc = sc_of(m); best = (sc, dict(m))
        for it in range(iters):
            T = 3.0 * (0.05 / 3.0) ** (it / iters)
            m2 = dict(m); m2[rng.choice(syms)] = rng.choice(letters)
            s2 = sc_of(m2)
            if s2 >= sc or rng.random() < math.exp((s2 - sc) / T):
                m, sc = m2, s2
                if sc > best[0]: best = (sc, dict(m))
        if best[0] > best_all[0]: best_all = best
    return best_all
for name, n, k in [('S1', 70, 53), ('S5', 180, 145)]:
    for trial in range(2):
        start = rng.randrange(0, len(pool) - n); pt = pool[start:start+n]
        ct = encipher(pt, k)
        assert len(set(ct)) == k
        sc, m = anneal(ct)
        dec = ''.join(m[s] for s in ct)
        acc = sum(1 for a, b in zip(dec, pt) if a == b) / n
        true_sc = lm.score([pt])
        print(f'{name}-control {trial+1}: truth score {true_sc:.1f}, found {sc:.1f}, letter accuracy {acc:.2f}\n   found: {dec}\n   truth: {pt}')
