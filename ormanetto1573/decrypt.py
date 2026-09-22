"""R116 with Meister VI.1 key (key1.py). Beam search, LM-scored."""
import sys,os
sys.path.insert(0,'..')
from lang import lm
from tok import load
from key1 import L,V1,NULLS,N
LANG=os.environ.get('LANG_M','es-golden-age'); FIVE=os.environ.get('FIVE','6')
M=lm.load(LANG,spaces=False); A,K=M.A,M.order; IDX=M.index; LP=M.lp.reshape(-1,A); MOD=A**(K-1)
def enc(s): return [IDX[c] for c in lm.norm(s,'early',False) if c in IDX]
def step(ctx,ch):
    s=0.0
    for x in ch: s+=float(LP[ctx,x]); ctx=(ctx*A+x)%MOD
    return ctx,s
def items(p):
    out=[]
    for d,dot,u in p:
        if d=='1' and not dot and out and out[-1][0] in '24568' and not out[-1][2]:
            x=out[-1]; nd=x[0]
            if nd=='5': nd=FIVE
            out[-1]=(nd,x[1],True); continue
        out.append((d,dot,False))
    return out
def moves(it,p):
    d,dot,mk=it[p]; r=[]
    if not dot and not mk and d in NULLS: r.append((1,'',-2.0))
    if dot and not mk and d in V1: r.append((1,V1[d],-0.3))
    if p+1<len(it):
        e,dot2,mk2=it[p+1]
        if not mk:
            code=d+e
            if not dot and not dot2 and not mk2 and code in L: r.append((2,L[code],0.0))
            if code in L and d=='0' and dot and not mk2 and not dot2: r.append((2,L[code],-0.5))
            key=('.' if dot else '')+code+('.' if dot2 else '')+('+' if mk2 else '')
            if key in N and not (dot and dot2): r.append((2,'['+N[key]+']',0.5))
    if not r: r.append((1,'{%s%s%s}'%(d,'.' if dot else '','+' if mk else ''),-6.0))
    return r
def decode(it,beam=400):
    n=len(it); st=[dict() for _ in range(n+1)]; st[0][0]=(0.0,None)
    for p in range(n):
        for ctx,(sc,_) in sorted(st[p].items(),key=lambda kv:-kv[1][0])[:beam]:
            for ln,txt,pen in moves(it,p):
                t=txt[1:-1] if txt.startswith('[') else ('' if txt.startswith('{') else txt)
                nc,s=step(ctx,enc(t)); v=sc+s+pen
                o=st[p+ln].get(nc)
                if o is None or v>o[0]: st[p+ln][nc]=(v,(p,ctx,txt))
    ctx=max(st[n],key=lambda c:st[n][c][0]); q=n; out=[]; tot=st[n][ctx][0]
    while st[q][ctx][1]:
        p,pc,txt=st[q][ctx][1]; out.append(txt); q,ctx=p,pc
    return ' '.join(reversed(out)).replace('  ',' '),tot/n
for p in load():
    if not p: continue
    s,sc=decode(items(p)); print(round(sc,3)); print(s); print()
