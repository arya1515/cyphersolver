"""Apply the tuned iterated local search to the fr. 3621 no. 97 transcription."""
import sys, time, argparse
sys.argv=['x']
exec(open('solve97b.py').read().split("if __name__")[0])
from search import ils

ap=argparse.ArgumentParser()
import sys as _s
args=_s.argv
merge = '--merge' in args
seeds = range(1,25)
P=Problem(merge=merge)
print(f'merge={merge}  segments={len(P.segs)} chars={P.nf} symbols={P.ns}', flush=True)
best=-9e9; bestk=None; bestmu=None
for mu in (0.0,1.0,2.0,3.0):
    for sd in seeds:
        b,k=ils(P,State,NA,iters=200,kick=4,mu=mu,seed=sd,FREQ=FREQ)
        raw,_=P.full(k)
        if raw>best:
            best=raw; bestk=list(k); bestmu=(mu,sd)
            print(f'  mu={mu} seed={sd}  raw {raw:.4f}', flush=True)
print(f'\nBEST raw {best:.4f}  (real French approx -1.93; control true keys approx -1.63)')
print(f'from mu={bestmu[0]} seed={bestmu[1]}\n')
print('KEY')
for s in P.syms: print(f'  {s} -> {AL[bestk[P.idx[s]]]}')
print()
print(decode(P,bestk,merge=merge))
