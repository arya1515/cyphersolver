import re, math, collections, json
raw=[];GS=[]
for ln in open('desmarets1710/transcription.txt',encoding='utf-8'):
    if ln.startswith('G |'): raw.append(ln[3:])
    elif ln.startswith('C |'): GS.append(ln[3:].split())
def ws(l):
    l=l.lower().replace('(ent)','ent').replace('(ens)','ens').replace('(ue)','ue').replace("'","' ")
    return re.sub(r"[^a-z' ]",'',l).split()
L=[(ws(r),g) for r,g in zip(raw,GS)]
MX=2
P=collections.defaultdict(collections.Counter)
for it in range(80):
    C=collections.defaultdict(collections.Counter)
    for t,gs in L:
        n,m=len(t),len(gs)
        def e(k,i,j):
            d=P[gs[k]];tot=sum(d.values());pri=[0.25,1,0.15][j-i]
            return pri*((d[' '.join(t[i:j])]+0.02)/(tot+0.5) if it else 1)
        F=[[0]*(n+1) for _ in range(m+1)];F[0][0]=1
        for k in range(m):
            for i in range(n+1):
                for j in range(i,min(n,i+MX)+1):F[k+1][j]+=F[k][i]*e(k,i,j)
        B=[[0]*(n+1) for _ in range(m+1)];B[m][n]=1
        for k in range(m-1,-1,-1):
            for i in range(n+1):B[k][i]=sum(e(k,i,j)*B[k+1][j] for j in range(i,min(n,i+MX)+1))
        Z=F[m][n]
        if Z==0: continue
        for k in range(m):
            for i in range(n+1):
                for j in range(i,min(n,i+MX)+1):
                    p=F[k][i]*e(k,i,j)*B[k+1][j]/Z
                    if p>1e-4:C[gs[k]][' '.join(t[i:j])]+=p
    P=C
for g,d in sorted(P.items(),key=lambda x:-sum(x[1].values())):
    top=d.most_common(3); print(g, round(sum(d.values()),1), [(k,round(v,1)) for k,v in top])
