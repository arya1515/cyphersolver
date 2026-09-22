import re, math, collections, json, sys
raw=[];GS=[]
for ln in open('desmarets1710/transcription.txt',encoding='utf-8'):
    if ln.startswith('G |'): raw.append(ln[3:])
    elif ln.startswith('C |'): GS.append(ln[3:].split())
def prep(l):
    l=l.lower().replace('(ent)','ent').replace('(ens)','ens').replace('(ue)','ue').replace("'"," ")
    ws=re.sub(r'[^a-z ]','',l).split();t='';B={0}
    for w in ws: t+=w;B.add(len(t))
    return t,B
L=[(prep(r),g) for r,g in zip(raw,GS)]
MAXL=12
lp=lambda l: math.log(0.03) if l==0 else -abs(l-4)*0.45
P=collections.defaultdict(collections.Counter)
for it in range(60):
    C=collections.defaultdict(collections.Counter);ll=0
    for (t,B),gs in L:
        n,m=len(t),len(gs)
        def e(k,i,j):
            d=P[gs[k]];tot=sum(d.values())
            w=math.exp(lp(j-i)+(0 if i in B else -1.2)+(0 if j in B else -1.2))
            return w*((d[t[i:j]]+0.1)/(tot+1) if it else 1)
        E={(k,i,j):e(k,i,j) for k in range(m) for i in range(n+1) for j in range(i,min(n,i+MAXL)+1)}
        F=[[0]*(n+1) for _ in range(m+1)];F[0][0]=1
        for k in range(m):
            for i in range(n+1):
                if F[k][i]:
                    for j in range(i,min(n,i+MAXL)+1):F[k+1][j]+=F[k][i]*E[k,i,j]
        Bk=[[0]*(n+1) for _ in range(m+1)];Bk[m][n]=1
        for k in range(m-1,-1,-1):
            for i in range(n+1):
                Bk[k][i]=sum(E[k,i,j]*Bk[k+1][j] for j in range(i,min(n,i+MAXL)+1))
        Z=F[m][n];ll+=math.log(Z)
        for (k,i,j),v in E.items():
            p=F[k][i]*v*Bk[k+1][j]/Z
            if p>1e-4:C[gs[k]][t[i:j]]+=p
    P=C
    if it%10==9: print(it,ll)
# viterbi
out=[]
for (t,B),gs in L:
    n,m=len(t),len(gs);V=[[(-1e18,0)]*(n+1) for _ in range(m+1)];V[0][0]=(0,0)
    for k in range(m):
        d=P[gs[k]];tot=sum(d.values())
        for i in range(n+1):
            if V[k][i][0]>-1e17:
                for j in range(i,min(n,i+MAXL)+1):
                    s=V[k][i][0]+math.log((d[t[i:j]]+0.1)/(tot+1))+lp(j-i)+(0 if i in B else -1.2)+(0 if j in B else -1.2)
                    if s>V[k+1][j][0]:V[k+1][j]=(s,i)
    seg=[];j=n
    for k in range(m,0,-1):
        i=V[k][j][1];seg.append(t[i:j]);j=i
    out.append(list(zip(gs,seg[::-1])))
for o in out: print(' '.join(f'{g}={s}' for g,s in o))
K=collections.defaultdict(collections.Counter)
for o in out:
    for g,s in o:K[g][s]+=1
json.dump({g:dict(c) for g,c in K.items()},open('desmarets1710/key_em3.json','w'),sort_keys=True)
