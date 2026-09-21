import re, collections, math
exec(open('pattern_search.py').read().split("txt=")[0])
txt=open('../burghley1559/sadler1.txt',encoding='utf-8',errors='ignore').read()+open('../throckmorton/sources/forbes1.txt',encoding='utf-8',errors='ignore').read().replace('ſ','s')
cnt=collections.Counter(re.findall(r'[a-z]+',txt.lower()))
for n in "knox knoxe prior lord laird lairde whitlaw whitlawe kirkaldy grange james hume dowager congregation croftes merse tivdale lordes".split(): cnt[n]+=200
vocab=[w for w,c in cnt.items() if c>=4]
def pat(ws): m={};return tuple(m.setdefault(s,len(m)) for s in ws)
by=collections.defaultdict(list)
for w in vocab: by[pat(w)].append(w)
words=[w[::-1] for k in "1234" for w in lines[k]]
cands=[sorted(by[pat(w)],key=lambda x:-cnt[x])[:400] for w in words]
order=sorted(range(len(words)),key=lambda i:len(cands[i]))
best=[]
def rec(k,m,inv,sc,ch):
    if k==len(order):
        best.append((sc,dict(ch)));return
    i=order[k];w=words[i]
    n=0
    for c in cands[i]:
        ok=True;add=[]
        for s,l in zip(w,c):
            if s in m:
                if m[s]!=l: ok=False;break
            elif l in inv and inv[l]!=s: ok=False;break
            elif s not in m: m[s]=l;inv[l]=s;add.append(s)
        if ok:
            ch[i]=c; rec(k+1,m,inv,sc+math.log(cnt[c]),ch); n+=1
        for s in add: del inv[m[s]];del m[s]
        if len(best)>200000: return
rec(0,{},{},0,{})
best.sort(key=lambda x:-x[0])
seen=set()
for sc,ch in best[:30]:
    print(round(sc,1),' / '.join(ch[i] for i in range(len(words))))
print(len(best))
