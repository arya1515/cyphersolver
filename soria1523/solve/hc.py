import sys, re, random, math
sys.path.insert(0,'solve'); import lm
M,FL=lm.load()
CODES=set('lod lih lib luc lim leh cap dus mos rip rap sag saq sig qed cip mul {pur} qur pur'.split())
def load_words(files):
    W=[]
    for fn in files:
        for l in open(fn,encoding='utf-8'):
            if not re.match(r'\s*L\d+:',l): continue
            for w in l.split(':',1)[1].split():
                if w in CODES or w in('|','...') : W.append(None); continue
                w=w.replace('?','')
                if w: W.append(w)
    return W
def score(W,key):
    s=0.0
    for w in W:
        if w is None: continue
        t=' '+''.join(key[c] for c in w)+' '
        for i in range(len(t)-3): s+=M.get(t[i:i+4],FL)
    return s
LET='abcdefghijlmnopqrstuvxyz'
FREQ='eaosnrildtcumpbgvyqhfzjx'
def solve(W,iters=40000,fixed={},seed=0):
    random.seed(seed)
    syms=sorted({c for w in W if w for c in w})
    key={c:random.choice(FREQ[:12]) for c in syms}; key.update(fixed)
    cur=score(W,key); best=(cur,dict(key)); T=30.0
    free=[c for c in syms if c not in fixed]
    for it in range(iters):
        c=random.choice(free); old=key[c]; key[c]=random.choice(LET)
        s=score(W,key)
        if s>cur or random.random()<math.exp((s-cur)/T): cur=s
        else: key[c]=old
        if cur>best[0]: best=(cur,dict(key))
        T=max(0.5,T*0.9997)
    return best
if __name__=='__main__':
    W=load_words(sys.argv[1:])
    res=[]
    for sd in range(8):
        b=solve(W,iters=25000,fixed={'f':'y'},seed=sd); res.append(b); print(sd,round(b[0]),''.join(f'{c}{b[1][c]} ' for c in sorted(b[1])),flush=True)
    b=max(res,key=lambda x:x[0]); key=b[1]
    print(' '.join('|' if w is None else ''.join(key[c] for c in w) for w in W))
