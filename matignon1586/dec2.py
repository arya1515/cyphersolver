import json, sys, math, pickle
from solve import segment
D=pickle.load(open('lm.pkl','rb')); CNT=D['cnt']; N=D['N']; AL='abcdefghilmnopqrstuxyz'
LAM=0.4
def clogp(ctx,ch):
    tot=0.0;w=1.0
    for n in range(N,1,-1):
        c=ctx[-(n-1):]
        if len(c)<n-1: continue
        den=CNT[n-1][c]
        if den<2: continue
        tot+=w*LAM*(CNT[n][c+ch]/den); w*=(1-LAM)
        if w<1e-6: break
    tot+=w*(CNT[1][ch]+1)/(sum(CNT[1].values())+22)
    return math.log(max(tot,1e-12))
key=json.load(open('key_exp.json'))
def beam(toks,width=500):
    B=[('',0.0)]
    for t in toks:
        opts=key.get(t,[[c,0.0] for c in AL])
        nb=[]
        for txt,sc in B:
            for o,pen in opts:
                s=sc-pen; c=txt
                for ch in o:
                    if ch.isalpha(): s+=clogp(c[-(N-1):],ch)
                    c+=ch
                nb.append((c,s))
        nb.sort(key=lambda x:-x[1])
        seen=set();out=[]
        for txt,sc in nb:
            k=txt[-(N-1):]
            if k in seen: continue
            seen.add(k); out.append((txt,sc))
            if len(out)>=width: break
        B=out
    return B[0][0]
if __name__=='__main__':
    for i,l in enumerate(open(sys.argv[1],encoding='utf-8'),1):
        l=l.strip()
        if l: print(i, segment(beam(l.split())))
