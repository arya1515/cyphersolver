import json,sys,hs6
V1761='a ai an au b be bi c ca ce ci co d da de di do du e em en er es et f fai fe g ga ge h hi i ia ie il ju k l la le ma me n na ne ni no nu o oi on ou p pour pr q que qui r ra re ri s sa se si son t te u v vous x y z'.split()
V1761=[v for v in V1761 if v!='w']
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
sc,key=hs6.run(segsI,len(syms),restarts=int(sys.argv[1]),W=float(sys.argv[2]),seed=int(sys.argv[3]),log=True,vals=V1761)
print(sc)
print(' '.join(f'{s}={k}' for s,k in zip(syms,key)))
print('|'.join(''.join(key[i] for i in sg) for sg in segsI)[:3000])
json.dump(dict(zip(syms,key)),open(f'key7_{sys.argv[3]}.json','w'))
