"""Joint letter-choice and word-segmentation decode.

Beam search over the token stream. A state carries a node of a period-French lexicon trie
(the word being built) plus the character-LM context. At each token the decoder picks a letter
from the classifier's top candidates, advancing the trie; whenever the current node is a word
end it may close the word and restart at the root, paying the word's unigram log-probability.
Out-of-vocabulary stretches are allowed through a separate 'free' mode at a per-letter penalty,
so the decode is not forced to invent vocabulary it does not have (names, numbers, abbreviations).
"""
import json, pickle, collections, math, re, glob, unicodedata, sys
import numpy as np

# ---------- lexicon ----------
def norm(t):
    t=unicodedata.normalize('NFD',t); t=''.join(c for c in t if unicodedata.category(c)!='Mn')
    t=t.lower().replace('j','i').replace('v','u').replace('w','u')
    return re.sub(r"[^a-z]+",' ',t)
cnt=collections.Counter()
for f in glob.glob('../dubellay/ref/legrand3_*.txt')+glob.glob('../nevers1593/*.txt')+glob.glob('../debosnys/corpus/fr*.txt'):
    try: cnt.update(norm(open(f,encoding='utf-8',errors='ignore').read()).split())
    except Exception: pass
NT=sum(cnt.values())
WORDS={w:math.log(c/NT) for w,c in cnt.items() if c>=4 and len(w)<=15}
# trie as dict of dicts; key '' holds the word logprob at a terminal
trie={}
for w,lp in WORDS.items():
    n=trie
    for ch in w: n=n.setdefault(ch,{})
    n['$']=lp
print('lexicon', len(WORDS))

# ---------- classifier posteriors (same as htr.py) ----------
X=np.load('feats.npy').astype(np.float64)
a=json.load(open('raince_tokens.json')); b=json.load(open('raince140_tokens.json'))
MAP={int(k):v for k,v in json.load(open('map140.json')).items()}
ALLOW70={1:'a',2:'a',3:'b',4:'adl',5:'adl',6:'q',7:'c',8:'c',9:'ca',10:'su',11:'s',12:'su',13:'sui',
 14:'t',15:'t',16:'t',17:'u',18:'tl',19:'tl',20:'aoy',21:'u',22:'u',23:'u',24:'hu',25:'pme',
 26:'e',27:'e',28:'n',29:'e',30:'eng',31:'e',32:'_',33:'mi',34:'tl',35:'tl',36:'d',37:'i',
 38:'er',39:'ne',40:'e',41:'d',42:'n',43:'pml',44:'y',45:'m',46:'tor',47:'f',48:'i',49:'mi',
 50:'r',51:'r',52:'zr',53:'e',54:'l',55:'e',56:'e',57:'i',58:'p',59:'p',60:'s',61:'s',62:'s',
 63:'o',64:'o',65:'oa',66:'s',67:'_',68:'dl',69:'i',70:'i'}
pair=collections.defaultdict(collections.Counter)
for t70,t140 in zip(a['tokens'],b['tokens']): pair[t140['cl']][t70['cl']]+=1
pure={}
for c140,c in pair.items():
    c70,k=c.most_common(1)[0]
    if k>=0.85*sum(c.values()) and len(ALLOW70[c70])<=2: pure[c140]=MAP[c140]
y=np.array([pure.get(t['cl'],'?') for t in b['tokens']]); tr=y!='?'
CLS=sorted(set(y[tr]))
mu=X.mean(0); Xc=X-mu
U,S,Vt=np.linalg.svd(Xc[tr],full_matrices=False); K=55; W=Vt[:K].T; Z=Xc@W
Zt,yt=Z[tr],y[tr]; sh=np.cov(Zt.T)*0.35
lp=np.zeros((len(Z),len(CLS)))
for j,c in enumerate(CLS):
    zz=Zt[yt==c]; m=zz.mean(0)
    cv=np.cov(zz.T)*(len(zz)/(len(zz)+30))+sh*(30/(len(zz)+30))+np.eye(K)*1e-3
    ic=np.linalg.inv(cv); _,ld=np.linalg.slogdet(cv); d=Z-m
    lp[:,j]=np.log(len(zz)/len(Zt))-0.5*(np.einsum('ij,jk,ik->i',d,ic,d)+ld)
