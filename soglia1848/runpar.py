import itertools,re,collections
s=open('ct.txt').read()
res=[]
for k in (1,2):
  for sp in itertools.combinations('0123456789',k):
    sp=''.join(sp)
    runs=[len(r) for r in re.split('['+sp+']',s) if r]
    ev=sum(1 for r in runs if r%2==0); 
    # weight by digits
    res.append((ev/len(runs),sp,len(runs),collections.Counter(r%2 for r in runs)))
for r in sorted(res,reverse=True)[:15]: print(r)
