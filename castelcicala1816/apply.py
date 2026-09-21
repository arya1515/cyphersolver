import sys,collections
sys.path.insert(0,'.')
from corpus import C,OTHER
K={}
for l in (x for x in open("key.tsv",encoding="utf-8") if not x.startswith("#")):
    a,b=l.rstrip('\n').split('\t')[:2]; K[a]=b
def norm(t):
    if len(t)>=5: return 'NULL'
    return t
tot=hit=0
for r,ts in C.items():
    if r in OTHER: continue
    out=[]
    for t in ts:
        t=norm(t); tot+=1
        if t in K: hit+=1; out.append(K[t])
        else: out.append('['+t+']')
    if len(sys.argv)>1 and r in sys.argv[1:]: print(r,' '.join(out))
print('coverage',hit,tot,round(hit/tot,3))
