import pickle, numpy as np, collections, math, sys
from PIL import Image
from scipy.cluster.hierarchy import fcluster
from seg import binarize
from assign95 import CL2L
from lm import ALPHA, IDX
L=len(ALPHA)
def corr(B,K):
    H,W=B.shape; h,w=K.shape; fh,fw=H+h-1,W+w-1
    full=np.fft.irfft2(np.fft.rfft2(B,s=(fh,fw))*np.fft.rfft2(K[::-1,::-1],s=(fh,fw)),s=(fh,fw))
    return full[h-1:H,w-1:W].astype(np.float32)   # valid, top-left anchored
JUNK={20,10,17,13,64,15,14,11,57,58,12,19,51,55,60,63,66,16,65,23,24,27,31}
d=pickle.load(open('f122r_glyphs.pkl','rb')); lab=fcluster(d['Z'],110,'maxclust'); meta=d['meta']; bmps=d['bmps']
tpl=[]  # (letter, T, thr)
for k in sorted(set(lab.tolist())):
    if k in JUNK or k not in CL2L: continue
    idx=[i for i in range(len(meta)) if lab[i]==k]
    if len(idx)<3: continue
    H=int(np.median([bmps[i].shape[0] for i in idx])); W=int(np.median([bmps[i].shape[1] for i in idx]))
    acc=np.zeros((H,W),np.float32); ss=[]
    for i in idx: acc+=np.asarray(Image.fromarray((bmps[i]*255).astype('uint8')).resize((W,H),Image.BILINEAR),np.float32)/255.
    T=acc/len(idx); Tz=T-T.mean(); e=np.sqrt((Tz**2).sum())
    for i in idx:
        b=np.asarray(Image.fromarray((bmps[i]*255).astype('uint8')).resize((W,H),Image.BILINEAR),np.float32)/255.
        v=b.sum()-b.sum()**2/(H*W)
        if v>0: ss.append(((b-b.mean())*Tz).sum()/(np.sqrt(v)*e))
    tpl.append((CL2L[k].lower(),T,max(0.45,float(np.percentile(ss,20))-0.05)))
print('templates',len(tpl))
pitch=114; top=32; y0,y1=800,4250
bw,_=binarize('full/f122r.jpg',0.14,0.93,y0,y1,C=22); B=bw.astype(np.float32); Hf,Wf=B.shape
XMIN=380
GAP=float(sys.argv[1]) if len(sys.argv)>1 else 0.012
MINW=int(np.median([m['x1']-m['x0'] for i,m in enumerate(meta) if lab[i] not in JUNK])*0.55); print('minw',MINW)   # penalty per skipped ink column (fraction of column ink)
results=[]
for ln in range(31):
    c=top+ln*pitch; a=max(0,int(c-pitch*0.62)); b=min(Hf,int(c+pitch*0.62))
    band=B[a:b, XMIN:]; h,w=band.shape
    colink=band.sum(0)
    # per template: best NCC over y for each x (left anchor), width
    cands=[]  # list of arrays s_k[x]
    for let,T,thr in tpl:
        H,W=T.shape
        if H>h: T=T[:h]; H=h
        Tz=T-T.mean(); e=np.sqrt((Tz**2).sum())
        s1=corr(band,np.ones((H,W),np.float32)); var=np.maximum(s1-s1*s1/(H*W),1e-3)
        ncc=corr(band,Tz)/(np.sqrt(var)*e); ncc[s1<0.6*T.sum()]=-1
        s=ncc.max(0)   # over y  -> length w-W+1
        cands.append((let,W,s,thr))
    # DP over x
    NEG=-1e9; best=np.full(w+1,NEG); best[0]=0.0; back=[None]*(w+1)
    for x in range(1,w+1):
        # skip column x-1
        v=best[x-1]-GAP*colink[x-1]
        if v>best[x]: best[x]=v; back[x]=('skip',None)
        for ki,(let,W,s,thr) in enumerate(cands):
            if x-W<0: continue
            sc=s[x-W]
            if sc<thr: continue
            if W<MINW: continue
            v=best[x-W]+ (sc-thr)*W*4.0
            if v>best[x]: best[x]=v; back[x]=('t',ki)
    # backtrack
    x=w; segs=[]
    while x>0:
        kind,ki=back[x]
        if kind=='skip': x-=1; continue
        let,W,s,thr=cands[ki]; segs.append((x-W,W,ki)); x-=W
    segs.reverse()
    # emission vectors: for each seg, NCC of every template of similar width anchored near the same x
    units=[]
    for x0,W,ki in segs:
        vec=np.full(L,-1.0)
        for kj,(let,Wj,s,thr) in enumerate(cands):
            if abs(Wj-W)>0.5*W: continue
            lo=max(0,x0-6); hi=min(len(s),x0+7)
            v=float(s[lo:hi].max()) if hi>lo else -1
            vec[IDX[let]]=max(vec[IDX[let]],v)
        units.append((ln,x0+XMIN,vec,cands[ki][0]))
    results.extend(units)
    print('line',ln+1,'segs',len(segs),''.join(u[3] for u in units),flush=True)
pickle.dump(results,open('f122r_dpunits.pkl','wb'))
