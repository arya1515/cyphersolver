import pickle, numpy as np, collections, math, sys
from PIL import Image
from scipy.cluster.hierarchy import fcluster
from seg import binarize
from lm import ALPHA, IDX
from assign95 import CL2L
L=len(ALPHA)
def corr(B,K):
    H,W=B.shape; h,w=K.shape; fh,fw=H+h-1,W+w-1
    full=np.fft.irfft2(np.fft.rfft2(B,s=(fh,fw))*np.fft.rfft2(K[::-1,::-1],s=(fh,fw)),s=(fh,fw))
    return full[h-1:H,w-1:W].astype(np.float32)
JUNK={20,10,17,13,64,15,14,11,57,58,12,19,51,55,60,63,66,16,65,23,24,27,31}
d=pickle.load(open('f122r_glyphs.pkl','rb')); lab=fcluster(d['Z'],110,'maxclust'); meta=d['meta']; bmps=d['bmps']
bw,_=binarize('full/f122r.jpg',0.14,0.93,800,4250,C=22); B=bw.astype(np.float32)
# templates per (cluster) with letter label; only labelled clusters
tpl={}
for k in sorted(set(lab.tolist())):
    if k in JUNK or k not in CL2L: continue
    idx=[i for i in range(len(meta)) if lab[i]==k]
    if len(idx)<3: continue
    H=int(np.median([bmps[i].shape[0] for i in idx])); W=int(np.median([bmps[i].shape[1] for i in idx]))
    acc=np.zeros((H,W),np.float32)
    for i in idx: acc+=np.asarray(Image.fromarray((bmps[i]*255).astype('uint8')).resize((W,H),Image.BILINEAR),np.float32)/255.
    tpl[k]=(acc/len(idx), CL2L[k].lower())
print('templates',len(tpl),'letters',sorted(set(v[1] for v in tpl.values())))
def emis(box):
    """best NCC per letter over templates, anywhere in box (box may be bigger than template)"""
    h,w=box.shape; best=collections.defaultdict(lambda:-1.0)
    for k,(T,let) in tpl.items():
        H,W=T.shape
        if H>h*1.25 or W>w*1.25: continue
        if H>h or W>w:
            T=np.asarray(Image.fromarray((T*255).astype('uint8')).resize((min(W,w),min(H,h)),Image.BILINEAR),np.float32)/255.; H,W=T.shape
        Tz=T-T.mean(); e=np.sqrt((Tz**2).sum())
        if e==0: continue
        s1=corr(box,np.ones((H,W),np.float32)); var=np.maximum(s1-s1*s1/(H*W),1e-3)
        ncc=corr(box,Tz)/(np.sqrt(var)*e); ncc[s1<0.45*T.sum()]=-1
        v=float(ncc.max())
        if v>best[let]: best[let]=v
    return best
medw=np.median([m['x1']-m['x0'] for i,m in enumerate(meta) if lab[i] not in JUNK])
units=[]  # (line, x, emission-vector over ALPHA, isgap)
for i,m in enumerate(meta):
    if m['n']<200: continue
    y0=max(0,m['y0']-6); y1=min(B.shape[0],m['y1']+6); x0=max(0,m['x0']-6); x1=min(B.shape[1],m['x1']+6)
    box=B[y0:y1,x0:x1]
    nparts=1 if (m['x1']-m['x0'])<1.6*medw else (2 if (m['x1']-m['x0'])<2.6*medw else 3)
    w=box.shape[1]
    for p in range(nparts):
        sub=box[:, int(w*p/nparts):int(w*(p+1)/nparts)]
        e=emis(sub); vec=np.full(L,-1.0)
        for let,v in e.items(): vec[IDX[let]]=v
        units.append((m['line'], m['x0']+int(w*p/nparts), vec))
units.sort(key=lambda t:(t[0],t[1]))
pickle.dump(units,open('f122r_units.pkl','wb'))
print('units',len(units))
