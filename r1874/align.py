# hard-EM monotone alignment of cipher groups to known decipherment (adapted from balbases1677/align2.py)
import math,collections,json,sys
from seg import seq
t=[u for pg,u in seq if pg in ('8953.png','8954.png') and u.isdigit()]
P=open('tx/para6-7.txt').read().split()
p6=''.join(P[:P.index('continuo')]); p7=''.join(P[P.index('continuo'):])
T6=t[2:388]; A=[i for i in range(len(T6)) if T6[i:i+3]==['672','2133','6210']]
import re
B=[m.start() for m in re.finditer('contediolivares',p6)]
cuts_t=[0];cuts_p=[0]
for a,b in zip(A,B): cuts_t+=[a,a+7]; cuts_p+=[b,b+15]
cuts_t.append(len(T6)); cuts_p.append(len(p6))
data=[(T6[cuts_t[i]:cuts_t[i+1]],p6[cuts_p[i]:cuts_p[i+1]]) for i in range(len(cuts_t)-1)]+[(t[390:635],p7)]
print([(len(a),len(b)) for a,b in data])
LP={0:.25,1:.3,2:.25,3:.12,4:.05,5:.02,6:.01}
MAXL=6; SKIP=9.0
cnt=collections.defaultdict(collections.Counter)
def cost(tok,sub):
    c=cnt[tok];n=sum(c.values())
    return -math.log((c[sub]+0.5*LP[len(sub)]*(1/20)**len(sub))/(n+0.5))
def align(t,s):
    I,J=len(t),len(s);INF=1e18
    D=[[INF]*(J+1) for _ in range(I+1)];B=[[None]*(J+1) for _ in range(I+1)];D[0][0]=0
    band=max(25,int(0.2*J))
    for i in range(I+1):
        c=i*J/I
        for j in range(max(0,int(c-band)),min(J,int(c+band))+1):
            d=D[i][j]
            if d>=INF: continue
            if j<J and d+SKIP<D[i][j+1]: D[i][j+1]=d+SKIP;B[i][j+1]=(i,j,None)
            if i<I:
                for L in range(0,min(MAXL,J-j)+1):
                    sub=s[j:j+L]; v=d+cost(t[i],sub)
                    if v<D[i+1][j+L]: D[i+1][j+L]=v;B[i+1][j+L]=(i,j,sub)
    i,j=I,J;path=[]
    while (i,j)!=(0,0):
        pi,pj,sub=B[i][j]
        if sub is not None: path.append((t[pi],sub))
        i,j=pi,pj
    return D[I][J],path[::-1]
for it in range(12):
    new=collections.defaultdict(collections.Counter);tot=0;paths=[]
    for tk,s in data:
        c,p=align(tk,s);tot+=c;paths.append(p)
        for a,b in p: new[a][b]+=1
    cnt=new
    cons=sum(max(v.values()) for v in cnt.values())/sum(sum(v.values()) for v in cnt.values())
    print(it,round(tot),round(cons,3),flush=True)
json.dump({k:dict(v) for k,v in cnt.items()},open('align_counts.json','w'),indent=0)
for p in paths: print(' '.join(f'{a}={b}' for a,b in p[:80]))
