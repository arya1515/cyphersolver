import random, math, sys, collections, json
sys.path.insert(0,'..')
from lang import lm
M=lm.load('de-modern')
lines=[l.split() for l in open('ct.txt',encoding='utf8') if not l.startswith('#')]
toks=[t for l in lines for t in l]
syms=sorted({int(t) for t in toks if t.isdigit() and int(t)<100})
codes=sorted({int(t) for t in toks if t.isdigit() and int(t)>=100})
PIN=json.loads(sys.argv[2]) if len(sys.argv)>2 else {}
PIN={int(a):b for a,b in PIN.items()}
A='abcdefghiklmnoprstuwz'+'eeennrsiad'+'h'
SYL=['der','die','das','und','den','dem','des','ein','eine','einen','en','er','ch','sch','st','ge','ver','be','ung','ich','ist','nicht','zu','in','an','auf','mit','von','wie','so','sie','es','e','n','r','s','t','ten','ter','ent','ei','ie','au','kaiser','koenig','england','frankreich','spanien','holland','wien','hannover','preussen','parlament','krieg','frieden','allianz','tractat','gibraltar','ostende','compagnie','russland','schweden','majestaet','minister','land','see','flotte','truppen','armee','hof']
def render(k):
    out=[]
    for l in lines:
        for t in l:
            if t.isdigit():
                n=int(t); out.append(k[n] if n<100 else '|'+k[n]+'|')
            else: out.append('|'+t+'|')
    return ' '.join(''.join(out).replace('|',' ').split())
def score(k): return M.score(render(k))
best=None
keys=[x for x in syms+codes if x not in PIN]
for run in range(int(sys.argv[1])):
    k={s:PIN.get(s,random.choice(A)) for s in syms}
    k.update({c:PIN.get(c,random.choice(SYL)) for c in codes})
    cur=score(k);T=4.0
    for it in range(250000):
        s=random.choice(keys);old=k[s]
        k[s]=random.choice(A) if s<100 else random.choice(SYL); n=score(k)
        if n>=cur or random.random()<math.exp((n-cur)/T): cur=n
        else: k[s]=old
        T=max(0.05,T*0.99997)
    print(run,round(cur,1),flush=True)
    if best is None or cur>best[0]: best=(cur,dict(k))
k=best[1];print(sorted(k.items()));print(render(k))
