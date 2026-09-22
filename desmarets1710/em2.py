import re, math, collections, json, sys
sys.path.insert(0,'desmarets1710'); from em import load, norm
G,U=load()
# keep word boundaries: text with '|' at word starts
def toks(line):
    line=line.replace("'"," ")
    return re.sub(r'[^a-z ]','',line.lower().replace('(ent)','ent').replace('(ens)','ens').replace('(ue)','ue')).split()
raw=[]
for ln in open('desmarets1710/transcription.txt',encoding='utf-8'):
    if ln.startswith('G |'): raw.append(ln[3:])
T=[];B=set()
for l in raw:
    for w in toks(l):
        B.add(len(T)); T.extend(w)
B.add(len(T)); text=''.join(T)
gs=[g for _,x in G for g in x]
n,m=len(text),len(gs); print(n,m,n/m)
MAXL=12
lenp=lambda L: math.log(0.02) if L==0 else -abs(L-4.5)*0.5
bon=lambda i,j: (0 if i in B else -1.5)+(0 if j in B else -1.5)
P=collections.defaultdict(collections.Counter)
for it in range(15):
    V=[[-1e18]*(n+1) for _ in range(m+1)];bp=[[0]*(n+1) for _ in range(m+1)];V[0][0]=0
    for k in range(m):
        d=P[gs[k]];tot=sum(d.values())
        lo=max(0,int(k*n/m)-80);hi=min(n,int(k*n/m)+80)
        for i in range(lo,hi+1):
            v=V[k][i]
            if v<-1e17: continue
            for j in range(i,min(n,i+MAXL)+1):
                s=text[i:j]
                em=math.log((d[s]+0.05)/(tot+1)) if tot else 0
                sc=v+em+lenp(j-i)+bon(i,j)
                if sc>V[k+1][j]: V[k+1][j]=sc;bp[k+1][j]=i
    seg=[];j=n
    for k in range(m,0,-1):
        i=bp[k][j];seg.append(text[i:j]);j=i
    seg=seg[::-1]
    P=collections.defaultdict(collections.Counter)
    for g,s in zip(gs,seg): P[g][s]+=1
    cons=sum(max(c.values()) for c in P.values())
    print(it,cons,V[m][n])
out=' '.join(f'{g}={s}' for g,s in zip(gs,seg));print(out)
json.dump({g:dict(c) for g,c in P.items()},open('desmarets1710/key_em2.json','w'),sort_keys=True)
