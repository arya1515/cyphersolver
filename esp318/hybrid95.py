import pickle, numpy as np, math, sys, collections
from scipy.cluster.hierarchy import fcluster
from lm import ALPHA, IDX
from assign95 import CL2L
L=len(ALPHA)
JUNK={20,10,17,13,64,15,14,11,57,58,12,19,51,55,60,63,66,16,65,23,24,27,31}
d=pickle.load(open('f122r_glyphs.pkl','rb')); lab=fcluster(d['Z'],110,'maxclust'); meta=d['meta']
units=pickle.load(open('f122r_units.pkl','rb'))   # (line, x, ncc-vector) from viterbi95 (sub-split boxes)
tabs=pickle.load(open('lm_tabs.pkl','rb'))
SCALE=float(sys.argv[1]) if len(sys.argv)>1 else 14.0; BEAM=int(sys.argv[2]) if len(sys.argv)>2 else 800
# map each unit back to its glyph: units were made from meta boxes with x = m.x0 + offset; build lookup by (line, x0)
byline=collections.defaultdict(list)
for i,m in enumerate(meta): byline[m['line']].append((m['x0'],i))
def glyph_of(ln,x):
    cands=[(abs(x-x0),i) for x0,i in byline[ln] if x0<=x+2]
    return min(cands)[1] if cands else None
E=[]; kinds=[]
for ln,x,vec in units:
    gi=glyph_of(ln,x); k=int(lab[gi]) if gi is not None else -1
    if k in CL2L and k not in JUNK:
        e=np.full(L,-14.0); e[IDX[CL2L[k].lower()]]=0.0; kinds.append('F')
    else:
        v=vec.copy()
        if not (v>-1).any(): e=np.full(L,math.log(1/L)); kinds.append('G')
        else:
            v[v<0]=-0.2; z=SCALE*v; z-=z.max(); p=np.exp(z); p/=p.sum(); e=np.log(np.maximum(p,1e-6)); kinds.append('S')
    E.append(e)
print('units',len(E),collections.Counter(kinds))
beams={(): (0.0, [])}
for t,e in enumerate(E):
    nb={}
    for ctx,(sc,hist) in beams.items():
        for c in range(L):
            if e[c]<-13 and kinds[t]=='F': continue
            if len(ctx)==4: s=sc+tabs[5][ctx[0],ctx[1],ctx[2],ctx[3],c]+e[c]
            else: s=sc+e[c]+(tabs[len(ctx)+1][tuple(ctx)+(c,)] if ctx else tabs[1][c])
            nctx=(ctx+(c,))[-4:]
            if nctx not in nb or nb[nctx][0]<s: nb[nctx]=(s,hist+[c])
    beams=dict(sorted(nb.items(),key=lambda kv:-kv[1][0])[:BEAM])
best=max(beams.values(),key=lambda v:v[0]); txt=''.join(ALPHA[c] for c in best[1])
lines=sorted(set(u[0] for u in units)); out=[]; marks=[]; pos=0
for ln in lines:
    n=sum(1 for u in units if u[0]==ln); out.append(txt[pos:pos+n]); marks.append(''.join(kinds[pos:pos+n])); pos+=n
res='\n'.join('%2d %s\n   %s'%(ln+1,t,mk.replace('F',' ').replace('S','~').replace('G','?')) for ln,t,mk in zip(lines,out,marks))
open('f122r_hybrid.txt','w').write(res); print('score',round(best[0],1)); print(res)
