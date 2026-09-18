# Beam decode of 1573 transcriptions: P(letter|glyph) from key1573.json (aligned counts), French 5-gram transitions.
# usage: python decode1573.py file.txt [W]
import sys, json, math, collections, os
import numpy as np
HERE=os.path.dirname(os.path.abspath(__file__))
ALPHA='abcdefghiklmnopqrstuvxyz'

K=len(ALPHA); tab=np.load(os.path.join(HERE,'fr5.npy'))
k=json.load(open(os.path.join(HERE,os.environ.get('KEY','key1573.json'))))
counts={t:collections.Counter(c) for t,c in k['counts'].items()}; nulls=collections.Counter(k['nulls'])
SM=float(os.environ.get('SM','0.3')); NP=float(os.environ.get('NP','1.0'))
def emis(t):
    c=counts.get(t,collections.Counter()); nn=nulls.get(t,0)
    S=sum(c.values())+nn+SM*K
    res=[(ALPHA.index(ch),math.log((v+SM)/S)) for ch,v in c.items() if ch in ALPHA]
    seen={i for i,_ in res}
    res+=[(i,math.log(SM/S)) for i in range(K) if i not in seen]
    res.append((-1,math.log((nn+0.2)/S)))
    return res
def beam(toks,W):
    e=ALPHA.index('e'); beams={(e,e,e,e):(0.0,'')}
    for t in toks:
        if t.startswith('['):
            beams={ctx:(sc,txt+t) for ctx,(sc,txt) in beams.items()}; continue
        E=emis(t); nb={}
        for ctx,(sc,txt) in beams.items():
            for li,lp in E:
                if li==-1:
                    ns=sc+lp-NP; kk=ctx; ch='·'
                else:
                    ns=sc+lp+tab[ctx[0],ctx[1],ctx[2],ctx[3],li]; kk=(ctx[1],ctx[2],ctx[3],li); ch=ALPHA[li]
                if kk not in nb or nb[kk][0]<ns: nb[kk]=(ns,txt+ch)
        beams=dict(sorted(nb.items(),key=lambda kv:-kv[1][0])[:W])
    return max(beams.values(),key=lambda v:v[0])
W=int(sys.argv[2]) if len(sys.argv)>2 else 200
lines=[]
for l in open(sys.argv[1],encoding='utf-8'):
    if l.startswith('#') or ':' not in l: continue
    lab,rest=l.split(':',1); lines.append((lab.strip(),[t for t in rest.split() if t not in('/','.')]))
# decode whole text as one stream (context carries across lines), then split back per line
allt=[t for _,ts in lines for t in ts]
sc,txt=beam(allt,W)
# split txt back: each token yields exactly one char, except [clear] tokens
i=0
for lab,ts in lines:
    out=''
    for t in ts:
        if t.startswith('['):
            j=txt.index(']',i)+1; out+=txt[i:j]; i=j
        else: out+=txt[i]; i+=1
    print('%3s  %s'%(lab,out))
