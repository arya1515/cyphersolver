# Beam decode: P(letter|glyph) from the aligned key counts + manual key, transitions from the French 5-gram table.
# Prints the most likely reading per line with '.' where even the best letter is improbable.
import sys, json, math, collections
import numpy as np
sys.path.insert(0,'../../sp53'); sys.path.insert(0,'hand')
from homo import ALPHA
from key_manual import KEY
K=len(ALPHA); tab=np.load('../../sp53/fr5.npy')
k2=json.load(open('hand/key2.json'))
counts={t:collections.Counter(c) for t,c in k2['key'].items()}
nulls=collections.Counter(k2['nulls'])
HARDNULL={'*','C','mq','j'}
def emis(t):
    # returns list of (letter_index or -1 for null, logprob)
    out={}
    c=counts.get(t,collections.Counter()); nn=nulls.get(t,0); tot=sum(c.values())+nn
    man=KEY.get(t,'')
    pri=collections.Counter()
    for i,ch in enumerate([x for x in man.split('/') if x and x!='?']): pri[ch]+=3.0/(i+1)
    allc=collections.Counter()
    for ch,v in c.items(): allc[ch]+=v
    for ch,v in pri.items(): allc[ch]+=v
    S=sum(allc.values())+nn+0.5*K
    for ch,v in allc.items():
        if ch in ALPHA: out[ALPHA.index(ch)]=math.log((v+0.02)/S)
    # small floor for every letter
    for i in range(K): out.setdefault(i,math.log(0.5/S))
    res=[(i,lp) for i,lp in out.items()]
    if t in HARDNULL: res.append((-1,math.log(0.95)))
    elif nn>0: res.append((-1,math.log((nn+0.1)/S)))
    else: res.append((-1,math.log(0.02/S)))
    return res
def beam_line(toks,W=300):
    beams={(23,23,23,23):(0.0,'')}  # start context 'z'*4 ~ neutral; use 'e'? pick index of 'e'
    e=ALPHA.index('e'); beams={(e,e,e,e):(0.0,'')}
    for t in toks:
        E=emis(t); nb={}
        for ctx,(sc,txt) in beams.items():
            for li,lp in E:
                if li==-1:
                    ns=sc+lp; k=ctx
                    if k not in nb or nb[k][0]<ns: 
                        if k not in nb or nb[k][0]<ns: nb[k]=(max(nb.get(k,(-1e18,''))[0],ns),txt+'·') if False else (ns,txt+'·')
                    continue
                tr=tab[ctx[0],ctx[1],ctx[2],ctx[3],li]
                ns=sc+lp+tr; k=(ctx[1],ctx[2],ctx[3],li)
                if k not in nb or nb[k][0]<ns: nb[k]=(ns,txt+ALPHA[li])
        beams=dict(sorted(nb.items(),key=lambda kv:-kv[1][0])[:W])
    return max(beams.values(),key=lambda v:v[0])
for f in sys.argv[1:]:
    for l in open(f,encoding='utf-8'):
        if ':' not in l or l.startswith('#'): continue
        lab,rest=l.split(':',1); toks=rest.split()
        sc,txt=beam_line(toks)
        print('%4s %7.1f  %s'%(lab.strip(),sc/max(1,len(toks)),txt))
