import random, math, sys, collections
sys.path.insert(0,'..')
from lang import lm
M=lm.load('de-modern')
lines=[l.split() for l in open('ct.txt',encoding='utf8') if not l.startswith('#')]
toks=[t for l in lines for t in l]
syms=sorted({int(t) for t in toks if t.isdigit() and int(t)<100})
cnt=collections.Counter(int(t) for t in toks if t.isdigit())
print(len(syms),'letter syms', sum(cnt[s] for s in syms),'tokens'); print(cnt.most_common(20))
CODES={230:'der'}
PIN={33:'e',23:'n',40:'s'}
A='abcdefghiklmnoprstuwz'+'eeenn'
def render(k):
    out=[];prev_num=False
    for l in lines:
        for t in l:
            if t.isdigit():
                n=int(t)
                if n<100:
                    out.append(k[n] if not prev_num or out[-1]!=' ' else k[n]); prev_num=True
                else:
                    out.append(' '+CODES.get(n,'')+' ' if n in CODES else ' ' ); prev_num=False
            else:
                out.append(' '+t+' '); prev_num=False
    return ' '.join(''.join(out).split())
def score(k): return M.score(render(k))
best=None
for run in range(int(sys.argv[1]) if len(sys.argv)>1 else 8):
    k={s:PIN.get(s,random.choice(A)) for s in syms}
    cur=score(k);T=3.0
    for it in range(40000):
        s=random.choice([x for x in syms if x not in PIN]);old=k[s]
        k[s]=random.choice(A); n=score(k)
        if n>=cur or random.random()<math.exp((n-cur)/T): cur=n
        else: k[s]=old
        T=max(0.05,T*0.9998)
    print(run,round(cur,1)); 
    if best is None or cur>best[0]: best=(cur,dict(k))
k=best[1];print(sorted(k.items()));print(render(k))
