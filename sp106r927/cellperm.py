import json,random,math,numpy as np,hc2,sys
g=json.load(open(sys.argv[1])); lg=sys.argv[2]
arr=hc2.prep(json.load(open(f'q_{lg}.json')))
keyc=['akt','blu','cmw','dnx','eoy','fpz','gq','hr','is']
toks=[(x['sh'],max(1,min(x['nd'],3))) for L in g for x in L if x['sh']!='?']
SH='ABCDEFGHI'
def text(p):
    return np.array([ord(keyc[p[SH.index(s)]][min(d,len(keyc[p[SH.index(s)]]))-1])-97 for s,d in toks])
def sc(p):
    L=text(p); return arr[((L[:-3]*26+L[1:-2])*26+L[2:-1])*26+L[3:]].sum()/len(L)
best=(-99,None)
for r in range(30):
    p=list(range(9)); random.shuffle(p); cur=sc(p)
    for it in range(3000):
        i,j=random.sample(range(9),2); p[i],p[j]=p[j],p[i]; n=sc(p)
        T=max(0.002,0.2*(1-it/3000))
        if n>=cur or random.random()<math.exp((n-cur)/T): cur=n
        else: p[i],p[j]=p[j],p[i]
    if cur>best[0]: best=(cur,p[:])
p=best[1]; print(lg,best[0],{SH[i]:keyc[p[i]] for i in range(9)})
print(''.join(chr(97+c) for c in text(p))[:200])
