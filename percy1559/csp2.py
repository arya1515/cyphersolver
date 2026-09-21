import re,collections,math,sys
src=open('csp.py').read()
pre,post=src.split("words=[w for k")
exec(pre)
import itertools
for pol in ['strip_dots','strip_under','strip_all','homoph']:
    def norm(t):
        if pol=='strip_dots': return t.rstrip(':.')
        if pol=='strip_under': return t.replace('_','')
        if pol=='strip_all': return t[0]
        return t
    L_=[[norm(t) for t in w] for k in ['1','2','3','4'] for w in lines[k]]
    words=L_
    cands=[sorted(by[pat(w)],key=lambda x:-cnt[x])[:300] for w in words]
    order=sorted(range(len(words)),key=lambda i:len(cands[i]))
    best=[]
    inj = pol!='homoph'
    def rec(k,m,inv,sc,ch):
        if len(best)>50000: return
        if k==len(order): best.append((sc,dict(ch)));return
        i=order[k];w=words[i]
        for c in cands[i]:
            ok=True;add=[]
            for s,l in zip(w,c):
                if s in m:
                    if m[s]!=l: ok=False;break
                elif inj and l in inv: ok=False;break
                else: m[s]=l;inv[l]=s;add.append(s)
            if ok: ch[i]=c;rec(k+1,m,inv,sc+math.log(cnt[c]),ch)
            for s in add: inv.pop(m[s],None);del m[s]
    rec(0,{},{},0,{})
    best.sort(key=lambda x:-x[0])
    print(pol,len(best))
    for sc,ch in best[:8]: print(' ',round(sc,1),' / '.join(ch[i] for i in range(len(words))))
