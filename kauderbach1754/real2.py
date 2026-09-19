import json,sys,hs3
D=json.load(open('pairs.json'))
segsT=[]
for f,tk in D:
  cur=[]
  for t in tk:
    if t.startswith('*'):
      if len(cur)>=3: segsT.append(cur)
      cur=[]
    else: cur.append(t)
  if len(cur)>=3: segsT.append(cur)
syms=sorted({t for sg in segsT for t in sg}); idx={t:i for i,t in enumerate(syms)}
segsI=[[idx[t] for t in sg] for sg in segsT]
sc,key=hs3.run(segsI,len(syms),restarts=int(sys.argv[1]),W=float(sys.argv[2]),seed=int(sys.argv[3]))
print(sc/sum(map(len,segsI)))
print(' '.join(f'{s}={k}' for s,k in zip(syms,key)))
print('|'.join(''.join(key[i] for i in sg) for sg in segsI)[:3000])
