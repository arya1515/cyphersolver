import pickle, numpy as np, math, sys
from lm import ALPHA, IDX
L=len(ALPHA)
tabs=pickle.load(open('lm_tabs.pkl','rb')); lp5=tabs[5]
units=pickle.load(open(sys.argv[1] if len(sys.argv)>1 else 'f122r_units.pkl','rb'))
SCALE=float(sys.argv[2]) if len(sys.argv)>2 else 9.0; BEAM=int(sys.argv[3]) if len(sys.argv)>3 else 1500
lines=sorted(set(u[0] for u in units))
def em(vec):
    v=vec.copy(); has=(v>-1).any()
    if not has: return np.full(L,math.log(1.0/L))
    v[v<0]=-0.2                      # letters with no template: weak floor
    z=SCALE*v; z=z-z.max(); p=np.exp(z); p/=p.sum()
    return np.log(np.maximum(p,1e-6))
seq=[u for u in units]   # continuous across lines (scriptio continua)
E=[em(u[2]) for u in seq]
# beam over full sequence; state = last 4 letters
beams={(): (0.0, [])}
for t,e in enumerate(E):
    nb={}
    for ctx,(sc,hist) in beams.items():
        for c in range(L):
            if len(ctx)==4: s=sc+lp5[ctx[0],ctx[1],ctx[2],ctx[3],c]+e[c]
            else: s=sc+e[c]+(tabs[len(ctx)+1][tuple(ctx)+(c,)] if len(ctx)>0 else tabs[1][c])
            nctx=(ctx+(c,))[-4:]
            if nctx not in nb or nb[nctx][0]<s: nb[nctx]=(s,hist+[c])
    beams=dict(sorted(nb.items(),key=lambda kv:-kv[1][0])[:BEAM])
best=max(beams.values(),key=lambda v:v[0])
txt=''.join(ALPHA[c] for c in best[1])
out=[];pos=0
for ln in lines:
    n=sum(1 for u in seq if u[0]==ln); out.append(txt[pos:pos+n]); pos+=n
res='\n'.join('%2d %s'%(ln+1,t) for ln,t in zip(lines,out))
open('f122r_beam.txt','w').write(res); print('score',round(best[0],1)); print(res)
