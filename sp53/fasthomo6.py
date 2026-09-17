# Fast homophonic solver (numba): symbols -> letters, simulated annealing with incremental 5-gram scoring,
# many restarts. Usage: python fasthomo.py <lang> <cipher.txt> <iters> <restarts> <seed> [base]
# 'base' strips letter suffixes from labels (01a -> 01). Prints best score, text, map.
import sys, random, time, collections, re
import numpy as np
from numba import njit
from homo import ALPHA, load_tokens

K = len(ALPHA)

@njit(cache=True)
def full_score(text, tab):
    n = text.shape[0]; s = 0.0
    for i in range(5, n):
        s += tab[text[i-5], text[i-4], text[i-3], text[i-2], text[i-1], text[i]]
    return s

@njit(cache=True)
def local_score(text, tab, positions, npos):
    # sum over windows ending at i for i in [p, p+4] for each p, deduplicated by a mark array
    n = text.shape[0]; s = 0.0
    for k in range(npos):
        p = positions[k]
        for i in range(p, min(n, p + 6)):
            if i < 5: continue
            # avoid double counting: only count window i if no earlier position q in list also covers it
            dup = False
            for k2 in range(k):
                q = positions[k2]
                if q <= i and i < q + 6:
                    dup = True; break
            if dup: continue
            s += tab[text[i-5], text[i-4], text[i-3], text[i-2], text[i-1], text[i]]
    return s

@njit(cache=True)
def anneal(toks, nsym, tab, init_map, iters, T0, T1, seed, sym_pos, sym_start, sym_count):
    np.random.seed(seed)
    n = toks.shape[0]
    mp = init_map.copy()
    text = np.empty(n, dtype=np.int64)
    for i in range(n): text[i] = mp[toks[i]]
    cur = full_score(text, tab)
    best = cur; bestmap = mp.copy()
    buf = np.empty(n, dtype=np.int64)
    for it in range(iters):
        T = T0 * (T1 / T0) ** (it / iters)
        s = np.random.randint(nsym)
        if np.random.random() < 0.8:
            u = np.random.randint(K)
            if u == mp[s]: continue
            c = sym_count[s]; st = sym_start[s]
            for k in range(c): buf[k] = sym_pos[st + k]
            before = local_score(text, tab, buf, c)
            old = mp[s]
            for k in range(c): text[buf[k]] = u
            after = local_score(text, tab, buf, c)
            d = after - before
            if d >= 0 or np.random.random() < np.exp(d / T):
                mp[s] = u; cur += d
            else:
                for k in range(c): text[buf[k]] = old
        else:
            s2 = np.random.randint(nsym)
            if s2 == s or mp[s2] == mp[s]: continue
            c = sym_count[s]; st = sym_start[s]; c2 = sym_count[s2]; st2 = sym_start[s2]
            for k in range(c): buf[k] = sym_pos[st + k]
            for k in range(c2): buf[c + k] = sym_pos[st2 + k]
            tot = c + c2
            before = local_score(text, tab, buf, tot)
            a = mp[s]; b = mp[s2]
            for k in range(c): text[buf[k]] = b
            for k in range(c2): text[buf[c + k]] = a
            after = local_score(text, tab, buf, tot)
            d = after - before
            if d >= 0 or np.random.random() < np.exp(d / T):
                mp[s] = b; mp[s2] = a; cur += d
            else:
                for k in range(c): text[buf[k]] = a
                for k in range(c2): text[buf[c + k]] = b
        if cur > best:
            best = cur
            for j in range(nsym): bestmap[j] = mp[j]
    return best, bestmap

def prepare(toks):
    syms = sorted(set(toks), key=lambda s: -toks.count(s))
    sid = {s: i for i, s in enumerate(syms)}
    arr = np.array([sid[t] for t in toks], dtype=np.int64)
    pos = collections.defaultdict(list)
    for i, t in enumerate(arr): pos[t].append(i)
    sym_pos = []; sym_start = np.zeros(len(syms), dtype=np.int64); sym_count = np.zeros(len(syms), dtype=np.int64)
    for i in range(len(syms)):
        sym_start[i] = len(sym_pos); sym_count[i] = len(pos[i]); sym_pos += pos[i]
    return syms, arr, np.array(sym_pos, dtype=np.int64), sym_start, sym_count

FREQ = {'en': 'etaoinshrdlucmfyvpbgk', 'fr': 'esaitnrulodcpmvqfgbhxyz', 'es': 'eaosrnidltcumpbgvyqhfz',
        'it': 'eaionlrtscdupmvghfbqz', 'la': 'ieautsrnomcldpqbgfhvx'}

def init_map(nsym, lang, rnd):
    order = [ALPHA.index(c) for c in FREQ[lang] if c in ALPHA]
    m = np.zeros(nsym, dtype=np.int64); k = 0.0
    for s in range(nsym):
        m[s] = order[min(len(order) - 1, int(k))]
        k += len(order) / max(1, nsym / 2.2)
        if k >= len(order): k = rnd.random() * 3
    return m

def solve(lang, toks, iters, restarts, seed, T0=2.0, T1=0.02, verbose=True):
    tab = np.load(f'{lang}6.npy')
    syms, arr, sym_pos, sym_start, sym_count = prepare(toks)
    rnd = random.Random(seed)
    best = -1e18; bestmap = None
    for r in range(restarts):
        m0 = init_map(len(syms), lang, rnd)
        sc, m = anneal(arr, len(syms), tab, m0, iters, T0, T1, seed * 1000 + r, sym_pos, sym_start, sym_count)
        if verbose: print(f'restart {r} score {sc:.1f} per-letter {sc/len(toks):.3f}', flush=True)
        if sc > best: best = sc; bestmap = m.copy()
    text = ''.join(ALPHA[bestmap[t]] for t in arr)
    mapping = {syms[i]: ALPHA[bestmap[i]] for i in range(len(syms))}
    return best, text, mapping

if __name__ == '__main__':
    lang, path, iters, restarts, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    toks = load_tokens(path)
    if len(sys.argv) > 6 and sys.argv[6] == 'base':
        toks = [re.sub(r'[a-z]$', '', t) for t in toks]
    toks = [t for t in toks if t != '?']
    t0 = time.time()
    import os
    best, text, mapping = solve(lang, toks, iters, restarts, seed, T0=float(os.environ.get("HT0", "2.0")), T1=float(os.environ.get("HT1", "0.02")))
    print('BEST', round(best, 1), 'per-letter', round(best / len(toks), 3), f'{time.time()-t0:.0f}s')
    print(text)
    print('MAP', sorted(mapping.items(), key=lambda x: (len(x[0]), x[0])))
