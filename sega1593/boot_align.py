# Bootstrap glyph classifier from line-3 labels + known plaintext alignment (f.188v <-> f.185).
import json, re, sys, numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
PAIRS=['an','bo','cp','dq','er','fs','gt','hu','ix','ly','mz']; NULL=11; CODE=12; NCL=13
X=np.load('sega1593/lines/joint5_feats.npy'); meta=json.load(open('sega1593/lines/joint5_meta.json'))
idx={}
for i,(pre,k,j) in enumerate(meta): idx.setdefault(pre,{}).setdefault(k,[]).append(i)
V='sega1593/lines/f188v'
read={0:'hu',1:'bo',2:'bo',4:'hu',5:'ly',6:'hu',7:'bo',8:'null',9:'cp',10:'bo',11:'fs',12:'fs',13:'er',14:'er',15:'an',16:'ly',17:'an',18:'gt',21:'er',22:'er',25:'ly',26:'er',27:'fs',28:'er',29:'fs',30:'cp',31:'an',32:'gt',33:'gt',34:'an',35:'an',36:'bo',37:'null',39:'ly',40:'mz',41:'er',42:'an',43:'an',44:'ly',45:'an',46:'cp',47:'er',48:'bo',49:'bo',50:'cp',51:'bo',52:'bo',53:'fs',54:'ix',55:'gt',56:'ix',57:'null',58:'bo',59:'null',60:'an',61:'code',62:'ly',63:'mz',64:'bo',65:'an',66:'gt',67:'fs',68:'an',69:'ix',70:'gt',71:'er',72:'dq',73:'er'}
def cls_of(s): return NULL if s=='null' else CODE if s=='code' else PAIRS.index(s)
labels={}
for j,s in read.items(): labels[idx[V][3][j]]=cls_of(s)
# plaintext class sequence
pt=open('sega1593/f185_plain.txt',encoding='utf-8').read().lower()
pt=re.sub(r'[^a-z# ]','',pt).replace(' ','')
def letter_cls(ch):
    if ch=='#': return CODE
    ch=ch.replace('j','i').replace('v','u').replace('w','u').replace('k','c')
    for i,p in enumerate(PAIRS):
        if ch in p: return i
    return None
# handle que/qui/pour as CODE tokens
pt2=[]; i=0
words=re.sub(r'[^a-z# ]','',open('sega1593/f185_plain.txt',encoding='utf-8').read().lower()).split()
for w in words:
    if w in ('que','qui','pour'): pt2.append(CODE); continue
    if w.startswith('qu') and w not in ('que','qui'):  # quilz -> qui + lz
        pt2.append(CODE); w=w[3:] if w.startswith('qui') else w[2:]
    for ch in w:
        c=letter_cls(ch)
        if c is not None: pt2.append(c)
P=np.array(pt2); print('plaintext classes',len(P))
# cipher tokens: f188v lines 3..21
lines=list(range(3,22)); toks=[]
for k in lines: toks+=idx[V][k]
T=np.array(toks); print('tokens',len(T))
sc=StandardScaler().fit(X)
Xs=sc.transform(X)
def train_predict(labels):
    ii=np.array(list(labels.keys())); yy=np.array([labels[i] for i in ii])
    knn=KNeighborsClassifier(n_neighbors=7,weights='distance').fit(Xs[ii],yy)
    pr=np.zeros((len(Xs),NCL))+1e-3
    p=knn.predict_proba(Xs); pr[:,knn.classes_]+=p
    pr/=pr.sum(1,keepdims=True)
    return pr
def align(pr):
    # DP: tokens vs plaintext; states (t,p); moves: match (t+1,p+1) score log pr[t,P[p]]; ins token (t+1,p) log 0.10 (token null/junk: use max(pr[t,NULL],0.1));
    # del letter (t,p+1) log 0.05
    n=len(T); m=len(P); NEG=-1e18
    D=np.full((n+1,m+1),NEG); B=np.zeros((n+1,m+1),np.int8); D[0,0]=0
    lpr=np.log(pr[T]+1e-9); lins=np.log(0.10); ldel=np.log(0.05)
    for t in range(n+1):
        for p in range(m+1):
            if t==0 and p==0: continue
            best=NEG; bb=0
            if t>0 and p>0:
                v=D[t-1,p-1]+lpr[t-1,P[p-1]]
                if v>best: best=v; bb=1
            if t>0:
                v=D[t-1,p]+max(lins,lpr[t-1,NULL])
                if v>best: best=v; bb=2
            if p>0:
                v=D[t,p-1]+ldel
                if v>best: best=v; bb=3
            D[t,p]=best; B[t,p]=bb
    t,p=n,m; pairs=[]
    while t>0 or p>0:
        b=B[t,p]
        if b==1: pairs.append((T[t-1],P[p-1])); t-=1; p-=1
        elif b==2: pairs.append((T[t-1],NULL)); t-=1
        else: p-=1
    return pairs[::-1], D[n,m]
for it in range(5):
    pr=train_predict(labels)
    pairs,score=align(pr)
    new={}
    for tok,c in pairs:
        if pr[tok,c]>0.25 or tok in labels: new[tok]=labels.get(tok,c)
    # accuracy on line 3 (compare alignment-derived class vs my labels)
    l3=idx[V][3]; agree=sum(1 for tok,c in pairs if tok in read_idx) if False else None
    d3={tok:c for tok,c in pairs if tok in set(l3)}
    acc=np.mean([d3.get(idx[V][3][j],-1)==cls_of(s) for j,s in read.items()])
    print(f'iter {it} score {score:.0f} labelled {len(new)} line3-agreement {acc:.2f}',flush=True)
    labels=new
pr=train_predict(labels)
np.save('sega1593/lines/joint5_classprob.npy',pr)
json.dump({str(k):int(v) for k,v in labels.items()},open('sega1593/lines/f188v_boot_labels.json','w'))
# print aligned decode of lines 4-6 as class-letter guesses
names=PAIRS+['.','#']
pairs,_=align(pr); d={tok:c for tok,c in pairs}
for k in (4,5,6):
    print(k,' '.join(names[d.get(i,NULL)] for i in idx[V][k]))
