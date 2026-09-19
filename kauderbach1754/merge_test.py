import sys,json,collections,align,hs3,real
m=dict(x.split('>') for x in sys.argv[1].split(',')) if sys.argv[1]!='-' else {}
S=[''.join(m.get(c,c) for c in s) for f,s in real.load()]
out=align.realign(S)
segsT=[]
for tk in out:
  cur=[]
  for t in tk:
    if t.startswith('*'):
      if len(cur)>=3: segsT.append(cur)
      cur=[]
    else: cur.append(t)
  if len(cur)>=3: segsT.append(cur)
syms=sorted({t for sg in segsT for t in sg}); idx={t:i for i,t in enumerate(syms)}
segsI=[[idx[t] for t in sg] for sg in segsT]
sc,key=hs3.run(segsI,len(syms),restarts=8,W=10,seed=1)
print(sys.argv[1],len(syms),sc/sum(map(len,segsI)))
print('|'.join(''.join(key[i] for i in sg) for sg in segsI)[:500])
