import json,math,random,numpy as np,re,glob,collections
A='abcdefghijklmnopqrstuvwxyz'
def unif(lang):
    q=json.load(open(f'q_{lang}.json'))
    c=collections.Counter()
    for k,v in q.items(): c[k[0]]+=10**v
    t=sum(c.values()); return np.array([max(c[a]/t,1e-4) for a in A])
def solve(sym,arr,uni,restarts=6,iters=60000,lam=1.0,fix=None):
    syms=sorted(set(sym)); idx={s:i for i,s in enumerate(syms)}
    S=np.array([idx[s] for s in sym]); n=len(S)
    cnt=np.bincount(S,minlength=len(syms))
    lu=np.log(uni)
    def score(m):
        L=m[S]; qs=arr[((L[:-3]*26+L[1:-2])*26+L[2:-1])*26+L[3:]].sum()
        f=np.bincount(m,weights=cnt,minlength=26)/n+1e-4
        kl=(f*np.log(f/uni)).sum()
        return qs - lam*n*kl
    best=(-1e18,None)
    for r in range(restarts):
        m=np.array([random.randrange(26) for _ in syms])
        if fix:
            for k,v in fix.items(): m[idx[k]]=ord(v)-97
        sc=score(m)
        for it in range(iters):
            T=max(0.05,6.0*(1-it/iters))
            i=random.randrange(len(syms))
            if fix and syms[i] in fix: continue
            if random.random()<0.5:
                j=random.randrange(len(syms))
                if fix and syms[j] in fix: continue
                m[i],m[j]=m[j],m[i]; ns=score(m)
                if ns>=sc or random.random()<math.exp((ns-sc)/T): sc=ns
                else: m[i],m[j]=m[j],m[i]
            else:
                old=m[i]; m[i]=random.randrange(26); ns=score(m)
                if ns>=sc or random.random()<math.exp((ns-sc)/T): sc=ns
                else: m[i]=old
        if sc>best[0]: best=(sc,m.copy())
    m=best[1]; return best[0]/n,{s:A[m[idx[s]]] for s in syms}
if __name__=='__main__':
    import hc2
    t=re.sub('[^a-z]','',open('../beale/lmcorpus/pg1342.txt',encoding='utf8').read().lower())[80000:80430]
    # homophonic synthetic: split e,t,a,o,i,n into 2 symbols each
    sym=[c+str(random.randrange(2)) if c in 'etaoin' else c for c in t]
    arr=hc2.prep(json.load(open('q_en.json')))
    sc,m=solve(sym,arr,unif('en'),restarts=4)
    print(sc,''.join(m[x] for x in sym)[:150]); print(t[:150])
