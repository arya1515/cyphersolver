import random,sys,hs2 as hsolve,solve as B
rnd=random.Random(5)
pt=B.corp[100000:103000]
letters=sorted(set(pt)); codes=list(range(64)); rnd.shuffle(codes)
# homophones: give frequent letters several codes
import collections
f=collections.Counter(pt); alloc={}
ci=0
for l,_ in f.most_common():
  n=max(1,round(64*f[l]/len(pt)*0.9)) if ci<64 else 0
  alloc[l]=codes[ci:ci+n] or [codes[rnd.randrange(64)]]; ci+=n
ct=[rnd.choice(alloc[c]) for c in pt]
segs=[ct[i:i+150] for i in range(0,len(ct),150)]
T0=float(sys.argv[1]); 
sc,key=hsolve.run(segs,64,int(sys.argv[2]),1,T0)
key=key
dec=''.join(key[c] for c in ct); print(sc/len(ct),sum(a==b for a,b in zip(dec,pt))/len(pt)); print(dec[:200]); print(pt[:200])
true=['?']*64
for l,cs in alloc.items():
  for c in cs: true[c]=l
print(''.join(true)); print(''.join(key))
s2,_=hsolve.run(segs,64,0,1,T0,init=true); print('true score',s2/len(ct))
