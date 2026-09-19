import random,sys,collections,hs3,solve as B
rnd=random.Random(5)
pt=B.corp[100000:100000+int(sys.argv[1])]
codes=list(range(64)); rnd.shuffle(codes)
f=collections.Counter(pt); alloc={}; ci=0
for l,_ in f.most_common():
  n=max(1,round(64*f[l]/len(pt)*0.9)) if ci<64 else 0
  alloc[l]=codes[ci:ci+n] or [codes[rnd.randrange(64)]]; ci+=n
ct=[rnd.choice(alloc[c]) for c in pt]
segs=[ct[i:i+150] for i in range(0,len(ct),150)]
sc,key=hs3.run(segs,64,restarts=int(sys.argv[2]),W=float(sys.argv[3]))
dec=''.join(key[c] for c in ct); print(sum(a==b for a,b in zip(dec,pt))/len(pt)); print(dec[:200])
