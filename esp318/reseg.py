import pickle, numpy as np, sys
from PIL import Image
from scipy.cluster.hierarchy import fcluster
from scipy import ndimage
from glyphs import extract
from lm import ALPHA, IDX
from assign95 import CL2L
S=28
def feat(b):
    h,w=b.shape
    im=Image.fromarray((b*255).astype('uint8'))
    sc=S/max(h,w); nw,nh=max(1,int(round(w*sc))),max(1,int(round(h*sc)))
    a=np.zeros((S,S),np.float32); y0=(S-nh)//2; x0=(S-nw)//2
    a[y0:y0+nh,x0:x0+nw]=np.asarray(im.resize((nw,nh),Image.BILINEAR),np.float32)/255.
    return np.concatenate([a.ravel(),[np.log(np.clip(w/float(h),0.15,6.0))*1.2]])

d=pickle.load(open('f122r_glyphs.pkl','rb'))
lab=fcluster(d['Z'],110,'maxclust'); meta=d['meta']; bmps=d['bmps']
JUNK={20,10,17,13,64,15,14,11,57,58,12,19,51,55,60,63,66,16,65,23,24,27,31}
clean=[i for i in range(len(meta)) if lab[i] not in JUNK]
junk=[i for i in range(len(meta)) if lab[i] in JUNK]
X=np.array([feat(b) for b in bmps])
# medoid (mean) per clean cluster + within-cluster spread
cl={}
for i in clean: cl.setdefault(int(lab[i]),[]).append(i)
cent={k:X[v].mean(0) for k,v in cl.items()}
spread=[]
for k,v in cl.items():
    if len(v)>=3: spread+= [np.linalg.norm(X[i]-cent[k]) for i in v]
thr=np.percentile(spread,92); print('NN threshold',round(thr,2),'median within',round(np.median(spread),2))
K=sorted(cent); C=np.array([cent[k] for k in K])
def nn(f):
    dd=np.linalg.norm(C-f,axis=1); j=dd.argmin(); return K[j], dd[j]
ws=np.array([m['x1']-m['x0'] for m in meta]); hs=np.array([m['y1']-m['y0'] for m in meta])
medw=np.median(ws[clean]); meda=np.median([meta[i]['n'] for i in clean])
print('junk',len(junk),'clean',len(clean),'median clean w',medw,'median ink',meda)
wide=[i for i in junk if ws[i]>1.55*medw]; small=[i for i in junk if meta[i]['n']<0.30*meda]
print('junk wide',len(wide),'junk small',len(small))
# new glyph list: keep clean as-is; split wide; drop small; NN for rest
new=[]  # (line,x0,label,dist)
for i in clean: new.append((meta[i]['line'],meta[i]['x0'],int(lab[i]),0.0))
recl=0; drop=0; splitn=0
for i in junk:
    m=meta[i]; b=bmps[i]
    if i in small: drop+=1; continue
    if i in wide:
        col=b.sum(0).astype(float); w=len(col)
        lo,hi=int(w*0.3),int(w*0.7)
        cut=lo+int(np.argmin(ndimage.uniform_filter1d(col,5)[lo:hi]))
        parts=[b[:,:cut],b[:,cut:]]
        # trim empty rows/cols
        outp=[]
        for p in parts:
            ys=np.where(p.any(1))[0]; xs=np.where(p.any(0))[0]
            if len(ys)==0 or len(xs)==0: continue
            outp.append((p[ys[0]:ys[-1]+1, xs[0]:xs[-1]+1], xs[0]))
        if len(outp)==2:
            splitn+=1
            for p,xo in outp:
                k,dist=nn(feat(p)); new.append((m['line'],m['x0']+xo,k if dist<thr else -1,dist))
            continue
    k,dist=nn(feat(b)); new.append((m['line'],m['x0'],k if dist<thr else -1,dist)); recl+= dist<thr
print('split',splitn,'dropped',drop,'reclassified',recl,'still gap',sum(1 for n in new if n[2]==-1))
new.sort(key=lambda t:(t[0],t[1]))
pickle.dump(new,open('f122r_reseg.pkl','wb'))
# decode with current fixed + solved free key
kk=pickle.load(open('f122r_key.pkl','rb'))['key']
def letter(k):
    if k==-1: return '.'
    if k in CL2L: return CL2L[k].lower()
    return ALPHA[kk[k]] if k<len(kk) else '?'
lines={}
for ln,x,k,dist in new: lines.setdefault(ln,[]).append(letter(k))
txt=['%2d %s'%(ln+1,''.join(v)) for ln,v in sorted(lines.items())]
tot=sum(len(v) for v in lines.values()); cov=sum(c!='.' for v in lines.values() for c in v)
print('glyphs',tot,'covered',cov,round(cov/tot,2))
open('f122r_reseg.txt','w').write('\n'.join(txt)); print('\n'.join(txt))
# ---- f122v through the same pipeline, NN-classified against f122r clusters
g2,bw2=extract('full/f122v.jpg',0.10,0.88,820,1300,pitch=111,first_top=40)
v=[]
for x in g2:
    k,dist=nn(feat(x['bmp'])); v.append((x['line'],x['x0'],k if dist<thr else -1,dist))
v.sort(key=lambda t:(t[0],t[1]))
pickle.dump(v,open('f122v_reseg.pkl','wb'))
lines={}
for ln,x,k,dist in v: lines.setdefault(ln,[]).append(letter(k))
print('--- f122v ---'); print('\n'.join('%2d %s'%(ln+1,''.join(w)) for ln,w in sorted(lines.items())))
