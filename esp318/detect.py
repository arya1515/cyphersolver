import pickle, numpy as np, sys
from PIL import Image
def fftconvolve(B,K,mode='same'):
    # 'same'-mode 2-D convolution via numpy FFT (scipy.signal is blocked on this machine)
    H,W=B.shape; h,w=K.shape; fh,fw=H+h-1,W+w-1
    F=np.fft.rfft2(B,s=(fh,fw)); G=np.fft.rfft2(K,s=(fh,fw))
    full=np.fft.irfft2(F*G,s=(fh,fw))
    oy,ox=(h-1)//2,(w-1)//2
    return full[oy:oy+H,ox:ox+W].astype(np.float32)
from scipy.cluster.hierarchy import fcluster
from seg import binarize
JUNK={20,10,17,13,64,15,14,11,57,58,12,19,51,55,60,63,66,16,65,23,24,27,31}
d=pickle.load(open('f122r_glyphs.pkl','rb')); lab=fcluster(d['Z'],110,'maxclust'); meta=d['meta']; bmps=d['bmps']
# templates: per clean cluster with >=3 members, mean bitmap at the cluster's median size
tpl={}
for k in sorted(set(lab.tolist())):
    if k in JUNK: continue
    idx=[i for i in range(len(meta)) if lab[i]==k]
    if len(idx)<3: continue
    hs=[bmps[i].shape[0] for i in idx]; ws=[bmps[i].shape[1] for i in idx]
    H,W=int(np.median(hs)),int(np.median(ws))
    acc=np.zeros((H,W),np.float32)
    for i in idx:
        acc+=np.asarray(Image.fromarray((bmps[i]*255).astype('uint8')).resize((W,H),Image.BILINEAR),np.float32)/255.
    tpl[k]=acc/len(idx)
print('templates',len(tpl))
def detect(page, x0f, x1f, y0, y1, pitch, first_top, thr=0.55, xmin=None):
    bw,_=binarize(page,x0f,x1f,y0,y1,C=22); B=bw.astype(np.float32)
    dets=[]
    for k,T in tpl.items():
        H,W=T.shape; Tz=T-T.mean(); e=np.sqrt((Tz**2).sum())
        if e==0: continue
        num=fftconvolve(B,Tz[::-1,::-1],mode='same')
        box=np.ones((H,W),np.float32)
        s1=fftconvolve(B,box,mode='same'); var=np.maximum(s1-s1*s1/(H*W),1e-3)
        ncc=num/(np.sqrt(var)*e)
        # local maxima
        from scipy.ndimage import maximum_filter
        mx=maximum_filter(ncc,size=(max(3,H//2),max(3,W//2)))
        ys,xs=np.where((ncc>=mx)&(ncc>thr))
        for y,x in zip(ys,xs):
            dets.append((float(ncc[y,x]),k,int(x-W//2),int(y-H//2),W,H))
    dets.sort(reverse=True)
    keep=[]
    for s,k,x,y,W,H in dets:
        if xmin is not None and x+W/2<xmin: continue
        ok=True
        for s2,k2,x2,y2,W2,H2 in keep:
            ix=max(0,min(x+W,x2+W2)-max(x,x2)); iy=max(0,min(y+H,y2+H2)-max(y,y2))
            inter=ix*iy; 
            if inter>0.35*min(W*H,W2*H2): ok=False; break
        if ok: keep.append((s,k,x,y,W,H))
    ncent=int(round((y1-y0-first_top)/pitch))+1; cent=np.array([first_top+j*pitch for j in range(ncent)])
    out=[]
    for s,k,x,y,W,H in keep:
        ln=int(np.argmin(np.abs(cent-(y+H/2)))); out.append((ln,x,k,s))
    out.sort()
    return out,bw
if __name__=='__main__':
    xmin=min(m['x0'] for m in meta if lab[list(meta).index(m)] not in JUNK) if False else 380
    r,bw=detect('full/f122r.jpg',0.14,0.93,800,4250,114,32,thr=float(sys.argv[1]) if len(sys.argv)>1 else 0.55,xmin=xmin)
    import collections; per=collections.Counter(t[0] for t in r)
    print('f122r detections',len(r),'per line',[per[i] for i in sorted(per)])
    pickle.dump(r,open('f122r_det.pkl','wb'))
    v,_=detect('full/f122v.jpg',0.10,0.88,820,1300,111,40,thr=float(sys.argv[1]) if len(sys.argv)>1 else 0.55,xmin=0)
    per=collections.Counter(t[0] for t in v); print('f122v detections',len(v),'per line',[per[i] for i in sorted(per)])
    pickle.dump(v,open('f122v_det.pkl','wb'))
    from lm import ALPHA
    from assign95 import CL2L
    kk=pickle.load(open('f122r_key.pkl','rb'))['key']
    def letter(k): return CL2L[k].lower() if k in CL2L else (ALPHA[kk[k]] if k<len(kk) else '?')
    for name,res in (('f122r',r),('f122v',v)):
        lines={}
        for ln,x,k,s in res: lines.setdefault(ln,[]).append(letter(k))
        print('---',name); print('\n'.join('%2d %s'%(ln+1,''.join(w)) for ln,w in sorted(lines.items())))
