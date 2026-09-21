# R701 p.2: anneal a one-to-one substitution against each language model (spaces kept).
import sys,random,math
sys.path.insert(0,'C:/Users/dbour/cypher/.worktrees/sp106b'); from lang import lm
CT="Esg frp rohxog x rygo fa ombhpeip nb waltmg bxdos ipdlts kd kek rxiro ids pydo pnydquosdpr np oi ia xohocfog frp bhpeocfscu kssp ttmoh tt aal"
# E = epsilon-shaped sign, kept distinct from e
syms=sorted(set(CT.replace(' ','')))
for mid in ['it-modern','en-modern','es-modern','fr-modern','la']:
    m=lm.load(mid,order=4,spaces=True); A=[c for c in m.alpha if c!=' ']
    best=(-1e9,None)
    for rs in range(6):
        k={s:random.choice(A) for s in syms}
        dec=lambda k:''.join(k.get(c,c) if c!=' ' else ' ' for c in CT)
        sc=m.score(dec(k)); T=3.0
        for it in range(30000):
            s=random.choice(syms); old=k[s]; k[s]=random.choice(A)
            n=m.score(dec(k))
            if n>sc or random.random()<math.exp((n-sc)/T): sc=n
            else: k[s]=old
            T=max(0.05,T*0.9997)
        if sc>best[0]: best=(sc,dec(k))
    print(mid, round(best[0]/len(CT),3), best[1])
