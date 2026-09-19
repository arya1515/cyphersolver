import json,sys,collections,solve as B
LQ,FL=B.LQ,B.FL
K=json.load(open(sys.argv[1]))
EXT='a ai an au b be bi c ca ce ci co d da de di do du e em en er es et f fai fe g ga ge h hi i ia ie il j ju k l la le m ma me n na ne ni no nu o oi on ou p pour pr q que qui qu r ra re ri s sa se si son st t te u v vous x y z pas par ous ent ment ont les des tion nt ss ll ur us eu ui is it'.split()
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
occ=collections.defaultdict(set)
for k,sg in enumerate(segsT):
  for t in sg: occ[t].add(k)
def sc(k):
  t=''.join(K[x] for x in segsT[k]); return sum(LQ.get(t[j:j+4],FL) for j in range(len(t)-3))/1.0
changed=True
while changed:
  changed=False
  for code in sorted(occ,key=lambda c:len(occ[c])):
    old=K[code]; base=sum(sc(k) for k in occ[code]); bestv,bests=old,base
    for v in EXT:
      K[code]=v; s=sum(sc(k) for k in occ[code])
      # penalise longer strings slightly to avoid greedy merges
      s-=0.3*len(occ[code])*(len(v)-len(old)) if len(v)>len(old) else 0
      if s>bests+1.0: bests,bestv=s,v
    K[code]=bestv
    if bestv!=old: print(code,old,'->',bestv,round(bests-base,1)); changed=True
json.dump(K,open(sys.argv[2],'w'))
