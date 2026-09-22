import sys,os,random,math,numpy as np
sys.path.insert(0,'..')
from lang import lm
from tok import load
LANG=os.environ.get('LANG_M','it-cinquecento'); ORD=int(os.environ.get('ORD','4'))
M=lm.load(LANG,order=ORD,spaces=False); A,K=M.A,M.order; IDX=M.index; LP=M.lp.reshape(-1,A); MOD=A**(K-1)
DIG=os.environ.get('DIGS','123456789')
LET=list(os.environ.get('LET','utimfgalosendrbcpz'))
# sequences of digits; dotted digits and undotted 0 are dropped (codes/nulls), breaking nothing
seqs=[]
from pool import pooled
for p in [[(d,False,False) for d in s] for s in pooled()]:
    if not p: continue
    s=[int(d) for d,dot,u in p if not dot and d in DIG]
    seqs.append(s)
LI=[IDX[c] for c in LET]
def viterbi(assign,beam=int(os.environ.get('BEAM','60')),ret=False):
    tot=0;outs=[]
    for s in seqs:
        st={0:(0.0,'')}
        for d in s:
            ns={}
            for ctx,(sc,txt) in st.items():
                for x in assign[d]:
                    v=sc+LP[ctx,x]; c=(ctx*A+x)%MOD
                    if c not in ns or v>ns[c][0]: ns[c]=(v,txt+M.alpha[x] if ret else '')
            st=dict(sorted(ns.items(),key=lambda kv:-kv[1][0])[:beam])
        b=max(st.values(),key=lambda v:v[0]); tot+=b[0]; outs.append(b[1])
    return (tot,outs) if ret else tot
rnd=random.Random(int(sys.argv[1]) if len(sys.argv)>1 else 0)
N=sum(len(s) for s in seqs)
def mk(perm): return {int(DIG[i]):(perm[2*i],perm[2*i+1]) for i in range(len(DIG))}
best=None
for r in range(int(sys.argv[2]) if len(sys.argv)>2 else 3):
    perm=LI[:]; rnd.shuffle(perm); cur=viterbi(mk(perm)); T=30.0
    for it in range(int(os.environ.get('NIT','1500'))):
        a,b=rnd.sample(range(2*len(DIG)),2)
        if a//2==b//2: continue
        perm[a],perm[b]=perm[b],perm[a]; v=viterbi(mk(perm))
        if v>cur or rnd.random()<math.exp((v-cur)/T): cur=v
        else: perm[a],perm[b]=perm[b],perm[a]
        T=max(0.5,T*0.997)
    k=mk(perm); print(r,round(cur/N,3),{d:M.alpha[a]+M.alpha[b] for d,(a,b) in k.items()},flush=True)
    if best is None or cur>best[0]: best=(cur,perm[:])
sc,outs=viterbi(mk(best[1]),ret=True)
for o in outs: print(o[:400])
