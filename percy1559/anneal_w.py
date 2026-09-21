import re,collections,math,random,sys
exec(open('pattern_search.py').read().split("txt=")[0])
t=open('../burghley1559/sadler1.txt',encoding='utf-8',errors='ignore').read()+open('sources/worksofjohnknox06knox.txt',encoding='utf-8',errors='ignore').read()[200000:900000]
t=re.sub(r'[^a-z]+',' ',t.lower())
wc=collections.Counter(t.split())
for n in "knox knoxe prior priour lord lorde laird lard whitlaw whytlaw whitlawe hume dowager dyogre congregation merse tevedale haddington croft james kirkcaldy kyrkcaldy grange".split(): wc[n]+=300
W=sum(wc.values())
tri=collections.Counter(t[i:i+3] for i in range(len(t)-2)); T=sum(tri.values())
mode=sys.argv[1]
def norm(s): return s if mode=='marks' else s[0]
ws=[[norm(s) for s in w] for k in '1234' for w in lines[k]]
syms=sorted({s for w in ws for s in w}); A='abcdefghiklmnopqrstuwy'
def wscore(x):
    if x in wc: return math.log(wc[x]/W)+2
    y=' '+x+' '; return sum(math.log((tri.get(y[i:i+3],0)+.05)/T) for i in range(len(y)-2))-6
def sc(m): return sum(wscore(''.join(m[s] for s in w)) for w in ws)
res=[]
for r in range(40):
    m={s:random.choice(A) for s in syms}; c=sc(m); Tm=4
    for it in range(15000):
        s=random.choice(syms);o=m[s];m[s]=random.choice(A);n=sc(m)
        if n>c or random.random()<math.exp((n-c)/Tm): c=n
        else: m[s]=o
        Tm=max(.05,Tm*.9995)
    d=[''.join(m[s] for s in w) for w in ws]
    res.append((c,' '.join(d),sum(x in wc for x in d)))
for r in sorted(res,reverse=True)[:10]: print(round(r[0],1),r[2],r[1])
