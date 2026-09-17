# Homophonic solver where some symbols may be nomenclator word-signs: such tokens are removed from the letter
# stream (n-grams span across them) at a per-token cost HC. Only symbols with count <= HMAXC are eligible.
# Usage: python fasthomo_skip.py <lang> <cipher.txt> <iters> <restarts> <seed> [base]
# Env: HT0 HT1 HC HMAXC HPW HINIT (warm start from a MAP line; '#' = word-sign).
import sys, random, time, collections, re, os, ast
import numpy as np
from numba import njit
from homo import ALPHA, load_tokens

K = len(ALPHA); WC = K

@njit(cache=True)
def win_score(text, tab, i, ctx):
    # score of the window ending at letter position i (text[i] != WC); ctx is scratch of size 4
    if text[i] == WC: return 0.0
    j = i - 1; k = 3
    while k >= 0 and j >= 0:
        if text[j] != WC:
            ctx[k] = text[j]; k -= 1
        j -= 1
    if k >= 0: return 0.0
    return tab[ctx[0], ctx[1], ctx[2], ctx[3], text[i]]

@njit(cache=True)
def full_score(text, tab, c):
    n = text.shape[0]; s = 0.0; ctx = np.empty(4, dtype=np.int64)
    for i in range(n):
        if text[i] == WC: s += c
        else: s += win_score(text, tab, i, ctx)
    return s

@njit(cache=True)
def affected(text, positions, npos, mark, stamp, out):
    # letter positions whose window includes any changed position: p itself (if letter) and next 4 letters after p
    n = text.shape[0]; m = 0
    for k in range(npos):
        p = positions[k]
        if mark[p] != stamp:
            mark[p] = stamp; out[m] = p; m += 1
        j = p + 1; cnt = 0
        while j < n and cnt < 4:
            if text[j] != WC:
                cnt += 1
                if mark[j] != stamp:
                    mark[j] = stamp; out[m] = j; m += 1
            j += 1
    return m

@njit(cache=True)
def score_set(text, tab, c, out, m, ctx):
    s = 0.0
    for k in range(m):
        i = out[k]
        if text[i] == WC: s += c
        else: s += win_score(text, tab, i, ctx)
    return s

@njit(cache=True)
def anneal(toks, nsym, tab, c, init_map, iters, T0, T1, seed, sym_pos, sym_start, sym_count, elig, pw, freq, maxw):
    np.random.seed(seed)
    n = toks.shape[0]
    mp = init_map.copy()
    text = np.empty(n, dtype=np.int64)
    for i in range(n): text[i] = mp[toks[i]]
    cur = full_score(text, tab, c)
    best = cur; bestmap = mp.copy()
    buf = np.empty(n, dtype=np.int64); out = np.empty(n, dtype=np.int64); out2 = np.empty(n, dtype=np.int64)
    mark = np.zeros(n, dtype=np.int64); stamp = 0; ctx = np.empty(4, dtype=np.int64)
    for it in range(iters):
        T = T0 * (T1 / T0) ** (it / iters)
        s = np.random.randint(nsym)
        if np.random.random() < 0.8:
            if elig[s] and np.random.random() < pw: u = WC
            else: u = np.random.randint(K)
            if u == mp[s]: continue
            if u == WC and freq[s]:
                # cap on frequent symbols (nulls) mapped to the wildcard
                nf = 0
                for j in range(nsym):
                    if freq[j] and mp[j] == WC: nf += 1
                if nf >= maxw: continue
            cnt = sym_count[s]; st = sym_start[s]
            for k in range(cnt): buf[k] = sym_pos[st + k]
            tot = cnt
        else:
            s2 = np.random.randint(nsym)
            if s2 == s or mp[s2] == mp[s]: continue
            if (mp[s] == WC and not elig[s2]) or (mp[s2] == WC and not elig[s]): continue
            if (mp[s] == WC and freq[s2] and not freq[s]) or (mp[s2] == WC and freq[s] and not freq[s2]): continue
            cnt = sym_count[s]; st = sym_start[s]; cnt2 = sym_count[s2]; st2 = sym_start[s2]
            for k in range(cnt): buf[k] = sym_pos[st + k]
            for k in range(cnt2): buf[cnt + k] = sym_pos[st2 + k]
            tot = cnt + cnt2
            u = -1
        stamp += 1
        m = affected(text, buf, tot, mark, stamp, out)
        # affected set after the change may differ (a letter becoming a word-sign or vice versa shifts contexts);
        # take the union by computing the set after the change too
        before_a = score_set(text, tab, c, out, m, ctx)
        if u >= 0:
            old = mp[s]
            for k in range(tot): text[buf[k]] = u
        else:
            a = mp[s]; b = mp[s2]
            for k in range(cnt): text[buf[k]] = b
            for k in range(cnt2): text[buf[cnt + k]] = a
        m2 = affected(text, buf, tot, mark, stamp, out2)   # same stamp: only positions not already in out
        # before-score of the newly added positions must be evaluated in the old text: undo, score, redo
        if m2 > 0:
            if u >= 0:
                for k in range(tot): text[buf[k]] = old
            else:
                for k in range(cnt): text[buf[k]] = a
                for k in range(cnt2): text[buf[cnt + k]] = b
            before_b = score_set(text, tab, c, out2, m2, ctx)
            if u >= 0:
                for k in range(tot): text[buf[k]] = u
            else:
                for k in range(cnt): text[buf[k]] = b
                for k in range(cnt2): text[buf[cnt + k]] = a
        else:
            before_b = 0.0
        after = score_set(text, tab, c, out, m, ctx) + score_set(text, tab, c, out2, m2, ctx)
        d = after - before_a - before_b
        if d >= 0 or np.random.random() < np.exp(d / T):
            if u >= 0: mp[s] = u
            else: mp[s] = b; mp[s2] = a
            cur += d
        else:
            if u >= 0:
                for k in range(tot): text[buf[k]] = old
            else:
                for k in range(cnt): text[buf[k]] = a
                for k in range(cnt2): text[buf[cnt + k]] = b
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

