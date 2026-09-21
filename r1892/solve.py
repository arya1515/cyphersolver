import sys,re,random,math
from collections import Counter
txt=re.sub('[^a-z]','',open('lang/corpora/nl-gutenberg.txt',encoding='utf8').read().lower())
Q=Counter(txt[i:i+4] for i in range(len(txt)-3));N=sum(Q.values())
LQ={q:math.log(c/N) for q,c in Q.items()};FL=math.log(0.01/N)
segs=[]
for f in sys.argv[1:]:
  for line in open(f,encoding='utf8'):
    cur=[]
    for t in re.findall(r'\[[^\]]*\]|<[^>]*>|\S+',line):
      t=t.rstrip('?')
      if re.fullmatch(r'[1-6]{2}',t): cur.append(t)
      elif cur: segs.append(cur); cur=[]
    if cur: segs.append(cur)
syms=sorted({t for s in segs for t in s})
A='abcdefghijklmnopqrstuvwxyz'
def dec(k): return [''.join(k[t] for t in s) for s in segs]
def score(k):
  return sum(LQ.get(x[i:i+4],FL) for x in dec(k) for i in range(len(x)-3))
best=None
for r in range(int(sys.argv[0] and 6)):
  L=list(A); random.shuffle(L); L+=list('eeee')
  k={t:L[i] for i,t in enumerate(syms)}; s=score(k)
  for T in [x/100 for x in range(300,0,-1)]:
    for _ in range(40):
      a,b=random.sample(syms,2); k[a],k[b]=k[b],k[a]; n=score(k)
      if n>s or random.random()<math.exp((n-s)/T): s=n
      else: k[a],k[b]=k[b],k[a]
  if not best or s>best[0]: best=(s,dict(k))
  print(r,round(s),' '.join(dec(k))[:160],flush=True)
s,k=best
print(sorted(k.items()))
print('\n'.join(' '.join(x) for x in [dec(k)]))
