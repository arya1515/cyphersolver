# Beam decode with word-space LM; '/' gaps in the transcription favour a word space before the next token.
# usage: python decode_sp.py file.txt [W] [PGAP] [PIN]
import sys, json, math, collections, os
import numpy as np
A='abcdefghiklmnopqrstuvxyz'; SP=24
tab=np.load('fr5sp.npy')
k=json.load(open(os.environ.get('KEY','key1573.json')))
counts={t:collections.Counter(c) for t,c in k['counts'].items()}; nulls=collections.Counter(k['nulls'])
W=int(sys.argv[2]) if len(sys.argv)>2 else 400
PGAP=float(sys.argv[3]) if len(sys.argv)>3 else 0.75
PIN=float(sys.argv[4]) if len(sys.argv)>4 else 0.12
def emis(t):
    c=counts.get(t,collections.Counter()); nn=nulls.get(t,0); S=sum(c.values())+nn+0.3*24
    res=[(A.index(ch),math.log((v+0.3)/S)) for ch,v in c.items() if ch in A]
    seen={i for i,_ in res}; res+=[(i,math.log(0.3/S)) for i in range(24) if i not in seen]
    res.append((-1,math.log((nn+0.2)/S)-1.0)); return res
def step(beams,t,gap,nb):
    E=emis(t)
    ps=[(True,math.log(PGAP if gap else PIN)),(False,math.log(1-(PGAP if gap else PIN)))]
    for ctx,(sc,txt) in beams.items():
        for li,lp in E:
            if li==-1:
                kk=ctx; ns=sc+lp
                if kk not in nb or nb[kk][0]<ns: nb[kk]=(ns,txt+'·')
                continue
            for sp,lsp in ps:
                c=ctx; s=sc+lp+lsp; tx=txt
                if sp and c[3]!=SP:
                    s+=tab[c]+0 if False else tab[c[0],c[1],c[2],c[3],SP]; c=(c[1],c[2],c[3],SP); tx+=' '
                elif sp: continue
                s+=tab[c[0],c[1],c[2],c[3],li]; c2=(c[1],c[2],c[3],li)
                if c2 not in nb or nb[c2][0]<s: nb[c2]=(s,tx+A[li])
lines=[]
for l in open(sys.argv[1],encoding='utf-8'):
    if l.startswith('#') or ':' not in l: continue
    lab,rest=l.split(':',1); toks=[]; g=True
    for t in rest.split():
        if t=='/': g=True; continue
        if t=='.': continue
        toks.append((t,g)); g=False
    lines.append((lab.strip(),toks))
beams={(SP,SP,SP,SP):(0.0,'')}
for lab,toks in lines:
    start={k:(v[0],'') for k,v in beams.items()}
    beams=start
    for t,g in toks:
        if t.startswith('['):
            w=t.strip('[]').replace('v','u').replace('j','i')
            nb={}
            for ctx,(sc,txt) in beams.items():
                c=ctx
                for ch in ' '+w:
                    i=SP if ch==' ' else A.index(ch)
                    if not(i==SP and c[3]==SP): sc+=tab[c[0],c[1],c[2],c[3],i]; c=(c[1],c[2],c[3],i)
                if c not in nb or nb[c][0]<sc: nb[c]=(sc,txt+' ['+w+']')
            beams=nb; continue
        nb={}; step(beams,t,g,nb)
        beams=dict(sorted(nb.items(),key=lambda kv:-kv[1][0])[:W])
    best=max(beams.values(),key=lambda v:v[0])
    print('%3s  %s'%(lab,best[1].strip()),flush=True)
