import pickle, numpy as np, sys, collections
from PIL import Image
from scipy.ndimage import maximum_filter
from scipy.cluster.hierarchy import fcluster
from seg import binarize
def corr(B,K):
    H,W=B.shape; h,w=K.shape; fh,fw=H+h-1,W+w-1
    full=np.fft.irfft2(np.fft.rfft2(B,s=(fh,fw))*np.fft.rfft2(K[::-1,::-1],s=(fh,fw)),s=(fh,fw))
    return full[(h-1)//2:(h-1)//2+H,(w-1)//2:(w-1)//2+W].astype(np.float32)
JUNK={20,10,17,13,64,15,14,11,57,58,12,19,51,55,60,63,66,16,65,23,24,27,31}
d=pickle.load(open('f122r_glyphs.pkl','rb')); lab=fcluster(d['Z'],110,'maxclust'); meta=d['meta']; bmps=d['bmps']
bwR,_=binarize('full/f122r.jpg',0.14,0.93,800,4250,C=22); BR=bwR.astype(np.float32)
tpl={}; thr={}; inkmin={}
for k in sorted(set(lab.tolist())):
    if k in JUNK: continue
    idx=[i for i in range(len(meta)) if lab[i]==k]
    if len(idx)<3: continue
    H=int(np.median([bmps[i].shape[0] for i in idx])); W=int(np.median([bmps[i].shape[1] for i in idx]))
    acc=np.zeros((H,W),np.float32)
    for i in idx: acc+=np.asarray(Image.fromarray((bmps[i]*255).astype('uint8')).resize((W,H),Image.BILINEAR),np.float32)/255.
    T=acc/len(idx); Tz=T-T.mean(); e=np.sqrt((Tz**2).sum())
    ncc=corr(BR,Tz)/(np.sqrt(np.maximum(corr(BR,np.ones((H,W),np.float32))-corr(BR,np.ones((H,W),np.float32))**2/(H*W),1e-3))*e)
    selfs=[ncc[min(bwR.shape[0]-1,(m['y0']+m['y1'])//2), min(bwR.shape[1]-1,(m['x0']+m['x1'])//2)] for m in (meta[i] for i in idx)]
    thr[k]=max(0.40, float(np.percentile(selfs,15))-0.04); inkmin[k]=0.55*T.sum(); tpl[k]=T
print('templates',len(tpl),'thr range',round(min(thr.values()),2),round(max(thr.values()),2))
def detect(bw,pitch,first_top,xmin=0):
    B=bw.astype(np.float32); H0,W0=B.shape
    dets=[]
    for k,T in tpl.items():
        H,W=T.shape; Tz=T-T.mean(); e=np.sqrt((Tz**2).sum())
        s1=corr(B,np.ones((H,W),np.float32)); var=np.maximum(s1-s1*s1/(H*W),1e-3)
        ncc=corr(B,Tz)/(np.sqrt(var)*e)
        mx=maximum_filter(ncc,size=(max(3,H//3),max(3,W//3)))
        ys,xs=np.where((ncc>=mx)&(ncc>thr[k])&(s1>=inkmin[k]))
        for y,x in zip(ys,xs):
            if x-W//2+W/2<xmin: continue
            dets.append((float(ncc[y,x])*np.sqrt(T.sum()),float(ncc[y,x]),k,int(x-W//2),int(y-H//2),W,H))
    dets.sort(reverse=True)
    claimed=np.zeros(B.shape,bool); keep=[]
    for adj,s,k,x,y,W,H in dets:
        y0,y1=max(0,y),min(H0,y+H); x0,x1=max(0,x),min(W0,x+W)
        if y1<=y0 or x1<=x0: continue
        box=B[y0:y1,x0:x1]>0
        ink=box.sum(); 
        if ink==0: continue
        already=(claimed[y0:y1,x0:x1]&box).sum()
        if already>0.30*ink: continue
        claimed[y0:y1,x0:x1]|=box; keep.append((s,k,x,y,W,H))
    ncent=int(round((H0-first_top)/pitch))+1; cent=np.array([first_top+j*pitch for j in range(ncent)])
    out=sorted((int(np.argmin(np.abs(cent-(y+H/2)))),x,k,s) for s,k,x,y,W,H in keep)
    return out
r=detect(bwR,114,32,xmin=380); per=collections.Counter(t[0] for t in r)
print('f122r detections',len(r),'per line',[per[i] for i in sorted(per)])
pickle.dump(r,open('f122r_det.pkl','wb'))
bwV,_=binarize('full/f122v.jpg',0.10,0.88,820,1300,C=22)
v=detect(bwV,111,40); per=collections.Counter(t[0] for t in v); print('f122v detections',len(v),'per line',[per[i] for i in sorted(per)])
pickle.dump(v,open('f122v_det.pkl','wb'))
from lm import ALPHA
from assign95 import CL2L
kk=pickle.load(open('f122r_key.pkl','rb'))['key']
def letter(k): return CL2L[k].lower() if k in CL2L else (ALPHA[kk[k]] if k<len(kk) else '?')
for name,res in (('f122r',r),('f122v',v)):
    lines={}
    for ln,x,k,s in res: lines.setdefault(ln,[]).append(letter(k))
    print('---',name); print('\n'.join('%2d %s'%(ln+1,''.join(w)) for ln,w in sorted(lines.items())))
