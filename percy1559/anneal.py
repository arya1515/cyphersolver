import re,collections,math,random,sys
exec(open('pattern_search.py').read().split("txt=")[0])
txt=open('../burghley1559/sadler1.txt',encoding='utf-8',errors='ignore').read().lower()
txt=re.sub(r'[^a-z]+',' ',txt)
tri=collections.Counter(txt[i:i+3] for i in range(len(txt)-2))
tot=sum(tri.values())
def lp(g): return math.log((tri.get(g,0)+0.1)/tot)
mode=sys.argv[1] if len(sys.argv)>1 else 'marks'
def norm(t): return t if mode=='marks' else t[0]
ws=[[norm(t) for t in w] for k in '1234' for w in lines[k]]
syms=sorted({s for w in ws for s in w})
A='abcdefghiklmnopqrstuwy'
def dec(m): return ' '.join(''.join(m[s] for s in w) for w in ws)
def score(m):
    t=' '+dec(m)+' '; return sum(lp(t[i:i+3]) for i in range(len(t)-2))
best=None
for r in range(30):
    m={s:random.choice(A) for s in syms}; sc=score(m); T=3
    for it in range(20000):
        s=random.choice(syms); o=m[s]; m[s]=random.choice(A); n=score(m)
        if n>sc or random.random()<math.exp((n-sc)/T): sc=n
        else: m[s]=o
        T=max(0.05,T*0.9997)
    if best is None or sc>best[0]: best=(sc,dict(m))
    print(round(sc,1),dec(m),flush=True)
