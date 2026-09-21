import sys,os,re,collections,math
sys.path.insert(0,r'C:\Users\dbour\cypher\.worktrees\beatrice1482')
from lang import lm
from corpus import C,OTHER
m=lm.load('it-modern',order=5,spaces=False)
K={}
for l in (x for x in open("key.tsv",encoding="utf-8") if not x.startswith("#")):
    a,b=l.rstrip('\n').split('\t')[:2]; K[a]=b
def norm(t): return 'NULL' if len(t)>=5 else t
seqs=[[norm(t) for t in ts if '?' not in t] for r,ts in C.items() if r not in OTHER]
seqs=[[t for t in s if t!='NULL'] for s in seqs]
cnt=collections.Counter(t for s in seqs for t in s)
def txt(v): return lm.norm(v,'modern') if v not in ('·',',','.') else ''
# candidate inventory: syllables from known values + CV/CVC patterns
V='aeiou'; Cn='bcdfglmnpqrstvz'
cands=set(txt(v) for v in K.values())
for c in list(Cn)+['ch','gh','gl','gn','sc','st','tr','pr','br','cr','dr','fr','gr','pl','qu','sp','str']:
    for v in V:
        cands.add(c+v)
        for e in 'lnrst': cands.add(c+v+e)
for v in V:
    cands.add(v)
    for e in 'lnrs': cands.add(v+e)
cands|={'ne','zione','sione','mente','ssi','zio','zia','io','ia','ie','uo','gli','che','non','per','con','del','nel','sul','il','lo','le','la','un','una','ed','si','se','ma','ha','ho','sono','essere','stato','fra','tra','sua','suo','loro','questo','quello','questa','quella','Re','Duca','Principe','Governo','Corte','Ministro','Inghilterra','Russia','Spagna','Austria','Napoli','Roma','Parigi','Londra'}
cands={c for c in cands if c}
cands=[lm.norm(c,'modern') for c in cands]
BONUS=float(sys.argv[2]) if len(sys.argv)>2 else 2.3
def windows(g,W=3):
    out=[]
    for s in seqs:
        for i,x in enumerate(s):
            if x!=g: continue
            L=[];j=i-1
            while j>=0 and s[j] in K and len(L)<W: L.insert(0,txt(K[s[j]]));j-=1
            R=[];j=i+1
            while j<len(s) and s[j] in K and len(R)<W: R.append(txt(K[s[j]]));j+=1
            if L or R: out.append((''.join(L),''.join(R)))
    return out
def best(g):
    ws=windows(g)
    if len(ws)<3: return None
    sc=lambda x: m.score(x) if x else 0.0
    base=sum(sc(l)+sc(r) for l,r in ws)
    res=[]
    for c in cands:
        s=sum(sc(l+c+r) for l,r in ws)-base-len(ws)*sc(c)
        res.append((s/len(ws),c))
    res.sort(reverse=True)
    return res[:4],len(ws)
if __name__=='__main__':
    N=int(sys.argv[1])
    for g,c in cnt.most_common():
        if g in K: continue
        r=best(g)
        if r: print(g,c,r[1],' '.join(f'{b}:{a:.1f}' for a,b in r[0]))
        N-=1
        if N==0: break
