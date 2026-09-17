"""EM alignment of cipher tokens to known plaintext (monotone, each token -> 0..K letters; plaintext letters may be
skipped at a cost to survive paraphrase). Learns P(unit | token) shared across all passages of corpus.txt.
usage: python em_align.py [iters] [--show]"""
import sys, math, collections, re
sys.stdout.reconfigure(encoding='utf-8')
ITERS = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 40
SHOW = '--show' in sys.argv
KMAX_LET, KMAX_SIGN = 1, 12
LOG0 = -1e9

def load(path='bethune/corpus.txt'):
    out = []
    for l in open(path, encoding='utf-8'):
        if not l.strip() or l.startswith('#'): continue
        pid, src, ct, pt = [x.strip() for x in l.split('|')]
        pt = re.sub(r'[^a-z]', '', pt.lower().replace('j', 'i').replace('v', 'u'))
        toks=ct.replace('s: 4 8','s: 48').replace('48 1 7','48 17').replace('f s 4 8','f s 48').split()
        out.append((pid, toks, pt))
    return out

def is_sign(tok):
    """word/syllable-capable tokens: figures and marked letters; everything else is a letter symbol (0 or 1 letter)"""
    return any(ch.isdigit() for ch in tok) or any(m in tok for m in ",:'.^_")

def lse(a, b):
    if a == LOG0: return b
    if b == LOG0: return a
    m = max(a, b); return m + math.log(math.exp(a-m) + math.exp(b-m))

def prior_logp(tok, u):
    """proper prior over strings: P(len) spread uniformly over the 22^len strings of that length"""
    k = len(u)
    if k == 0: return math.log(0.25 if tok in NULLABLE else 0.002)
    if is_sign(tok):
        pl = {1: .35, 2: .25, 3: .12, 4: .08}.get(k, .19 / 8)
    else:
        if k > 1: return LOG0
        pl = 1.0
    return math.log(pl) - k * math.log(22.0)

SEED = {'Z':'e','ff':'e','q':'t','v':'i','x':'m','h':'l','B':'l','o':'p','T':'p','b':'c','f':'o','+':'o','t':'o','4':'a','6':'a',
        'u':'a','y':'u','c':'u','r':'r','d':'r','a':'i','l':'h','e':'c','7':'t','1':'i','0':'e','63':'re','61':'qui','f,':'le',
        'g,':'la','x,':'que','r,':'par','s,':'pro','x:':'et','x^':'et','48':'cardinal','17':'aldobrandin','65':'si','d,':'ie','DL,':'ie',
        't:':'de','t.':'de','p:':'ce','p.':'ce','J':'bon','J,':'mais'}
NULLABLE = {'PH','HB','$','Y','LS'}
SEEDW = 6.0
class Model:
    def __init__(self, data):
        self.counts = collections.defaultdict(lambda: collections.defaultdict(float))
        self.tot = collections.defaultdict(float)
        self.alpha = 3.0
        self.skip = math.log(0.004)       # skipping a plaintext letter (paraphrase / clear word not enciphered)
    def logp(self, tok, u):
        c = self.counts[tok].get(u, 0.0); t = self.tot[tok]
        seed = SEEDW if SEED.get(tok) == u else 0.0
        return math.log((c + seed + self.alpha * math.exp(prior_logp(tok, u))) / (t + self.alpha + (SEEDW if tok in SEED else 0.0)))

def kmax(tok): return KMAX_SIGN if is_sign(tok) else KMAX_LET

