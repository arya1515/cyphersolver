"""Word-boundary-aware attack: 5-gram over 27 symbols (a-z + space) from ../chaulnes/corpus_fr.txt (spaced French,
model on first 95%, controls from the last 5%). Cipher groups are joined by spaces, so the model sees word edges.
Controls: held-out French cut into 37 words (~207 letters), adjacent words merged with prob .2 (the target has
descrupule, lesreigles ...), same homophone multiplicities as Pitt's key.  usage: python solve2.py [restarts]"""
import sys, re, random, collections, statistics, os, numpy as np, key
random.seed(5); np.random.seed(5)
A = 27; SP = 26
raw = open('../chaulnes/corpus_fr.txt', encoding='utf-8').read().replace('v', 'u').replace('j', 'i')  # the cipher has no v/j: u for v, i for j, as in 1644
ROMAN = re.compile(r'[ivxlcdm]+')
words = [w for w in re.sub(r'[^a-z ]', ' ', raw).split() if len(w) < 20 and not ROMAN.fullmatch(w) and not re.search(r'(.)', w) and 'ii' not in w]  # OCR Roman numerals gave an all-i attractor in run2.txt
cut = int(len(words)*0.95); TRAIN = words[:cut]; HELD = words[cut:]
def enc(s): return np.array([SP if c == ' ' else ord(c)-97 for c in s], dtype=np.int64)
def build(out='ng5_frsp.npy'):
    idx = enc(' '.join(TRAIN)); n = len(idx)
    def bc(k):
        v = np.zeros(len(idx)-k+1, dtype=np.int64)
        for j in range(k): v = v*A + idx[j:len(idx)-k+1+j]
        return np.bincount(v, minlength=A**k).astype(np.float32)
    c5, c4, c3, c2 = bc(5), bc(4), bc(3), bc(2)
    p1 = (np.bincount(idx, minlength=A)+1)/(n+A)
    def cond(c, lower):
        c = c.reshape(-1, A); ctx = c.sum(1)
        return (c+5*np.tile(lower, (c.shape[0]//lower.shape[0], 1)))/(ctx[:, None]+5)
    p2 = cond(c2, p1[None, :]); p3 = cond(c3, p2); p4 = cond(c4, p3); p5 = cond(c5, p4)
    lp = np.log(p5).astype(np.float32).reshape(-1); np.save(out, lp); return lp
TAB = np.load('ng5_frsp.npy') if os.path.exists('ng5_frsp.npy') else build()
def score(p):
    q = p[:-4]*A**4+p[1:-3]*A**3+p[2:-2]*A**2+p[3:-1]*A+p[4:]
    return float(TAB[q].sum())
def layout(groups):
    """symbol sequence with space markers: returns (positions array of symbol indices or -1 for space, syms)"""
    syms = sorted({t for g in groups for t in g if t != '|'}); si = {s:i for i,s in enumerate(syms)}
    seq = [-1]
    for g in groups:
        if g == ['|']: continue
        seq += [si[t] for t in g] + [-1]
    return np.array(seq), syms
def anneal(groups, iters=150000, restarts=8, T0=3.0):
    seq, syms = layout(groups); S = len(syms); ispace = seq < 0
    def dec(m):
        out = m[np.where(ispace, 0, seq)]; out[ispace] = SP; return out
    best = (-1e9, None)
    for r in range(restarts):
        m = np.random.randint(0, 26, S); cur = score(dec(m)); bl = (cur, m.copy())
        for it in range(iters):
            T = T0*(1-it/iters)+0.05
            n = m.copy()
            if random.random() < 0.7: n[random.randrange(S)] = random.randrange(26)
            else:
                i, j = random.sample(range(S), 2); n[i], n[j] = n[j], n[i]
            sc = score(dec(n))
            if sc >= cur or random.random() < np.exp((sc-cur)/T):
                m, cur = n, sc
                if cur > bl[0]: bl = (cur, m.copy())
        if bl[0] > best[0]: best = bl
    return best[0], {s: 'abcdefghijklmnopqrstuvwxyz'[best[1][i]] for i, s in enumerate(syms)}
def render(groups, k): return ' '.join('|' if g == ['|'] else ''.join(k[t] for t in g) for g in groups)
def acc(groups, k, truth):
    toks = [t for g in groups for t in g if t != '|']; return sum(k[t] == truth[t] for t in toks)/len(toks)
def make_control(seed, n_letters=207):
    rnd = random.Random(seed)
    while True:
        start = rnd.randrange(len(HELD)-80); ws = []; n = 0
        for w in HELD[start:]:
            if n + len(w) > n_letters + 3: break
            ws.append(w); n += len(w)
        if abs(n-n_letters) <= 3: break
    gs = []
    for w in ws:
        if gs and rnd.random() < 0.2 and len(gs[-1]) < 7: gs[-1] += w
        else: gs.append(w)
    pt = ''.join(gs)
    mult = sorted(collections.Counter(key.KEY.values()).values(), reverse=True)
    letters = [l for l, _ in collections.Counter(pt).most_common()]
    symbols = list(range(1000)); rnd.shuffle(symbols); k = {}
    for i, l in enumerate(letters):
        for _ in range(mult[i] if i < len(mult) else 1): k[str(symbols.pop())] = l
    inv = collections.defaultdict(list)
    for s, l in k.items(): inv[l].append(s)
    groups = [[rnd.choice(inv[c]) for c in g] for g in gs]
    return groups, k, ' '.join(gs)
if __name__ == '__main__':
    R = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    gs = key.groups()
    seqp = enc(' ' + render(gs, key.KEY).replace(' | ', ' ') + ' '); real = score(seqp)
    letters = sorted(set(key.KEY.values())); null = []
    for i in range(20000):
        p = letters[:]; random.shuffle(p); mp = {a: b for a, b in zip(letters, p)}
        null.append(score(enc(' ' + render(gs, {t: mp[v] for t, v in key.KEY.items()}).replace(' | ', ' ') + ' ')))
    mu, sd = statistics.mean(null), statistics.pstdev(null)
    print(f'PERMUTATION TEST (spaced model): Pitt key {real:.1f}; null mean {mu:.1f} sd {sd:.1f} max {max(null):.1f}; z={(real-mu)/sd:.1f}; #>=real {sum(x>=real for x in null)}/20000', flush=True)
    sc, k = anneal(gs, restarts=R)
    print(f'TARGET blind (word edges): score {sc:.1f} (Pitt {real:.1f}); agreement with Pitt key {acc(gs,k,key.KEY):.3f}')
    print('   reading:', render(gs, k), flush=True)
    for seed in range(6):
        cg, tk, pt = make_control(seed)
        sc, k = anneal(cg, restarts=R)
        truth = score(enc(' '+pt+' '))
        print(f'CONTROL {seed}: found {sc:.1f} truth {truth:.1f} letters right {acc(cg,k,tk):.3f} | {render(cg,k)[:90]}', flush=True)
