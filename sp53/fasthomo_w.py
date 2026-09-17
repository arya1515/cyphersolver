# Homophonic solver with a wildcard class for nomenclator word-signs, and optional warm start.
# Usage: python fasthomo_w.py <lang> <cipher.txt> <iters> <restarts> <seed> [base]
# Env: HT0, HT1 (schedule), HW (wildcard window score, e.g. -2.6; 0 disables), HMAXC (max count of a symbol eligible
#      for wildcard, default 3), HINIT (file whose MAP line seeds every restart; then HT0 is the reheat temperature).
import sys, random, time, collections, re, os, ast
import numpy as np
from numba import njit
from homo import ALPHA, load_tokens

K = len(ALPHA); WC = K          # wildcard index

@njit(cache=True)
def full_score(text, tab):
    n = text.shape[0]; s = 0.0
    for i in range(4, n):
        s += tab[text[i-4], text[i-3], text[i-2], text[i-1], text[i]]
    return s

@njit(cache=True)
def local_score(text, tab, positions, npos):
    n = text.shape[0]; s = 0.0
    for k in range(npos):
        p = positions[k]
        for i in range(p, min(n, p + 5)):
            if i < 4: continue
            dup = False
            for k2 in range(k):
                q = positions[k2]
                if q <= i and i < q + 5:
                    dup = True; break
            if dup: continue
            s += tab[text[i-4], text[i-3], text[i-2], text[i-1], text[i]]
    return s

@njit(cache=True)
def anneal(toks, nsym, tab, init_map, iters, T0, T1, seed, sym_pos, sym_start, sym_count, elig, pw):
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
        r = np.random.random()
        if r < 0.8:
            if elig[s] and np.random.random() < pw: u = WC
            else: u = np.random.randint(K)
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
            if (mp[s] == WC and not elig[s2]) or (mp[s2] == WC and not elig[s]): continue
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

def ext_table(lang, W):
    t = np.load(f'{lang}5.npy')
    if W == 0:
        return t
    e = np.full((K + 1,) * 5, np.float32(W), dtype=np.float32)
    e[:K, :K, :K, :K, :K] = t
    return e

def solve(lang, toks, iters, restarts, seed, T0, T1, W, maxc, pw, init=None, verbose=True):
    tab = ext_table(lang, W)
    syms, arr, sym_pos, sym_start, sym_count = prepare(toks)
    elig = np.array([bool(W != 0 and c <= maxc) for c in sym_count])
    rnd = random.Random(seed)
    best = -1e18; bestmap = None
    for r in range(restarts):
        if init is not None:
            m0 = np.array([init.get(s, 0) for s in syms], dtype=np.int64)
        else:
            m0 = init_map(len(syms), lang, rnd)
        sc, m = anneal(arr, len(syms), tab, m0, iters, T0, T1, seed * 1000 + r, sym_pos, sym_start, sym_count, elig, pw)
        if verbose: print(f'restart {r} score {sc:.1f} per-letter {sc/len(toks):.3f} wild {int((m==WC).sum())}', flush=True)
        if sc > best: best = sc; bestmap = m.copy()
    A = ALPHA + '#'
    text = ''.join(A[bestmap[t]] for t in arr)
    mapping = {syms[i]: A[bestmap[i]] for i in range(len(syms))}
    return best, text, mapping

def read_init(path):
    for line in open(path, encoding='utf-8'):
        if line.startswith('MAP '):
            items = ast.literal_eval(line[4:].strip())
            return {s: (ALPHA + '#').index(c) for s, c in items}
    raise SystemExit('no MAP line in ' + path)

if __name__ == '__main__':
    lang, path, iters, restarts, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    toks = load_tokens(path)
    if len(sys.argv) > 6 and sys.argv[6] == 'base':
        toks = [re.sub(r'[a-z]$', '', t) for t in toks]
    toks = [t for t in toks if t != '?']
    T0 = float(os.environ.get('HT0', '6.0')); T1 = float(os.environ.get('HT1', '0.1'))
    W = float(os.environ.get('HW', '0')); maxc = int(os.environ.get('HMAXC', '3')); pw = float(os.environ.get('HPW', '0.3'))
    init = read_init(os.environ['HINIT']) if os.environ.get('HINIT') else None
    t0 = time.time()
    best, text, mapping = solve(lang, toks, iters, restarts, seed, T0, T1, W, maxc, pw, init)
    print('BEST', round(best, 1), 'per-letter', round(best / len(toks), 3), f'{time.time()-t0:.0f}s', 'wild', text.count('#'))
    print(text)
    print('MAP', sorted(mapping.items(), key=lambda x: (len(x[0]), x[0])))
