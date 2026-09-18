import sys,re,json,math,random,collections
Q=json.load(open('../richelieu/fr_quadgrams.json'))
tot=sum(Q.values()); LQ={k:math.log10(v/tot) for k,v in Q.items()}; FL=math.log10(0.01/tot)
def qscore(s):
    return sum(LQ.get(s[i:i+4],FL) for i in range(len(s)-3))
from dec import K0
files=sys.argv[1].split(',')
segs=[]
for f in files:
  for line in open(f,encoding='utf-8'):
    m=re.match(r'(C\d+):\s*(.*)',line)
    if m: segs.append(m.group(2).split())
toks=sorted(set(t for s in segs for t in s))
ALPH='abcdefghilmnopqrstuxyz'
key={t:K0.get(t,'') for t in toks}
fixed_null={'#','...','C','?','xx'}
def text(k): return '|'.join(''.join(k[t] for t in s) for s in segs)
def score(k):
    return sum(qscore(''.join(k[t] for t in s)) for s in segs)
random.seed(int(sys.argv[2]) if len(sys.argv)>2 else 1)
cur=score(key); best=(cur,dict(key))
T=float(sys.argv[3]) if len(sys.argv)>3 else 3.0
free=[t for t in toks if t not in fixed_null]
for it in range(40000):
    t=random.choice(free); old=key[t]
    key[t]=random.choice(ALPH+'e'*3)
    if key[t]==old: continue
    s=score(key)
    temp=T*(1-it/40000)+0.05
    if s>cur or random.random()<math.exp((s-cur)/temp):
        cur=s
        if s>best[0]: best=(s,dict(key))
    else: key[t]=old
print(best[0])
k=best[1]
cnt=collections.Counter(t for s in segs for t in s)
print(' '.join(f'{t}={k[t] or "_"}{"*" if k[t]!=K0.get(t,"") else ""}' for t in sorted(toks,key=lambda x:-cnt[x])))
for s in segs[:40]: print(''.join(k[t] or '' for t in s))
