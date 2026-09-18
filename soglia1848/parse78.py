import collections,sys
s=open('ct2.txt').read().strip()
P=sys.argv[1] if len(sys.argv)>1 else '78'
segs=[r for r in s.split('5') if r]
ok=0;bad=[];toks=[]
for r in segs:
    i=0;t=[]
    while i<len(r):
        n=4 if r[i] in P else 2
        t.append(r[i:i+n]); i+=n
    if i==len(r) and all(len(x)==(4 if x[0] in P else 2) for x in t): ok+=1; toks.append(t)
    else: bad.append(r); toks.append(['?'+r])
print(P,'ok',ok,'bad',len(bad),bad)
C=collections.Counter(x for t in toks for x in t)
print(sorted(C.items(),key=lambda x:-x[1])[:70])
print(' / '.join(' '.join(t) for t in toks))
