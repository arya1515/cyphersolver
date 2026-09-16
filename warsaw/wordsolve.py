"""Word-segmentation hill-climb for R1408.
Symbols: two-digit groups plus the letter pairs (ll zg fi lu pr th o p n); a and m are dropped as nulls;
three-digit groups split the text into segments. Score = best unigram word segmentation (DP) with an
unknown-word penalty, over the Italian corpus in ../lucca/corpus (v->u, j->i)."""
import numpy as np, random, math, sys, re, collections, unicodedata, glob, json

def clean_words(t):
    t = unicodedata.normalize('NFKD', t.lower()); t = ''.join(c for c in t if not unicodedata.combining(c))
    t = t.replace('v', 'u').replace('j', 'i').replace('y', 'i')
    return [w for w in re.findall(r'[a-z]+', t) if not re.search(r'[kwx]', w)]

def load_words():
    cnt = collections.Counter()
    for f in glob.glob('../lucca/corpus/*.txt'):
        cnt.update(clean_words(open(f, encoding='utf-8', errors='ignore').read()))
    # add 17th-century spellings / frequent words missing from a 19th-c. corpus
    extra = 'et hauer hauere hauendo hauuto hauea haueua hauendosi maesta mta sua vostra vra polonia suetia suecia turco turchi tartari moscouia cosacchi re regina imperatore cesare cesarea gustauo danzica prussia lituania senato dieta nuntio nuncio vienna cracouia varsouia'.split()
    for w in extra: cnt[w] += 20
    tot = sum(cnt.values())
    lp = {w: math.log(c / tot) for w, c in cnt.items() if c >= 2}
    return lp

toks = open('ct.txt').read().split()
s = ' '.join(toks)
for pr in ['l l', 'z g', 'f i', 'p r', 'l u', 't h']: s = s.replace(pr, pr.replace(' ', ''))
toks = s.split()
seq = [t for t in toks if t not in ('a', 'm')]
segs = []; cur = []
for t in seq:
    if t.isdigit() and len(t) == 3:
        if cur: segs.append(cur); cur = []
    else: cur.append(t)
if cur: segs.append(cur)
syms = sorted(set(t for sg in segs for t in sg)); pos = {x: i for i, x in enumerate(syms)}
core = [i for i, x in enumerate(syms) if x.isdigit() and 12 <= int(x) <= 33]
segi = [[pos[x] for x in sg] for sg in segs]
LET = 'abcdefghilmnopqrstuz'
MAXW = 14
UNK = -12.0  # per-letter cost of an unknown word

def seg_score(txt, lp):
    n = len(txt); best = [0.0] + [-1e18] * n
    for i in range(1, n + 1):
        b = best[i - 1] + UNK
        for j in range(max(0, i - MAXW), i):
            w = txt[j:i]
            v = lp.get(w)
            if v is not None and best[j] + v > b: b = best[j] + v
        best[i] = b
    return best[n]

def total(key, lp):
    return sum(seg_score(''.join(key[x] for x in sg), lp) for sg in segi)

def decode(key):
    return ' | '.join(''.join(key[x] for x in sg) for sg in segi)

def segment(txt, lp):
    n = len(txt); best = [0.0] + [-1e18] * n; back = [0] * (n + 1)
    for i in range(1, n + 1):
        b = best[i - 1] + UNK; bj = i - 1
        for j in range(max(0, i - MAXW), i):
            v = lp.get(txt[j:i])
            if v is not None and best[j] + v > b: b = best[j] + v; bj = j
        best[i] = b; back[i] = bj
    out = []; i = n
    while i > 0: out.append(txt[back[i]:i]); i = back[i]
    return ' '.join(reversed(out))

def anneal(seed, lp, iters=20000, T0=30.0, init=None):
    rnd = random.Random(seed)
    key = list(init) if init else [rnd.choice(LET) for _ in syms]
    if not init:
        perm = list(LET); rnd.shuffle(perm)
        for k, i in enumerate(core): key[i] = perm[k % 20]
    cur = total(key, lp); best = (cur, key[:])
    for it in range(iters):
        T = max(0.5, T0 * (1 - it / iters))
        a = rnd.randrange(len(syms)); old = key[a]
        if a in core or rnd.random() < 0.5:
            b = rnd.randrange(len(syms)); key[a], key[b] = key[b], key[a]
            new = total(key, lp)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: key[a], key[b] = key[b], key[a]
        else:
            key[a] = rnd.choice(LET); new = total(key, lp)
            if new > cur or rnd.random() < math.exp((new - cur) / T): cur = new
            else: key[a] = old
        if cur > best[0]: best = (cur, key[:])
    return best

if __name__ == '__main__':
    lp = load_words()
    print('lexicon', len(lp), 'symbols', len(syms), syms, 'letters', sum(len(sg) for sg in segi))
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    init = None
    if len(sys.argv) > 2:
        k = json.load(open(sys.argv[2])); init = [k.get(x, 'e') for x in syms]
    res = []
    for seed in range(n):
        b = anneal(seed, lp, init=init); res.append(b)
        print(seed, round(b[0], 1), decode(b[1]), flush=True)
    b = max(res)
    key = {x: b[1][i] for i, x in enumerate(syms)}
    json.dump(key, open('key_word.json', 'w'))
    print('KEY', key)
    for sg in segi: print(segment(''.join(b[1][x] for x in sg), lp))
