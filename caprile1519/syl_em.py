"""Variable-length monotone EM: each cipher column emits 1..K plaintext letters (syllabic hypothesis)."""
import math, collections, re, sys, random
def load_cols(path, src):
    toks=[]
    for l in open(path,encoding='utf8'):
        if l.startswith(src+' '):
            toks+= [t.rstrip('?') for t in l.split(':',1)[1].split() if t.startswith('#') is False]
    return toks
def plain(s): return re.sub(r'[^a-z]','',s.lower().replace('j','i').replace('v','u'))
def align(T,L,P,K=3,gapT=-6.0,gapL=-6.0,deflen={1:-4.0,2:-4.5,3:-6.0}):
    n,m=len(T),len(L);INF=-1e18
    D=[[INF]*(m+1) for _ in range(n+1)];B=[[None]*(m+1) for _ in range(n+1)];D[0][0]=0
    for i in range(n+1):
        for j in range(m+1):
            if i==0 and j==0: continue
            best,bb=INF,None
            if i:
                for k in range(1,K+1):
                    if j>=k:
                        s=L[j-k:j];v=D[i-1][j-k]+P.get((T[i-1],s),deflen[k])
                        if v>best: best,bb=v,('d',k)
                v=D[i-1][j]+gapT
                if v>best: best,bb=v,('t',0)
            if j:
                v=D[i][j-1]+gapL
                if v>best: best,bb=v,('l',0)
            D[i][j],B[i][j]=best,bb
    i,j=n,m;al=[]
    while i or j:
        b,k=B[i][j]
        if b=='d': al.append((T[i-1],L[j-k:j]));i-=1;j-=k
        elif b=='t': al.append((T[i-1],None));i-=1
        else: al.append((None,L[j-1]));j-=1
    return D[n][m],al[::-1]
def reest(al):
    C=collections.Counter((t,s) for t,s in al if t and s);tot=collections.Counter()
    for (t,s),c in C.items(): tot[t]+=c
    return {(t,s):math.log((c+0.1)/(tot[t]+1.0)) for (t,s),c in C.items()},C
def run(T,L,iters=15,**kw):
    P={}
    for it in range(iters):
        sc,al=align(T,L,P,**kw);P,C=reest(al)
        key=collections.defaultdict(collections.Counter)
        for (t,s),c in C.items(): key[t][s]+=c
        n=sum(C.values());pure=sum(max(c.values()) for c in key.values())/max(n,1)
        print(it,round(sc),n,round(pure,3),flush=True)
    return al,key
