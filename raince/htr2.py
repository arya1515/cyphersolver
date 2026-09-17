"""Per-token letter classifier trained on hand labels (gold/labels.txt) plus the
shape-constrained map's own confident tokens, then an LM beam decode.
Reports leave-one-line-out accuracy on the hand-labelled lines, which is the only
honest measure of how good the reading is."""
import json, pickle, collections, sys
import numpy as np

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

idx={(t['page'],t['line'],t['x0']):i for i,t in enumerate(b['tokens'])}
gold={}; goldline=collections.defaultdict(list)
for ln in open('gold/labels.txt'):
    if ln.startswith('#') or not ln.strip(): continue
    p,l,s=ln.split(); L=int(l)-1
    row=sorted([t for t in b['tokens'] if t['page']==p and t['line']==L],key=lambda t:t['x0'])
    assert len(row)==len(s), (p,l,len(row),len(s))
    for t,ch in zip(row,s):
        i=idx[(t['page'],t['line'],t['x0'])]
        if ch not in '?C': gold[i]=ch; goldline[(p,L)].append(i)
        else: goldline[(p,L)].append(None)
print('gold tokens', len(gold), 'over', len(goldline), 'lines')

def fit(train_idx, train_lab, Z, K):
    CLS=sorted(set(train_lab))
    Zt=np.array([Z[i] for i in train_idx]); yt=np.array(train_lab)
    sh=np.cov(Zt.T)*0.35
    out=np.zeros((len(Z),len(CLS)))
    for j,c in enumerate(CLS):
        zz=Zt[yt==c]
        if len(zz)<3: out[:,j]=-1e6; continue
        m=zz.mean(0)
        cv=np.cov(zz.T)*(len(zz)/(len(zz)+30))+sh*(30/(len(zz)+30))+np.eye(K)*1e-3
        ic=np.linalg.inv(cv); _,ld=np.linalg.slogdet(cv); dd=Z-m
        out[:,j]=np.log(len(zz)/len(Zt))-0.5*(np.einsum('ij,jk,ik->i',dd,ic,dd)+ld)
    out-=out.max(1,keepdims=True); out-=np.log(np.exp(out).sum(1,keepdims=True))
    return CLS,out

mu=X.mean(0); Xc=X-mu
base=[i for i,t in enumerate(b['tokens']) if t['cl'] in pure]
U,S,Vt=np.linalg.svd(Xc[base],full_matrices=False)
K=int(sys.argv[2]) if len(sys.argv)>2 else 55
Wp=Vt[:K].T; Z=Xc@Wp

GW=int(sys.argv[1]) if len(sys.argv)>1 else 8
# leave-one-line-out
tot=ok=0
for key,ids in goldline.items():
    hold=set(i for i in ids if i is not None)
    ti=[]; tl=[]
    for i in base:
        if i in hold: continue
        ti.append(i); tl.append(pure[b['tokens'][i]['cl']])
    for i,ch in gold.items():
        if i in hold: continue
        ti+= [i]*GW; tl+= [ch]*GW
    CLS,lpv=fit(ti,tl,Z,K)
    for i in hold:
        tot+=1; ok += (CLS[int(np.argmax(lpv[i]))]==gold[i])
print('LOO per-token accuracy', round(ok/tot,3))

# final model on everything
ti=list(base); tl=[pure[b['tokens'][i]['cl']] for i in base]
for i,ch in gold.items(): ti+=[i]*GW; tl+=[ch]*GW
CLS,lpv=fit(ti,tl,Z,K)
np.save('post.npy',lpv); json.dump(CLS,open('post_cls.json','w'))
print('classes',CLS)
