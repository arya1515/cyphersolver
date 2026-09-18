import pickle, numpy as np, collections
from PIL import Image
from scipy.cluster.hierarchy import fcluster
from seg import binarize
JUNK={20,10,17,13,64,15,14,11,57,58,12,19,51,55,60,63,66,16,65,23,24,27,31}
d=pickle.load(open('f122r_glyphs.pkl','rb')); lab=fcluster(d['Z'],110,'maxclust'); meta=d['meta']; bmps=d['bmps']
bw,_=binarize('full/f122r.jpg',0.14,0.93,800,4250,C=22); B=bw.astype(np.float32)
tpl={}
for k in sorted(set(lab.tolist())):
    if k in JUNK: continue
    idx=[i for i in range(len(meta)) if lab[i]==k]
    if len(idx)<3: continue
    H=int(np.median([bmps[i].shape[0] for i in idx])); W=int(np.median([bmps[i].shape[1] for i in idx]))
    acc=np.zeros((H,W),np.float32)
    for i in idx: acc+=np.asarray(Image.fromarray((bmps[i]*255).astype('uint8')).resize((W,H),Image.BILINEAR),np.float32)/255.
    tpl[k]=acc/len(idx)
def ncc_at(box, T):
    # normalised cross-correlation of template T over patch box (both float), returns map (valid positions)
    H,W=T.shape; h,w=box.shape
    if h<H or w<W: return None
    Tz=T-T.mean(); e=np.sqrt((Tz**2).sum())
    out=np.full((h-H+1,w-W+1),-1.0,np.float32)
    for y in range(h-H+1):
        for x in range(w-W+1):
            p=box[y:y+H,x:x+W]; s=p.sum()
            if s<0.5*T.sum(): continue
            v=s-s*s/(H*W)
            if v<=0: continue
            out[y,x]=((p-p.mean())*Tz).sum()/(np.sqrt(v)*e)
    return out
clean_w=np.median([m['x1']-m['x0'] for i,m in enumerate(meta) if lab[i] not in JUNK])
new=[]
stats=collections.Counter()
for i,m in enumerate(meta):
    k=int(lab[i])
    if k not in JUNK: new.append((m['line'],m['x0'],k,1.0)); continue
    if m['n']<250 or (m['x1']-m['x0'])<0.35*clean_w and m['n']<600: stats['dropped']+=1; continue
    pad=8
    y0=max(0,m['y0']-pad); y1=min(B.shape[0],m['y1']+pad); x0=max(0,m['x0']-pad); x1=min(B.shape[1],m['x1']+pad)
    box=B[y0:y1,x0:x1].copy()
    # candidates
    cands=[]
    for kk,T in tpl.items():
        H,W=T.shape
        if H>box.shape[0]*1.15 or W>box.shape[1]*1.15: continue
        Ts=T
        if H>box.shape[0] or W>box.shape[1]:
            Ts=np.asarray(Image.fromarray((T*255).astype('uint8')).resize((min(W,box.shape[1]),min(H,box.shape[0])),Image.BILINEAR),np.float32)/255.
        mp=ncc_at(box,Ts)
        if mp is None: continue
        j=mp.argmax(); y,x=np.unravel_index(j,mp.shape)
        if mp[y,x]>0.45: cands.append((float(mp[y,x])*np.sqrt(Ts.sum()),float(mp[y,x]),kk,x,y,Ts.shape[1],Ts.shape[0]))
    cands.sort(reverse=True)
    claimed=np.zeros(box.shape,bool); acc=[]
    for adj,s,kk,x,y,W,H in cands:
        sub=box[y:y+H,x:x+W]>0; ink=sub.sum()
        if ink==0 or (claimed[y:y+H,x:x+W]&sub).sum()>0.25*ink: continue
        claimed[y:y+H,x:x+W]|=sub; acc.append((x,kk,s))
        if len(acc)==3: break
    explained=(claimed&(box>0)).sum()/max(1,(box>0).sum())
    if not acc or explained<0.45:
        new.append((m['line'],m['x0'],-1,0.0)); stats['gap']+=1; continue
    acc.sort()
    for x,kk,s in acc: new.append((m['line'],m['x0']+x,kk,s))
    stats['explained_%d'%len(acc)]+=1
new.sort(key=lambda t:(t[0],t[1]))
print(dict(stats),'total glyphs',len(new),'gaps',sum(1 for t in new if t[2]==-1))
pickle.dump(new,open('f122r_local.pkl','wb'))
from lm import ALPHA
from assign95 import CL2L
kk=pickle.load(open('f122r_key.pkl','rb'))['key']
def letter(k): return '.' if k==-1 else (CL2L[k].lower() if k in CL2L else ALPHA[kk[k]])
lines={}
for ln,x,k,s in new: lines.setdefault(ln,[]).append(letter(k))
print('\n'.join('%2d %s'%(ln+1,''.join(w)) for ln,w in sorted(lines.items())))
