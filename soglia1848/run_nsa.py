import sys,numpy as np,time,json
sys.argv=[sys.argv[0]]+sys.argv[1:]
from nsa import *
seed=int(sys.argv[1]); iters=int(sys.argv[2]); R=int(sys.argv[3])
U=load_units('ct2.txt')
types=sorted(set(u for u in U if u!='_'))
ti={t:i for i,t in enumerate(types)}
seq=np.array([-1 if u=='_' else ti[u] for u in U],dtype=np.int64)
allowed=np.array([i for i in range(1,27) if chr(96+i) not in 'jkwxy'],dtype=np.int64)
fixed=np.zeros(len(types),dtype=np.bool_)
res=[]
rng=np.random.default_rng(seed)
for r in range(R):
    m=rng.choice(allowed,len(types)).astype(np.int64)
    t=time.time()
    b,bm=anneal(seq,m,LP,fixed,iters,15.0,0.3,seed*1000+r,allowed)
    # polish at low T
    b,bm=anneal(seq,bm.copy(),LP,fixed,iters//4,0.5,0.05,seed*1000+r+500,allowed)
    res.append((b,bm))
    print(f'{r} {b:.1f} {time.time()-t:.0f}s', show(seq,bm,types)[:160],flush=True)
b,bm=max(res,key=lambda x:x[0])
json.dump({'score':b,'key':{t:chr(96+int(bm[i])) for i,t in enumerate(types)},'text':show(seq,bm,types)},open(f'runs/nsa_{seed}.json','w'))
