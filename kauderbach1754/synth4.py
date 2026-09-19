import random,sys,collections,hs3,solve as B
rnd=random.Random(7)
pt=B.corp[500000:506400]
codes=list(range(56)); rnd.shuffle(codes)
f=collections.Counter(pt); alloc={}; ci=0
for l,_ in f.most_common():
  n=max(1,round(56*f[l]/len(pt)*0.85)) if ci<56 else 0
  alloc[l]=codes[ci:ci+n] or [codes[rnd.randrange(56)]]; ci+=n
ct=[rnd.choice(alloc[c]) if rnd.random()>float(sys.argv[1]) else rnd.randrange(56) for c in pt]
segs=[];i=0
while i<len(ct):
  L=rnd.randint(10,200); segs.append(ct[i:i+L]); i+=L
sc,key=hs3.run(segs,56,restarts=10,W=10)
dec=''.join(key[c] for c in ct); print(sc/len(ct),sum(a==b for a,b in zip(dec,pt))/len(pt)); print(dec[:200])
