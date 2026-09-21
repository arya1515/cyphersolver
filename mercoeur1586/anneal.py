# Homophonic anneal: each sign -> one letter, scored with a 4-gram French model (Henri IV letters, matignon1586/lm.pkl).
import pickle, math, random, sys
d=pickle.load(open('../matignon1586/lm.pkl','rb')); cnt=d['cnt']
N=4; A='abcdefghilmnopqrstuxyz'
tot3={}
def lp(g):
    c=cnt[4].get(g,0); b=cnt[3].get(g[:3],0)
    return math.log((c+0.1)/(b+0.1*len(A)))
T={}
import itertools
for g in itertools.product(A,repeat=4): T[''.join(g)]=lp(''.join(g))
toks=[w for l in open('cipher.txt',encoding='utf-8') if not l.startswith('#') for w in l.split()[1:]]
runs=[];cur=[]
for l in open('cipher.txt',encoding='utf-8'):
    if l.startswith('#'): continue
    runs.append(l.split()[1:])
def score(m):
    s=0
    for r in runs:
        p=''.join(m[x] for x in r)
        for i in range(len(p)-3): s+=T[p[i:i+4]]
    return s
freq={'e':15,'s':8,'a':8,'i':8,'t':7,'n':7,'r':7,'u':7,'o':5,'l':5,'d':4,'c':3,'m':3,'p':3}
pool=''.join(k*v for k,v in freq.items())+'bfghqxyz'
def run(seed,runs_=None):
    random.seed(seed); syms=sorted(set(x for r in runs for x in r))
    m={s:random.choice(pool) for s in syms}; sc=score(m); best=(sc,dict(m)); t=3.0
    for it in range(60000):
        s=random.choice(syms); old=m[s]; m[s]=random.choice(A); n=score(m)
        if n>sc or random.random()<math.exp((n-sc)/t): sc=n
        else: m[s]=old
        if sc>best[0]: best=(sc,dict(m))
        t=max(0.05,t*0.99993)
    return best
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='shuf':
        flat=[x for r in runs for x in r]; random.seed(99); random.shuffle(flat); i=0
        for k,r in enumerate(runs): runs[k]=flat[i:i+len(r)]; i+=len(r)
    res=[run(s) for s in range(int(sys.argv[2]))]
    res.sort(key=lambda x:-x[0])
    for sc,m in res[:3]:
        print(mode, round(sc/len(toks),3), ' | '.join(''.join(m[x] for x in r) for r in runs))
