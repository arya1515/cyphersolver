# coordinate-ascent solver: each code group -> string, scored by char 5-gram LM over the concatenated decryption
import math,collections,json,sys,random
from view import load
N=5
txt=open('corpus_fr.txt').read().replace('\n','')
cnt=[collections.Counter() for _ in range(N+1)]
for n in range(1,N+1):
    for i in range(len(txt)-n+1): cnt[n][txt[i:i+n]]+=1
tot=len(txt)
cache={}
def lp(ctx,c):
    k=(ctx,c)
    if k in cache: return cache[k]
    # interpolated absolute-discount-ish backoff
    p=(cnt[1][c]+1)/(tot+26)
    for n in range(1,N):
        h=ctx[-n:] if n<=len(ctx) else None
        if h is None: break
        hc=cnt[n][h]
        if hc==0: break
        w=hc/(hc+5.0)
        p=w*cnt[n+1][h+c]/hc+(1-w)*p
    v=math.log(p);cache[k]=v;return v
def score(s,start=0):
    return sum(lp(s[max(0,i-N+1):i],s[i]) for i in range(start,len(s)))
BONUS=float(sys.argv[3]) if len(sys.argv)>3 else 2.1
def cands(maxn=5,top=2500):
    c=collections.Counter()
    for n in range(1,maxn+1):
        for g,v in cnt[n].items(): c[g]=v*(n**1.5)
    return [g for g,_ in c.most_common(top)]
if __name__=='__main__':
    code=sys.argv[1]; passes=int(sys.argv[2])
    L=load(code); seed=json.load(open(f'key_{code}.json',encoding='utf8'))
    import unicodedata,re
    def norm(s):
        s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if unicodedata.category(c)!='Mn'); return re.sub(r'[^a-z]','',s)
    fixed={int(k):norm(v) for k,v in seed.items()}
    docs=list(L.values())
    freq=collections.Counter(x for d in docs for x in d)
    occ=collections.defaultdict(list)
    for di,d in enumerate(docs):
        for i,x in enumerate(d): occ[x].append((di,i))
    C=cands()
    key=dict(fixed)
    for g in freq:
        if g not in key: key[g]='e'
    def window(di,i,g,val):
        d=docs[di]
        left=''.join(key[x] for x in d[max(0,i-3):i])[-4:]
        right=''.join(key[x] for x in d[i+1:i+3])[:5]
        s=left+val+right
        return score(s,len(left))+BONUS*len(val)
    order=[g for g,_ in freq.most_common() if g not in fixed and freq[g]>=2]
    for p in range(passes):
        ch=0
        for g in order:
            best=None
            for v in C:
                sc=sum(window(di,i,g,v) for di,i in occ[g])
                if best is None or sc>best[0]: best=(sc,v)
            if best[1]!=key[g]: ch+=1; key[g]=best[1]
        print('pass',p,'changed',ch,flush=True)
        json.dump({str(k):v for k,v in key.items()},open(f'auto_{code}.json','w'))
    for name,d in L.items():
        print('==',name); print(' '.join(key[x] if x not in fixed else key[x].upper() for x in d[:200]))
