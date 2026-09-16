"""Key-free ADFGVX attack for the messages no published key reads: recover the columnar transposition without
knowing the substitution square, by annealing the column order for each key length and scoring how much the
resulting letter pairs look like a monoalphabetic substitution of German (index of coincidence of the 36 pairs,
plus a bonus for pairs concentrating on few symbols). Then solve the substitution with the German quadgram model.

A planted control at the same length is run first; if the control is not recovered, the message is below what
this method can do at that length and the negative is recorded as such.

Usage: python keyless.py PAGE[+PAGE] [nmin nmax restarts iters]     python keyless.py control LEN
"""
import collections, math, random, sys
import gaps, lm_de, repair

SYM = 'ADFGVX'

def untrans(ct, order):
    """order[k] = column read k-th (0-based). Returns row-wise stream."""
    n = len(order); L = len(ct); rows, rem = divmod(L, n)
    h = [rows + 1 if c < rem else rows for c in range(n)]
    cols = {}; i = 0
    for c in order:
        cols[c] = ct[i:i + h[c]]; i += h[c]
    return ''.join(cols[c][r] for r in range(rows + 1) for c in range(n) if r < h[c])

def pair_score(s):
    pairs = [s[i:i + 2] for i in range(0, len(s) - 1, 2)]
    c = collections.Counter(pairs); N = len(pairs)
    ic = sum(v * (v - 1) for v in c.values()) / (N * (N - 1))
    return ic

def anneal_order(ct, n, iters, rng):
    order = list(range(n)); rng.shuffle(order)
    cur = pair_score(untrans(ct, order)); best = (cur, list(order))
    T0, T1 = 0.004, 0.0002
    for it in range(iters):
        T = T0 * (T1 / T0) ** (it / iters)
        o2 = list(order); r = rng.random()
        if r < 0.5:
            a, b = rng.randrange(n), rng.randrange(n); o2[a], o2[b] = o2[b], o2[a]
        elif r < 0.8:
            a, b = sorted((rng.randrange(n), rng.randrange(n))); o2[a:b + 1] = reversed(o2[a:b + 1])
        else:
            a = rng.randrange(n); x = o2.pop(a); o2.insert(rng.randrange(n), x)
        v = pair_score(untrans(ct, o2))
        if v >= cur or rng.random() < math.exp((v - cur) / T):
            order, cur = o2, v
            if cur > best[0]: best = (cur, list(order))
    return best

def solve_sub(pairs, iters=20000, rng=None):
    """monoalphabetic: map each of the distinct pairs to a letter, anneal on quadgrams."""
    rng = rng or random.Random(0)
    syms = sorted(set(pairs)); letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    freq = collections.Counter(pairs)
    # start: frequency order onto German letter frequency order
    de = 'ENISRATDHULCGMOBWFKZPVJYXQ0123456789'
    m = {s: de[i] for i, s in enumerate(sorted(syms, key=lambda s: -freq[s]))}
    def txt(m): return ''.join(m[p] for p in pairs)
    cur = lm_de.score(txt(m)); best = (cur, dict(m))
    for it in range(iters):
        T = 2.0 * (0.05 / 2.0) ** (it / iters)
        a, b = rng.sample(syms, 2) if len(syms) > 1 else (syms[0], syms[0])
        m2 = dict(m); m2[a], m2[b] = m[b], m[a]      # swaps only: the mapping stays one-to-one
        v = lm_de.score(txt(m2))
        if v >= cur or rng.random() < math.exp((v - cur) / T):
            m, cur = m2, v
            if cur > best[0]: best = (cur, dict(m))
    return best[0], txt(best[1])

def attack(ct, nmin=15, nmax=23, restarts=6, iters=30000, seed=1):
    rng = random.Random(seed)
    out = []
    for n in range(nmin, nmax + 1):
        bests = [anneal_order(ct, n, iters, rng) for _ in range(restarts)]
        ic, order = max(bests)
        s = untrans(ct, order); pairs = [s[i:i + 2] for i in range(0, len(s) - 1, 2)]
        sc, pt = solve_sub(pairs, rng=rng)
        out.append((lm_de.per(pt), ic, n, order, pt))
        print('n=%2d  pairIC %.4f  german %.3f  %s' % (n, ic, out[-1][0], pt[:70]), flush=True)
    out.sort(reverse=True)
    return out[0]

def control(L, n=None, seed=3):
    rng = random.Random(seed)
    text = open('corpus/de_34811.txt', encoding='utf-8', errors='ignore').read()
    pt = lm_de.clean(text[200000:200000 + 4 * L])[:L // 2]
    square = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'); rng.shuffle(square)
    n = n or rng.randrange(16, 23)
    frac = ''.join(SYM[square.index(ch) // 6] + SYM[square.index(ch) % 6] for ch in pt)
    order = list(range(n)); rng.shuffle(order)
    # encrypt: write rows of n, read columns in order
    rows, rem = divmod(len(frac), n)
    cols = [''.join(frac[r * n + c] for r in range(rows + (1 if c < rem else 0))) for c in range(n)]
    ct = ''.join(cols[c] for c in order)
    print('control: %d letters, key length %d, plaintext %s...' % (len(ct), n, pt[:40]))
    best = attack(ct, 15, 23, seed=seed)
    print('control result: n=%d german %.3f  %s' % (best[2], best[0], best[4][:80]))
    print('recovered' if best[2] == n and best[4][:20] == pt[:20] else 'NOT recovered')

if __name__ == '__main__':
    if sys.argv[1] == 'control':
        control(int(sys.argv[2]))
    else:
        pages = sys.argv[1].split('+')
        msgs = gaps.parse()
        ct = ''.join(next(m for m in msgs if m['page'] == p)['ct'].replace('#', '') for p in pages)
        print('pages', pages, len(ct), 'letters')
        a = [int(x) for x in sys.argv[2:]]
        best = attack(ct, *(a or []))
        print('BEST n=%d german %.3f\n%s' % (best[2], best[0], best[4]))
