import re,sys,random,math,os
sys.path.insert(0,'..')
from lang import lm
M=lm.load('it-cinquecento',order=5,spaces=False)
t=open('transcription.txt').read(); t=re.sub(r'#.*','',t)
parts=re.split(r'(\{.*?\})',t)
seq=[]  # items: ('c',tok) or ('p',letter)
for p in parts:
    if p.startswith('{'):
        for ch in lm.norm(p[1:-1],'early').replace(' ',''): seq.append(('p',ch))
    else:
        for x in p.split():
            if x in '|.?': continue
            seq.append(('c',x))
syms=sorted({x for k,x in seq if k=='c'})
A='abcdefghilmnopqrstuxz'
CAP=dict(a=3,e=3,i=3,o=3,u=2,n=2,r=1,l=2,s=2,t=2,c=2,d=1,p=1,m=1,g=1,h=1,b=1,f=1,q=1,x=1,z=1)
def text(key): return ''.join(key[x] if k=='c' else x for k,x in seq)
def score(key): return M.score_idx(M.encode(text(key)))
best=None
for rs in range(int(sys.argv[1]) if len(sys.argv)>1 else 8):
    random.seed(rs); pool=[c for c in A for _ in range(CAP[c])]; random.shuffle(pool); key={s:pool[i] for i,s in enumerate(syms)}
    cur=score(key); T=3.0
    for it in range(40000):
        s=random.choice(syms); old=key[s]; new=random.choice(A)
        if sum(1 for v in key.values() if v==new)>=CAP.get(new,1): 
            s2=random.choice([k for k in syms if key[k]==new]); key[s2],key[s]=old,new
        else: key[s]=new
        old2=None
        n=score(key)
        if n>cur or random.random()<math.exp((n-cur)/T): cur=n
        else:
            if 's2' in dir() and key.get(s2)==old and key[s]==new: key[s2]=new
            key[s]=old
        s2=None
        T=max(0.05,T*0.99985)
    print(rs,round(cur,1),''.join(key[x] if k=='c' else x.upper() for k,x in seq)[:400],flush=True)
    if best is None or cur>best[0]: best=(cur,dict(key))
print(best)
