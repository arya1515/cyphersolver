"""Unsupervised quality metric for a draft: the fraction of decoded letters that the DP
word-segmentation can cover with real period-French words, plus the control-line distance."""
import re, math, glob, unicodedata, collections, sys
def norm(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if unicodedata.category(c)!='Mn')
    t=t.lower().replace('j','i').replace('v','u').replace('w','u')
    return re.sub(r"[^a-z]+",' ',t)
cnt=collections.Counter()
for f in glob.glob('../dubellay/ref/legrand3_*.txt')+glob.glob('../nevers1593/*.txt')+glob.glob('../debosnys/corpus/fr*.txt'):
    try: cnt.update(norm(open(f,encoding='utf-8',errors='ignore').read()).split())
    except Exception: pass
N=sum(cnt.values()); LOGP={w:math.log(c/N) for w,c in cnt.items() if c>=3}
UNK=-14.0; MAXW=14
def cover(s):
    n=len(s); best=[-1e18]*(n+1); bk=[0]*(n+1); best[0]=0.0
    for i in range(1,n+1):
        for L in range(1,min(MAXW,i)+1):
            w=s[i-L:i]; sc=LOGP.get(w,UNK-1.2*L)
            if best[i-L]+sc>best[i]: best[i]=best[i-L]+sc; bk[i]=L
    cov=0; i=n
    while i>0:
        L=bk[i]
        if s[i-L:i] in LOGP and L>=2: cov+=L
        i-=L
    return cov,n
def lev(a,b):
    d=list(range(len(b)+1))
    for i,ca in enumerate(a,1):
        prev=d[:]; d[0]=i
        for j,cb in enumerate(b,1): d[j]=min(prev[j]+1,d[j-1]+1,prev[j-1]+(ca!=cb))
    return d[-1]
TRUTH='squiestoitenlacourtdesauoyeestpartypouruenirici'
for fn in sys.argv[1:]:
    body=[l for l in open(fn).read().splitlines() if l and not l.startswith('##')]
    s=''.join(l.split(' ',1)[1] for l in body)
    c,n=cover(s)
    ctrl=[l for l in body if l.startswith('20 ')][0][3:].replace('v','u').replace('y','i')
    print(f"{fn}: {n} letters, word-covered {100*c/n:.1f}%, control lev {lev(ctrl,TRUTH)}/{len(TRUTH)}")
