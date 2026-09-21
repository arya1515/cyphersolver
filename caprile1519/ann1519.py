import json, fastanneal as F
from anneal import runs
fixed=json.load(open('fixed1519.json'))
fixed={k.replace('[','L').replace(']',''):v for k,v in fixed.items()}
seqs=[s for s in runs('c1519.txt') if len(s)>=2]
print(len(seqs),sum(map(len,seqs)))
(sc,key),toks=F.run(seqs,150000,12,seed=11,fixed=fixed)
k={t:F.M.alpha[v] for t,v in zip(toks,key)}
json.dump(k,open('key1519_ann.json','w'),indent=0)
print('best',sc)
for line in open('c1519.txt',encoding='utf8'):
    lab,s=line.split(':',1)
    print(lab, ''.join('|' if t=='[x]' else k.get(t,'?') for t in s.split()))