lp-=lp.max(1,keepdims=True); lp-=np.log(np.exp(lp).sum(1,keepdims=True))
print('train acc', round(float((np.array(CLS)[lp[tr].argmax(1)]==yt).mean()),3))

CLW=float(sys.argv[1]) if len(sys.argv)>1 else 1.0
OOV=float(sys.argv[2]) if len(sys.argv)>2 else -3.6   # per-letter penalty inside an OOV run
BEAM=int(sys.argv[3]) if len(sys.argv)>3 else 2500
TOPK=6
NULLI=CLS.index('_')

order={(t['page'],t['line'],t['x0']):i for i,t in enumerate(b['tokens'])}
out=[]
for page in b['regions']:
    rows=[sorted([x for x in b['tokens'] if x['page']==page and x['line']==k],key=lambda x:x['x0'])
          for k in range(len(b['regions'][page]['lines']))]
    stream=[order[(t['page'],t['line'],t['x0'])] for r in rows for t in r]
    # state key: (id(node) or 'F', ) ; keep best per (node,) with its path
    start=(id(trie),0)
    nodes={id(trie):trie}
    beams={(id(trie),0):(0.0,())}          # (node id, oovlen) -> (score, path)
    for i in stream:
        v=lp[i]; cand=np.argsort(-v)[:TOPK]
        nb={}
        for (nid,oov),(sc,path) in beams.items():
            node=nodes[nid]
            for j in cand:
                ch=CLS[j]; e=CLW*float(v[j])
                if ch=='_':
                    k2=(nid,oov); s=sc+e; p=path+('',)
                    if k2 not in nb or nb[k2][0]<s: nb[k2]=(s,p)
                    continue
                # (1) continue the current word inside the lexicon
                if oov==0 and ch in node:
                    ch_node=node[ch]; nodes[id(ch_node)]=ch_node
                    k2=(id(ch_node),0); s=sc+e
                    if k2 not in nb or nb[k2][0]<s: nb[k2]=(s,path+(ch,))
                # (2) close the current word (if terminal or OOV) and start a new one
                base=None
                if oov==0 and '$' in node: base=sc+node['$']
                elif oov>0: base=sc+oov*OOV
                if base is not None:
                    if ch in trie:
                        ch_node=trie[ch]; nodes[id(ch_node)]=ch_node
                        k2=(id(ch_node),0); s=base+e
                        if k2 not in nb or nb[k2][0]<s: nb[k2]=(s,path+(ch,))
                    k2=(id(trie),1); s=base+e            # start an OOV run
                    if k2 not in nb or nb[k2][0]<s: nb[k2]=(s,path+(ch,))
                # (3) continue an OOV run
                if oov>0:
                    k2=(id(trie),oov+1); s=sc+e
                    if k2 not in nb or nb[k2][0]<s: nb[k2]=(s,path+(ch,))
        beams=dict(sorted(nb.items(),key=lambda kv:-kv[1][0])[:BEAM])
    best=max(((k,v) for k,v in beams.items()), key=lambda kv: kv[1][0]+ (nodes[kv[0][0]].get('$',0.0) if kv[0][1]==0 else kv[0][1]*OOV))
    sc,path=best[1]
    out.append('## '+page); j=0
    for k,r in enumerate(rows):
        out.append(f'{k+1:02d} '+''.join(path[j+i] for i in range(len(r)))); j+=len(r)
    print(page, round(sc,1))
open('draft8.txt','w').write('\n'.join(out)+'\n')
