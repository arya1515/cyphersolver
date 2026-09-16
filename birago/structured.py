# Structured-homophony hypotheses: collapse two-digit symbols to a letter class by a rule, then anneal the (near-)monoalphabetic problem.
import json,sys,collections,seg,numpy as np
P=json.load(open('pairings.json'))
rules={}
for M in range(19,34): rules[f'mod{M}']=lambda p,M=M: int(p)%M
rules['units+tenshalf']=lambda p:(int(p[1]),int(p[0])>=5)
rules['units+tensparity']=lambda p:(int(p[1]),int(p[0])%2)
rules['tens+unitshalf']=lambda p:(int(p[0]),int(p[1])>=5)
rules['tens+unitsparity']=lambda p:(int(p[0]),int(p[1])%2)
rules['digitsum']=lambda p:int(p[0])+int(p[1])
rules['digitsum_mod10+order']=lambda p:((int(p[0])+int(p[1]))%10,int(p[0])>int(p[1]))
rules['absdiff+half']=lambda p:(abs(int(p[0])-int(p[1])),int(p[0])>=5)
rules['none']=lambda p:p
pidx=int(sys.argv[1]) if len(sys.argv)>1 else 0
base=[t if t!='|' else '#|' for t in P[pidx]]
out=[]
for name,f in rules.items():
    toks=[t if t[0]=='#' else 'c'+str(f(t)) for t in base]
    nd=len(set(t for t in toks if t[0]!='#'))
    r=seg.solve(toks,restarts=4,iters=80000)
    out.append((r[0],name,nd,r[1])); print(f'{r[0]:.3f} {name:22s} classes={nd} {r[1][:120]}',flush=True)
out.sort(reverse=True); print('BEST',out[0][:3]); print(out[0][3])
