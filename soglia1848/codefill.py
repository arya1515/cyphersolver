import json,re,collections,numpy as np,sys
from lmscore import LM
from lm import enc
L=LM('lm5sp.npy')
key=json.load(open('key.json'))
s=open('ct2.txt').read().strip()
s=s.replace('519090599098446675','51909049909844667 5'.replace(' ',''),1) if False else s
# fix passaporti misprint: 19 09 0 5 99 -> 19 09 04 99
s=s.replace('5190905990984466','5190904990984466',1)
toks=[]
for r in s.split('5'):
    i=0
    while i<len(r):
        if r[i]=='8' and i+4<=len(r): toks.append(('C',r[i:i+4])); i+=4
        elif i+2<=len(r): toks.append(('D',r[i:i+2])); i+=2
        else: toks.append(('P',r[i])); i+=1
    toks.append(('S',' '))
anchors={c:v.strip('[]').lower() for c,v in key.items() if c.startswith('8')}
words=collections.Counter(open('it19.txt').read().split())
vocab=[w for w,c in words.items() if c>=8 and len(w)>=2]
vocab.sort()
codes=sorted(set(v for t,v in toks if t=='C'))
unk=[c for c in codes if c not in anchors]
sa=sorted(anchors.items())
def interval(c):
    lo='a';hi='zzzz'
    for k,v in sa:
        if k<c: lo=v
        if k>c: hi=v;break
    return lo,hi
cur={c:anchors.get(c) for c in codes}
cands={}
for c in unk:
    lo,hi=interval(c)
    cs=[w for w in vocab if lo<w<hi]
    cands[c]=cs
    print(c,lo,hi,len(cs))
def render(assign):
    out=[]
    for t,v in toks:
        if t=='S': out.append(' ')
        elif t=='P': out.append(' ')
        elif t=='D': out.append(key.get(v,'?'))
        else:
            w=assign.get(v)
            out.append(' '+w+' ' if w else ' ')
    x=re.sub(' +',' ',''.join(out))
    return x
def ctx_score(assign,c):
    txt=render(assign)
    return L.score(enc(re.sub('[^a-z ]','',txt)))
json.dump({'codes':codes,'unk':unk},open('codes.json','w'))
if len(sys.argv)>1:
    for rnd in range(2):
        for c in unk:
            best=None
            for w in cands[c]:
                a=dict(cur); a[c]=w
                sc=ctx_score(a,c)
                if best is None or sc>best[0]: best=(sc,w)
            # also top-5
            cur[c]=best[1]
            print(rnd,c,best,flush=True)
    print(render(cur))
    json.dump(cur,open('codefill.json','w'))
