import random,collections,json,solve as B,align,hs3
rnd=random.Random(3)
pt=B.corp[700000:706500]
codes=[a+b for a in '01234679' for b in '1234679']; rnd.shuffle(codes); codes=codes[:48]
f=collections.Counter(pt); alloc={}; ci=0
for l,_ in f.most_common():
  n=max(1,round(48*f[l]/len(pt)*0.85)) if ci<48 else 0
  alloc[l]=codes[ci:ci+n] or [codes[rnd.randrange(48)]]; ci+=n
digits=''
for c in pt:
  digits+=rnd.choice(alloc[c])
  if rnd.random()<0.06: digits+=rnd.choice('58')
S=[];i=0
while i<len(digits):
  L=rnd.randint(20,400); S.append(digits[i:i+L]); i+=L
S=[s.replace('5','').replace('8','') for s in S]
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
sc,key=hs3.run(segsI,len(syms),restarts=8,W=10)
print(sc/sum(map(len,segsI)))
print('|'.join(''.join(key[i] for i in sg) for sg in segsI)[:600])