FREQ = {'en': 'etaoinshrdlucmfyvpbgk', 'fr': 'esaitnrulodcpmvqfgbhxyz', 'la': 'ieautsrnomcldpqbgfhvx'}

def init_map(nsym, lang, rnd):
    order = [ALPHA.index(c) for c in FREQ[lang] if c in ALPHA]
    m = np.zeros(nsym, dtype=np.int64); k = 0.0
    for s in range(nsym):
        m[s] = order[min(len(order) - 1, int(k))]
        k += len(order) / max(1, nsym / 2.2)
        if k >= len(order): k = rnd.random() * 3
    return m

def read_init(path):
    for line in open(path, encoding='utf-8'):
        if line.startswith('MAP '):
            return {s: (ALPHA + '#').index(c) for s, c in ast.literal_eval(line[4:].strip())}
    raise SystemExit('no MAP line in ' + path)

if __name__ == '__main__':
    lang, path, iters, restarts, seed = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    toks = load_tokens(path)
    if len(sys.argv) > 6 and sys.argv[6] == 'base':
        toks = [re.sub(r'[a-z]$', '', t) for t in toks]
    toks = [t for t in toks if t != '?']
    T0 = float(os.environ.get('HT0', '6.0')); T1 = float(os.environ.get('HT1', '0.1'))
    c = float(os.environ.get('HC', '-2.0')); maxc = int(os.environ.get('HMAXC', '3')); pw = float(os.environ.get('HPW', '0.3'))
    maxw = int(os.environ.get('HMAXW', '0'))   # how many frequent symbols (count > HMAXC) may be nulls
    init = read_init(os.environ['HINIT']) if os.environ.get('HINIT') else None
    tab = np.load(f'{lang}5.npy')
    syms, arr, sym_pos, sym_start, sym_count = prepare(toks)
    freq = np.array([cc > maxc for cc in sym_count])
    elig = np.array([cc <= maxc or maxw > 0 for cc in sym_count])
    rnd = random.Random(seed); t0 = time.time()
    best = -1e18; bestmap = None
    for r in range(restarts):
        m0 = np.array([init.get(s, 0) for s in syms], dtype=np.int64) if init else init_map(len(syms), lang, rnd)
        sc, m = anneal(arr, len(syms), tab, c, m0, iters, T0, T1, seed * 1000 + r, sym_pos, sym_start, sym_count, elig, pw, freq, maxw)
        print(f'restart {r} score {sc:.1f} per-letter {sc/len(toks):.3f} wild {int((m==WC).sum())}', flush=True)
        if sc > best: best = sc; bestmap = m.copy()
    A = ALPHA + '#'
    text = ''.join(A[bestmap[t]] for t in arr)
    print('BEST', round(best, 1), 'per-letter', round(best / len(toks), 3), f'{time.time()-t0:.0f}s', 'wild', text.count('#'))
    print(text)
    print('MAP', sorted({syms[i]: A[bestmap[i]] for i in range(len(syms))}.items(), key=lambda x: (len(x[0]), x[0])))
