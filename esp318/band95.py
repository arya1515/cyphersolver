import pickle, numpy as np, collections
from PIL import Image
from scipy import ndimage
from scipy.cluster.hierarchy import fcluster
from seg import binarize
from assign95 import CL2L
from lm import ALPHA, IDX
S=28
def feat(b):
    h,w=b.shape; im=Image.fromarray((b*255).astype('uint8'))
    sc=S/max(h,w); nw,nh=max(1,int(round(w*sc))),max(1,int(round(h*sc)))
    a=np.zeros((S,S),np.float32); y0=(S-nh)//2; x0=(S-nw)//2
    a[y0:y0+nh,x0:x0+nw]=np.asarray(im.resize((nw,nh),Image.BILINEAR),np.float32)/255.
    return np.concatenate([a.ravel(),[np.log(np.clip(w/float(h),0.15,6.0))*1.2]])
# reference templates from the labelled clusters of the first run
d=pickle.load(open('f122r_glyphs.pkl','rb')); lab=fcluster(d['Z'],110,'maxclust'); meta=d['meta']; bmps=d['bmps']
JUNK={20,10,17,13,64,15,14,11,57,58,12,19,51,55,60,63,66,16,65,23,24,27,31}
ref=[]; refl=[]
for i,m in enumerate(meta):
    k=int(lab[i])
    if k in JUNK or k not in CL2L: continue
    ref.append(feat(bmps[i])); refl.append(CL2L[k].lower())
ref=np.array(ref); refl=np.array(refl); print('reference glyphs',len(ref))
# band-clipped segmentation
pitch=114; top=32; y0,y1=800,4250
bw,gray=binarize('full/f122r.jpg',0.14,0.93,y0,y1,C=22)
H,W=bw.shape; ncent=int(round((H-top)/pitch))+1; cent=np.array([top+k*pitch for k in range(ncent)])
half=int(pitch*0.42)
units=[]
for ln,c in enumerate(cent):
    a=max(0,int(c-half)); b=min(H,int(c+half))
    band=bw[a:b]
    # keep components whose ink mostly lies in this band
    lab2,n=ndimage.label(band); objs=ndimage.find_objects(lab2)
    comps=[]
    for i,sl in enumerate(objs):
        m=(lab2[sl]==i+1); npx=m.sum()
        if npx<25: continue
        ys,xs=sl
        comps.append(dict(x0=xs.start,x1=xs.stop,y0=ys.start,y1=ys.stop,n=int(npx),id=i+1))
    comps.sort(key=lambda c:c['x0'])
    small=pitch*pitch*0.035
    big=[c for c in comps if c['n']>=small]; sml=[c for c in comps if c['n']<small]
    groups=[]
    for c in big:
        placed=False
        for g in groups:
            gx0=min(x['x0'] for x in g); gx1=max(x['x1'] for x in g)
            inter=min(gx1,c['x1'])-max(gx0,c['x0']); narrow=min(gx1-gx0,c['x1']-c['x0'])
            if narrow>0 and inter>=0.35*narrow: g.append(c); placed=True; break
        if not placed: groups.append([c])
    for c in sml:
        best,bs=None,-1e9
        for g in groups:
            gx0=min(x['x0'] for x in g); gx1=max(x['x1'] for x in g)
            inter=min(gx1,c['x1'])-max(gx0,c['x0']); s=inter if inter>0 else -min(abs(c['x0']-gx1),abs(gx0-c['x1']))
            if s>bs: bs,best=s,g
        if best is not None and bs>-pitch*0.25: best.append(c)
        else: groups.append([c])
    groups.sort(key=lambda g:min(x['x0'] for x in g))
    for g in groups:
        gx0=min(x['x0'] for x in g); gx1=max(x['x1'] for x in g); gy0=min(x['y0'] for x in g); gy1=max(x['y1'] for x in g)
        mask=np.zeros((gy1-gy0,gx1-gx0),bool)
        for x in g: mask|=(lab2[gy0:gy1,gx0:gx1]==x['id'])
        units.append(dict(line=ln,x0=gx0,w=gx1-gx0,n=int(mask.sum()),bmp=mask))
per=collections.Counter(u['line'] for u in units)
print('band units',len(units),'per line median',np.median(list(per.values())))
# NN classification against reference glyphs
X=np.array([feat(u['bmp']) for u in units])
thr=np.percentile([np.linalg.norm(ref[i]-ref[j]) for i in range(0,len(ref),7) for j in range(len(ref)) if refl[i]==refl[j] and i!=j],60)
print('nn thr',round(thr,2))
out=[]
for i,u in enumerate(units):
    dd=np.linalg.norm(ref-X[i],axis=1); j=dd.argmin()
    # vote among 5 nearest within thr
    order=np.argsort(dd)[:5]; votes=collections.Counter(refl[k] for k in order if dd[k]<thr)
    let=votes.most_common(1)[0][0] if votes else '.'
    out.append((u['line'],u['x0'],let,float(dd[j])))
cov=sum(1 for o in out if o[2]!='.'); print('classified',cov,'of',len(out),round(cov/len(out),2))
lines={}
for ln,x,l,dd in out: lines.setdefault(ln,[]).append(l)
txt='\n'.join('%2d %s'%(ln+1,''.join(w)) for ln,w in sorted(lines.items()))
open('f122r_band.txt','w').write(txt); print(txt)
pickle.dump(out,open('f122r_band.pkl','wb'))
