import sys,re,json,math,collections
Q=json.load(open('../richelieu/fr_quadgrams.json'))
T3=collections.Counter()
for k,v in Q.items(): T3[k[:3]]+=v
LQ={k:math.log10(v/T3[k[:3]]) for k,v in Q.items()}
def qs(s):
    r=0
    for i in range(len(s)-3):
        q=s[i:i+4]; r+=LQ.get(q, math.log10(0.5/(T3.get(q[:3],0)+30)))
    return r
from dec import K0
segs=[]
for f in sys.argv[1].split(','):
  for line in open(f,encoding='utf-8'):
    m=re.match(r'(C\d+):\s*(.*)',line)
    if m: segs.append(m.group(2).split())
cnt=collections.Counter(t for s in segs for t in s)
key={t:K0.get(t,'') for t in cnt}
def score(k): return sum(qs(''.join(k[t] for t in s)) for s in segs)
ALPH=list('abcdefghilmnopqrstuxyz')
base=score(key); print('base',round(base,1))
for rnd in range(3):
  changed=0
  for t in sorted(cnt,key=lambda x:-cnt[x]):
    res=[]
    if key[t]=='': continue
    for a in ALPH:
        old=key[t]; key[t]=a; res.append((score(key),a)); key[t]=old
    res.sort(reverse=True)
    cur=[r for r in res if r[1]==key[t]][0][0]
    top=' '.join(f'{a or "_"}:{s-cur:+.0f}' for s,a in res[:4])
    if rnd==0: print(f'{t:4} n={cnt[t]:3} cur={key[t] or "_"}  {top}')
    if res[0][1]!=key[t] and res[0][0]-cur>3 and len(sys.argv)>2:
        key[t]=res[0][1]; changed+=1
  if len(sys.argv)<=2 or not changed: break
print('final',round(score(key),1))
json.dump(key,open('key_refined.json','w'))
