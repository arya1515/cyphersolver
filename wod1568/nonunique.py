# Non-uniqueness test for the 39-sign Wood line: anneal a homophonic key (each sign -> one letter)
# against a quadgram model of Bain ii (Scots/English 1563-69) from many random restarts, and report
# how many mutually different readings score at least as well as real text of the same length.
import numpy as np,re,random
t=re.sub('[^a-z]','',open('bain2.txt',encoding='utf-8',errors='ignore').read().lower())
ix=np.frombuffer(t.encode(),dtype=np.uint8).astype(np.int64)-97
q=ix[:-3]*17576+ix[1:-2]*676+ix[2:-1]*26+ix[3:]
c=np.bincount(q,minlength=26**4).astype(float); T=np.log((c+.05)/(c.sum()+.05*26**4))
def sc(p): p=np.asarray(p); return T[p[:-3]*17576+p[1:-2]*676+p[2:-1]*26+p[3:]].sum()
signs=open('wood_line.txt',encoding='utf-8').read().split()
signs=[s for s in signs if s!='/']
S=sorted(set(signs)); n=len(signs); idx=[S.index(s) for s in signs]
print(n,'signs',len(S),'distinct')
# reference: real text windows of same length
rs=[sc(ix[k:k+n]) for k in random.sample(range(len(ix)-n),2000)]
ref=np.percentile(rs,50); print('median real-text score',round(ref,1),'90th',round(np.percentile(rs,90),1))
res=[]
random.seed(1)
for r in range(200):
    key=[random.randrange(26) for _ in S]; cur=sc([key[i] for i in idx]); Tm=3.0
    for it in range(6000):
        k=random.randrange(len(S)); old=key[k]; key[k]=random.randrange(26)
        s=sc([key[i] for i in idx])
        if s>cur or random.random()<np.exp((s-cur)/Tm): cur=s
        else: key[k]=old
        Tm=max(.05,Tm*0.999)
    res.append((cur,''.join(chr(97+key[i]) for i in idx)))
res.sort(reverse=True)
good=[r for r in res if r[0]>=ref]
print('restarts scoring above median real text:',len(good),'of',len(res))
d=[]
for s,p in good:
    if all(sum(a!=b for a,b in zip(p,x))>n//3 for x in d): d.append(p)
print('mutually distinct (>1/3 letters differ):',len(d))
for s,p in res[:12]: print(round(s,1),p)
