import re,collections,math,sys
src=open('csp.py').read(); pre=src.split("words=[w for k")[0]; exec(pre)
words=[w for k in '1234' for w in lines[k]]
cands=[sorted(by[pat(w)],key=lambda x:-cnt[x])[:40] for w in words]
order=sorted(range(len(words)),key=lambda i:len(cands[i]))
best=[];MAXSKIP=int(sys.argv[1])
def rec(k,m,inv,sc,ch,sk):
    if k==len(order):
        best.append((len(words)-sk,sc,dict(ch)));return
    i=order[k];w=words[i]
    for c in cands[i]:
        ok=True;add=[]
        for s,l in zip(w,c):
            if s in m:
                if m[s]!=l: ok=False;break
            elif l in inv: ok=False;break
            else: m[s]=l;inv[l]=s;add.append(s)
        if ok: ch[i]=c;rec(k+1,m,inv,sc+math.log(cnt[c]),ch,sk)
        for s in add: del inv[m[s]];del m[s]
        if len(best)>100000: return
    if sk<MAXSKIP: ch[i]='?'*len(w);rec(k+1,m,inv,sc-3,ch,sk+1)
rec(0,{},{},0,{},0)
best.sort(key=lambda x:(-x[0],-x[1]))
for n,sc,ch in best[:25]: print(n,round(sc,1),' / '.join(ch[i] for i in range(len(words))))
