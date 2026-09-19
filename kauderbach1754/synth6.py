import random,sys,collections,hs6,solve as B,re
rnd=random.Random(7)
pt=B.corp[500000:509000]
# tokenise plaintext: greedily use syllable codes for some words
sylset=['de','le','la','les','des','que','qui','et','en','pour','par']
toks=[];i=0
while i<len(pt):
  for s in sorted(sylset,key=len,reverse=True):
    if pt.startswith(s,i) and rnd.random()<0.5: toks.append(s); i+=len(s); break
  else: toks.append(pt[i]); i+=1
units=collections.Counter(toks); codes=list(range(60)); rnd.shuffle(codes); alloc={};ci=0
for u,c in units.most_common():
  n=max(1,round(60*c/len(toks)*0.8)) if ci<60 else 0
  alloc[u]=codes[ci:ci+n] or [codes[rnd.randrange(60)]]; ci+=n
ct=[rnd.choice(alloc[u]) for u in toks]
segs=[];i=0
while i<len(ct):
  L=rnd.randint(10,200); segs.append(ct[i:i+L]); i+=L
sc,key=hs6.run(segs,60,restarts=int(sys.argv[1]),W=10,log=True)
dec=''.join(key[c] for c in ct); print(sc); print(dec[:300]); print(pt[:300])
