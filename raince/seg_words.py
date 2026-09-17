"""Segment the letter stream into French words with a DP over a period-French lexicon,
allowing a small number of unknown chunks. Purely a reading aid for the draft."""
import re, math, glob, unicodedata, json, collections, sys
def norm(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if unicodedata.category(c)!='Mn')
    t=t.lower().replace('j','i').replace('v','u').replace('w','u')
    return re.sub(r"[^a-z]+",' ',t)
cnt=collections.Counter()
for f in glob.glob('../dubellay/ref/legrand3_*.txt')+glob.glob('../nevers1593/*.txt')+glob.glob('../debosnys/corpus/fr*.txt'):
    try: cnt.update(norm(open(f,encoding='utf-8',errors='ignore').read()).split())
    except Exception: pass
N=sum(cnt.values())
LOGP={w: math.log(c/N) for w,c in cnt.items() if c>=3}
UNK=-14.0
MAXW=14
def seg(s):
    n=len(s); best=[-1e18]*(n+1); bk=[0]*(n+1); best[0]=0.0
    for i in range(1,n+1):
        for L in range(1,min(MAXW,i)+1):
            w=s[i-L:i]
            sc=LOGP.get(w, UNK-1.2*L)
            if best[i-L]+sc>best[i]: best[i]=best[i-L]+sc; bk[i]=L
    out=[]; i=n
    while i>0:
        L=bk[i]; w=s[i-L:i]
        out.append(w if w in LOGP else w.upper()); i-=L
    return ' '.join(reversed(out))
txt=open(sys.argv[1] if len(sys.argv)>1 else 'draft5.txt').read().splitlines()
for ln in txt:
    if ln.startswith('##') or not ln.strip(): print(ln); continue
    num,body=ln.split(' ',1)
    print(num, seg(body))
