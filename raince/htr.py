"""Per-token letter classifier + LM beam decode.

Training labels come from the tokens whose 140-cluster sits almost entirely inside one
70-cluster whose glyph shape allows at most two letters; the label is that cluster's value in
map140.json. PCA + Gaussian class-conditionals give a per-token posterior over letters, and a
beam search combines those posteriors with the space-free period-French 6-gram LM.
"""
import json, pickle, collections, numpy as np, sys

X = np.load('feats.npy').astype(np.float64)
a = json.load(open('raince_tokens.json')); b = json.load(open('raince140_tokens.json'))
MAP = {int(k): v for k, v in json.load(open('map140.json')).items()}
ALLOW70 = {
 1:'a',2:'a',3:'b',4:'adl',5:'adl',6:'q',7:'c',8:'c',9:'ca',10:'su',11:'s',12:'su',13:'sui',
 14:'t',15:'t',16:'t',17:'u',18:'tl',19:'tl',20:'aoy',21:'u',22:'u',23:'u',24:'hu',25:'pme',
 26:'e',27:'e',28:'n',29:'e',30:'eng',31:'e',32:'_',33:'mi',34:'tl',35:'tl',36:'d',37:'i',
 38:'er',39:'ne',40:'e',41:'d',42:'n',43:'pml',44:'y',45:'m',46:'tor',47:'f',48:'i',49:'mi',
 50:'r',51:'r',52:'zr',53:'e',54:'l',55:'e',56:'e',57:'i',58:'p',59:'p',60:'s',61:'s',62:'s',
 63:'o',64:'o',65:'oa',66:'s',67:'_',68:'dl',69:'i',70:'i'}
pair = collections.defaultdict(collections.Counter)
for t70, t140 in zip(a['tokens'], b['tokens']): pair[t140['cl']][t70['cl']] += 1
pure = {}
for c140, cnt in pair.items():
    c70, k = cnt.most_common(1)[0]
    if k >= 0.85 * sum(cnt.values()) and len(ALLOW70[c70]) <= 2: pure[c140] = MAP[c140]

y = np.array([pure.get(t['cl'], '?') for t in b['tokens']])
tr = y != '?'
CLS = sorted(set(y[tr]))
print('train', tr.sum(), 'of', len(y), 'classes', CLS)

mu = X.mean(0); Xc = X - mu
U, S, Vt = np.linalg.svd(Xc[tr], full_matrices=False)
K = 55
W = Vt[:K].T
Z = Xc @ W
prior, means, covs = {}, {}, {}
Zt, yt = Z[tr], y[tr]
sh = np.cov(Zt.T) * 0.35
for c in CLS:
    zz = Zt[yt == c]
    prior[c] = np.log(len(zz) / len(Zt))
    means[c] = zz.mean(0)
    covs[c] = np.cov(zz.T) * (len(zz) / (len(zz) + 30)) + sh * (30 / (len(zz) + 30)) + np.eye(K) * 1e-3
logpost = np.zeros((len(Z), len(CLS)))
for j, c in enumerate(CLS):
    ic = np.linalg.inv(covs[c]); sign, ld = np.linalg.slogdet(covs[c])
    d = Z - means[c]
    logpost[:, j] = prior[c] - 0.5 * (np.einsum('ij,jk,ik->i', d, ic, d) + ld)
logpost -= logpost.max(1, keepdims=True)
logpost -= np.log(np.exp(logpost).sum(1, keepdims=True))
acc = (np.array(CLS)[logpost[tr].argmax(1)] == yt).mean()
print('train accuracy', round(float(acc), 3))

D = pickle.load(open('frns6.pkl', 'rb')); N = D['n']; P = D['p']; BACK = D['back']
LMW = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0
CLW = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
BEAM = int(sys.argv[3]) if len(sys.argv) > 3 else 700
TOPK = 5
order = {(t['page'], t['line'], t['x0']): i for i, t in enumerate(b['tokens'])}

def lp(ctx, ch):
    d = P.get(ctx); return d.get(ch, BACK) if d else BACK

out = []
for page in b['regions']:
    rows = [sorted([x for x in b['tokens'] if x['page'] == page and x['line'] == k], key=lambda x: x['x0'])
            for k in range(len(b['regions'][page]['lines']))]
    stream = [order[(t['page'], t['line'], t['x0'])] for r in rows for t in r]
    beams = {' ' * (N - 1): (0.0, ())}
    for i in stream:
        lpv = logpost[i]
        cand = np.argsort(-lpv)[:TOPK]
        opts = [(CLS[j], CLW * lpv[j]) for j in cand]
        nb = {}
        for ctx, (sc, path) in beams.items():
            for ch, e in opts:
                if ch == '_':
                    k2 = ctx; s = sc + e; p = path + ('',)
                else:
                    s = sc + e + LMW * lp(ctx, ch); k2 = (ctx + ch)[-(N - 1):]; p = path + (ch,)
                if k2 not in nb or nb[k2][0] < s: nb[k2] = (s, p)
        beams = dict(sorted(nb.items(), key=lambda kv: -kv[1][0])[:BEAM])
    sc, path = max(beams.values(), key=lambda v: v[0])
    out.append('## ' + page)
    j = 0
    for k, r in enumerate(rows):
        out.append(f'{k+1:02d} ' + ''.join(path[j + i] for i in range(len(r)))); j += len(r)
    print(page, round(sc, 1))
open('draft7.txt', 'w').write('\n'.join(out) + '\n')

# control: f29r line 20 is known glyph for glyph
def lev(a,b):
    import numpy as _np
    d=_np.arange(len(b)+1)
    for i,ca in enumerate(a,1):
        prev=d.copy(); d[0]=i
        for j,cb in enumerate(b,1):
            d[j]=min(prev[j]+1, d[j-1]+1, prev[j-1]+(ca!=cb))
    return int(d[-1])
TRUTH='squiestoitenlacourtdesauoyeestpartypouruenirici'
got=[l for l in open('draft7.txt').read().splitlines() if l.startswith('20 ')][0][3:]
got=got.replace('v','u').replace('y','i')
print('CONTROL lev', lev(got,TRUTH), 'len', len(TRUTH), '->', got)
