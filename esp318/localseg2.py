import pickle, numpy as np, collections
from PIL import Image
from scipy.cluster.hierarchy import fcluster
from seg import binarize
def corr(B,K):
    H,W=B.shape; h,w=K.shape; fh,fw=H+h-1,W+w-1
    full=np.fft.irfft2(np.fft.rfft2(B,s=(fh,fw))*np.fft.rfft2(K[::-1,::-1],s=(fh,fw)),s=(fh,fw))
    return full[h-1:H,w-1:W].astype(np.float32)   # 'valid' positions: top-left anchored
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
def explain(box, maxk=3):
    h,w=box.shape; cands=[]
    for k,T in tpl.items():
        H,W=T.shape
        if H>h or W>w:
            if H>1.2*h or W>1.2*w: continue
            T=np.asarray(Image.fromarray((T*255).astype('uint8')).resize((min(W,w),min(H,h)),Image.BILINEAR),np.float32)/255.; H,W=T.shape
        Tz=T-T.mean(); e=np.sqrt((Tz**2).sum())
        if e==0: continue
        s1=corr(box,np.ones((H,W),np.float32)); num=corr(box,Tz)
        var=np.maximum(s1-s1*s1/(H*W),1e-3); ncc=num/(np.sqrt(var)*e)
        ncc[s1<0.5*T.sum()]=-1
        j=ncc.argmax(); y,x=np.unravel_index(j,ncc.shape)
        if ncc[y,x]>0.45: cands.append((float(ncc[y,x])*np.sqrt(T.sum()),float(ncc[y,x]),k,int(x),int(y),W,H))
    cands.sort(reverse=True); claimed=np.zeros(box.shape,bool); acc=[]
    for adj,s,k,x,y,W,H in cands:
        sub=box[y:y+H,x:x+W]>0; ink=sub.sum()
        if ink==0 or (claimed[y:y+H,x:x+W]&sub).sum()>0.25*ink: continue
        claimed[y:y+H,x:x+W]|=sub; acc.append((x,k,s))
        if len(acc)==maxk: break
    return sorted(acc),(claimed&(box>0)).sum()/max(1,(box>0).sum())
clean_w=np.median([m['x1']-m['x0'] for i,m in enumerate(meta) if lab[i] not in JUNK])
new=[]; stats=collections.Counter()
for i,m in enumerate(meta):
    k=int(lab[i])
    if k not in JUNK: new.append((m['line'],m['x0'],k,1.0)); continue
    if m['n']<250 or ((m['x1']-m['x0'])<0.35*clean_w and m['n']<600): stats['dropped']+=1; continue
    pad=8; y0=max(0,m['y0']-pad); y1=min(B.shape[0],m['y1']+pad); x0=max(0,m['x0']-pad); x1=min(B.shape[1],m['x1']+pad)
    acc,expl=explain(B[y0:y1,x0:x1].copy())
    if not acc or expl<0.45: new.append((m['line'],m['x0'],-1,0.0)); stats['gap']+=1; continue
    for x,kk,s in acc: new.append((m['line'],x0+x,kk,s))
    stats['explained_%d'%len(acc)]+=1
new.sort(key=lambda t:(t[0],t[1]))
print(dict(stats),'total',len(new),'gaps',sum(1 for t in new if t[2]==-1))
pickle.dump(new,open('f122r_local.pkl','wb'))
from lm import ALPHA
from assign95 import CL2L
kk=pickle.load(open('f122r_key.pkl','rb'))['key']
def letter(k): return '.' if k==-1 else (CL2L[k].lower() if k in CL2L else ALPHA[kk[k]])
lines={}
for ln,x,k,s in new: lines.setdefault(ln,[]).append(letter(k))
print('\n'.join('%2d %s'%(ln+1,''.join(w)) for ln,w in sorted(lines.items())))
