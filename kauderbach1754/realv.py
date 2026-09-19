import json,sys,hs3v as hs3
D=json.load(open('pairs.json'))
V=set(['24','29','92','16','32','94','69','03','43','64','09','41','47','31','72','33','97','74','46','13'])
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
import collections; cnt=collections.Counter(t for sg in segsT for t in sg)
allowed=[('aeiouy' if s in V else 'bcdfghjlmnpqrstvxz') if cnt[s]>=15 else 'abcdefghijlmnopqrstuvxyz' for s in syms]
sc,key=hs3.run(segsI,len(syms),allowed=allowed,restarts=int(sys.argv[1]),W=10,seed=int(sys.argv[2]))
print(sc/sum(map(len,segsI)))
print(' '.join(f'{s}={k}' for s,k in zip(syms,key)))
print('|'.join(''.join(key[i] for i in sg) for sg in segsI)[:2000])
