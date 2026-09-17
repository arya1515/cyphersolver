"""Controls for solve.py: (1) blind run, no pinned letters; (2) pinned run on shuffled token order (same symbols, same
frequencies) to show the language-model score of the real order is not reachable on a random one."""
import random, solve
lines=solve.load()
print('tokens',sum(len(t) for _,t in lines))
best_real=None
for sd in range(3):
    sc,m=solve.anneal(lines,solve.PIN,sd,iters=40000); best_real=max(best_real or sc,sc); print('pinned real',sd,round(sc,1),flush=True)
for sd in range(3):
    sc,m=solve.anneal(lines,{},sd,iters=40000)
    agree=sum(1 for k,v in solve.PIN.items() if m.get(k)==v); print('blind',sd,round(sc,1),'pinned letters recovered',agree,'/',len(solve.PIN),flush=True)
toks=[t for _,tk in lines for t in tk]
for sd in range(3):
    r=random.Random(100+sd); sh=toks[:]; r.shuffle(sh)
    sl=[('shuf',sh)]
    sc,m=solve.anneal(sl,solve.PIN,sd,iters=40000); print('pinned shuffled',sd,round(sc,1),flush=True)
