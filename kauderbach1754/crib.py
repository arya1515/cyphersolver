import json,collections,re,unicodedata
D=json.load(open('pairs.json'))
seqs=[[t for t in tk if not t.startswith('*')] for f,tk in D]
# long repeats in pair space
C=collections.Counter()
for s in seqs:
  for n in range(6,16):
    for i in range(len(s)-n+1): C[tuple(s[i:i+n])]+=1
reps=[(k,v) for k,v in C.items() if v>=3 and len(k)>=7]
# keep maximal
reps.sort(key=lambda x:(-len(x[0]),-x[1]))
maxi=[]
for k,v in reps:
  ks=' '.join(k)
  if not any(ks in ' '.join(m) for m,_ in maxi): maxi.append((k,v))
for k,v in maxi[:25]: print(v,' '.join(k))
json.dump([[list(k),v] for k,v in maxi[:40]],open('reps.json','w'))