def forward_backward(model, ct, pt, collect=True):
    n, m = len(ct), len(pt)
    # alpha[i][j]: log prob of consuming i tokens and j letters
    A = [[LOG0]*(m+1) for _ in range(n+1)]; A[0][0] = 0.0
    for i in range(n+1):
        for j in range(m+1):
            a = A[i][j]
            if a == LOG0: continue
            if j < m: A[i][j+1] = lse(A[i][j+1], a + model.skip)          # skip plaintext letter
            if i < n:
                tok = ct[i]
                for k in range(0, min(kmax(tok), m-j)+1):
                    A[i+1][j+k] = lse(A[i+1][j+k], a + model.logp(tok, pt[j:j+k]))
    Z = A[n][m]
    if Z == LOG0 or not collect: return Z, None
    Bk = [[LOG0]*(m+1) for _ in range(n+1)]; Bk[n][m] = 0.0
    for i in range(n, -1, -1):
        for j in range(m, -1, -1):
            b = LOG0
            if j < m and Bk[i][j+1] != LOG0: b = lse(b, model.skip + Bk[i][j+1])
            if i < n:
                tok = ct[i]
                for k in range(0, min(kmax(tok), m-j)+1):
                    if Bk[i+1][j+k] != LOG0: b = lse(b, model.logp(tok, pt[j:j+k]) + Bk[i+1][j+k])
            if i == n and j == m: b = 0.0
            Bk[i][j] = b
    post = collections.defaultdict(float)
    for i in range(n):
        tok = ct[i]
        for j in range(m+1):
            if A[i][j] == LOG0: continue
            for k in range(0, min(kmax(tok), m-j)+1):
                if Bk[i+1][j+k] == LOG0: continue
                p = math.exp(A[i][j] + model.logp(tok, pt[j:j+k]) + Bk[i+1][j+k] - Z)
                if p > 1e-6: post[(tok, pt[j:j+k])] += p
    return Z, post

def viterbi(model, ct, pt):
    n, m = len(ct), len(pt)
    V = [[LOG0]*(m+1) for _ in range(n+1)]; bp = {}
    V[0][0] = 0.0
    for i in range(n+1):
        for j in range(m+1):
            v = V[i][j]
            if v == LOG0: continue
            if j < m and v + model.skip > V[i][j+1]: V[i][j+1] = v + model.skip; bp[(i, j+1)] = (i, j, None)
            if i < n:
                tok = ct[i]
                for k in range(0, min(kmax(tok), m-j)+1):
                    s = v + model.logp(tok, pt[j:j+k])
                    if s > V[i+1][j+k]: V[i+1][j+k] = s; bp[(i+1, j+k)] = (i, j, pt[j:j+k])
    path = []; i, j = n, m
    while (i, j) != (0, 0):
        pi, pj, u = bp[(i, j)]
        if u is None: path.append(('~', pt[pj]))
        else: path.append((ct[pi], u))
        i, j = pi, pj
    return path[::-1], V[n][m]

def main():
    data = load(); model = Model(data)
    for it in range(ITERS):
        newc = collections.defaultdict(lambda: collections.defaultdict(float)); newt = collections.defaultdict(float)
        total = 0.0
        for pid, ct, pt in data:
            Z, post = forward_backward(model, ct, pt)
            total += Z
            if post is None: continue
            for (tok, u), p in post.items(): newc[tok][u] += p; newt[tok] += p
        model.counts, model.tot = newc, newt
        if it % 5 == 0 or it == ITERS-1: print(f'iter {it} logL {total:.1f}', flush=True)
    # key table
    print('\n== key (token: unit prob count) ==')
    toks = sorted(model.tot, key=lambda t: -model.tot[t])
    for t in toks:
        d = model.counts[t]; tot = model.tot[t]
        best = sorted(d.items(), key=lambda x: -x[1])[:4]
        print(f'{t:5s} n={tot:5.1f}  ' + '  '.join(f'{(u or "-")}:{c/tot:.2f}' for u, c in best))
    import json
    dump={t:{(u or '-'):c/model.tot[t] for u,c in model.counts[t].items() if c/model.tot[t]>0.01} for t in model.tot}
    json.dump(dump,open('bethune/em_model.json','w',encoding='utf-8'),ensure_ascii=False,indent=0)
    if SHOW:
        print('\n== alignments ==')
        for pid, ct, pt in data:
            path, sc = viterbi(model, ct, pt)
            print(f'\n[{pid}] {sc:.1f}')
            print(' '.join(f'{t}={u or "-"}' for t, u in path))

if __name__ == '__main__':
    main()
