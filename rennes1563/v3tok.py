import sys
from v3lat_vals import A
from lattice import decode
for i,ln in enumerate(open('c390_p139_v3.txt',encoding='utf-8')):
    if ln.startswith('#') or not ln.strip(): continue
    toks=ln.split(); c=[A.get(t,'?').split('|') for t in toks]
    # beam with alignment: decode per token and track choices
    B=[(0.0,'',[])]
    from lattice import M
    for opts in c:
        nb={}
        for sc,s,ch in B:
            for o in opts:
                o='' if o in('-','?') else o
                t=s+o
                add=(M.score(t[-(M.order-1+len(o)):])-M.score(t[-(M.order-1+len(o)):len(t)-len(o)])) if o else -0.3
                key=(t,)
                if key not in nb or nb[key][0]<sc+add: nb[key]=(sc+add,t,ch+[o or '·'])
        B=sorted(nb.values(),reverse=True)[:3000]
    best=B[0]
    print(' '.join(f'{a}={b}' for a,b in zip(toks,best[2])))
    print('  ->',best[1])
