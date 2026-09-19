import json,math,random
A='abcdefghijklmnopqrstuvwxyz'
def prep(q):
    import numpy as np
    arr=np.full(26**4,min(q.values())-1.0)
    for k,v in q.items():
        if len(k)==4 and all(c in A for c in k):
            arr[((ord(k[0])-97)*26+ord(k[1])-97)*26*26+(ord(k[2])-97)*26+ord(k[3])-97]=v
    return arr
def solve(sym,arr,restarts=10,iters=30000,fix=None):
    import numpy as np
    syms=sorted(set(sym)); idx={s:i for i,s in enumerate(syms)}
    S=np.array([idx[s] for s in sym])
    def score(m):
        L=m[S]; c=((L[:-3]*26+L[1:-2])*26+L[2:-1])*26+L[3:]
        return arr[c].sum()
    uf='etaoinshrdlcumwfgypbvkjxqz'
    best=(-1e18,None)
    for r in range(restarts):
        # init by frequency
        from collections import Counter
        cnt=Counter(sym); order=[s for s,_ in cnt.most_common()]
        m=np.zeros(len(syms),int)
        for j,s in enumerate(order): m[idx[s]]=ord(uf[j%26])-97 if r==0 else random.randrange(26)
        if fix:
            for s,l in fix.items(): m[idx[s]]=ord(l)-97
        sc=score(m); T=2.0
        for it in range(iters):
            i=random.randrange(len(syms))
            if fix and syms[i] in fix: continue
            if random.random()<0.5:
                j=random.randrange(len(syms)); 
                if fix and syms[j] in fix: continue
                m[i],m[j]=m[j],m[i]; ns=score(m)
                if ns>=sc or random.random()<math.exp((ns-sc)/T): sc=ns
                else: m[i],m[j]=m[j],m[i]
            else:
                old=m[i]; m[i]=random.randrange(26)
                ns=score(m)
                if ns>=sc or random.random()<math.exp((ns-sc)/T): sc=ns
                else: m[i]=old
            T=max(0.05,6.0*(1-it/iters))
        if sc>best[0]: best=(sc,m.copy())
    m=best[1]; return best[0]/len(sym),{s:A[m[idx[s]]] for s in syms}
