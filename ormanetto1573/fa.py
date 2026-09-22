import sys,os
sys.path.insert(0,'../caprile1519'); sys.path.insert(0,'..')
import types; sys.modules['anneal']=types.SimpleNamespace(runs=None)
import fastanneal as F
from tok import load
from units import units
nulls=set(os.environ.get('NULLS','').split(','))
if os.environ.get('CTL'):
    import random;R=random.Random(3)
    t=open('../lang/corpora/it-nunziature.txt',encoding='utf-8').read()
    t=''.join(c for c in t.lower() if c in 'abcdefghilmnopqrstuz')[300000:301000]
    h={c:[c+'0'] for c in set(t)}
    for c in 'eaoinlrt': h[c].append(c+'1')
    seqs=[[R.choice(h[c]) for c in t]];print('TRUE',t[:150])
else:
    seqs=[[u for u in units(p) if u not in nulls] for p in load() if p]
(sc,key),toks=F.run(seqs,int(sys.argv[1]),int(sys.argv[2]),seed=int(sys.argv[3]) if len(sys.argv)>3 else 1)
print('best',sc/sum(map(len,seqs)));print({t:F.M.alpha[k] for t,k in zip(toks,key)})
ti={t:i for i,t in enumerate(toks)}
for s in seqs: print(''.join(F.M.alpha[key[ti[t]]] for t in s)[:300])
