import math, collections, re, sys
from syl_em import load_cols, plain
def align(T,L,P,Kc=3,Kw=14,gap=-7.0):
    n,m=len(T),len(L);INF=-1e18
    D=[[INF]*(m+1) for _ in range(n+1)];B=[[None]*(m+1) for _ in range(n+1)];D[0][0]=0
    for i in range(n+1):
        Ti=T[i-1] if i else None
        K=Kw if (Ti and Ti.startswith('-/[')) else Kc
        for j in range(m+1):
            if i==0 and j==0: continue
            best,bb=INF,None
            if i:
                for k in range(1,min(K,j)+1):
                    s=L[j-k:j]
                    v=D[i-1][j-k]+P.get((Ti,s),-5.0-0.8*k if K==Kc else -6.0-0.5*k)
                    if v>best: best,bb=v,k
                v=D[i-1][j]+gap
                if v>best: best,bb=v,-1
            if j:
                v=D[i][j-1]+gap
                if v>best: best,bb=v,-2
            D[i][j],B[i][j]=best,bb
    i,j=n,m;al=[]
    while i or j:
        b=B[i][j]
        if b>0: al.append((T[i-1],L[j-b:j]));i-=1;j-=b
        elif b==-1: al.append((T[i-1],None));i-=1
        else: al.append((None,L[j-1]));j-=1
    return D[n][m],al[::-1]
def reest(al,seed):
    C=collections.Counter((t,s) for t,s in al if t and s)
    for k,v in seed.items(): C[(k,v)]+=3
    tot=collections.Counter()
    for (t,s),c in C.items(): tot[t]+=c
    return {(t,s):math.log((c+0.05)/(tot[t]+0.5)) for (t,s),c in C.items()},C
if __name__=='__main__':
    crib=open('crib1519.md',encoding='utf8').read()
    L=plain(crib.split('## 7c')[1].split('## 8c')[0].split('\n',1)[1])
    T=[t for t in load_cols('t1133_full.txt','R1133')]
    T=[t for t in T if '#' not in t.split('/')[0] or True]
    seed={'-/[d]':'de','-/[s]':'vostra','-/[&]':'maesta'}
    P={(k,v):-0.1 for k,v in seed.items()}
    for it in range(12):
        sc,al=align(T,L,P);P,C=reest(al,seed)
        key=collections.defaultdict(collections.Counter)
        for (t,s),c in C.items(): key[t][s]+=c
        n=sum(C.values());pure=sum(max(c.values()) for c in key.values())/n
        print(it,round(sc),n,round(pure,3),flush=True)
    import json
    json.dump({t:dict(c) for t,c in key.items()},open('key1519_counts.json','w'),ensure_ascii=False,indent=0)
    for t,c in sorted(key.items(),key=lambda x:-sum(x[1].values()))[:60]: print(t,dict(c.most_common(4)))
    print(' '.join(f"{t or '-'}={s or '_'}" for t,s in al[:200]))
