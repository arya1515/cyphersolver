import numpy as np, sys, json
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
src,pre=sys.argv[1],sys.argv[2]
box=tuple(map(int,sys.argv[3].split(','))) if len(sys.argv)>3 else None
im=Image.open(src).convert('L')
if box: im=im.crop(box)
a=np.array(im).astype(float)
bg=ndi.median_filter(a[::4,::4],15); bg=np.kron(bg,np.ones((4,4)))[:a.shape[0],:a.shape[1]]
ink=(a<bg-40); ink=ndi.binary_opening(ink,np.ones((2,2)))
lab,n=ndi.label(ndi.binary_dilation(ink,np.ones((5,5)))); objs=ndi.find_objects(lab)
shapes={frozenset('RB'):'A',frozenset('LRB'):'B',frozenset('LB'):'C',frozenset('TRB'):'D',frozenset('TLRB'):'E',frozenset('TLB'):'F',frozenset('TR'):'G',frozenset('TLR'):'H',frozenset('TL'):'I'}
G=[];D=[]
for i,s in enumerate(objs):
    m=(lab[s]==i+1)&ink[s]; h,w=m.shape; ar=m.sum()
    if h>=20 and w>=20 and ar>150 and h<95 and w<95: G.append((s,m))
    elif 4<=ar<=200 and h<=24 and w<=24: D.append(((s[0].start+s[0].stop)/2,(s[1].start+s[1].stop)/2))
out=[]
for s,m in G:
    ys,xs=np.nonzero(m); y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1; m=m[y0:y1,x0:x1]; h,w=m.shape
    q=lambda k,l:max(2,int(k*l))
    T=m[:q(.28,h),:].any(0).mean(); B=m[-q(.28,h):,:].any(0).mean()
    L=m[:,:q(.28,w)].any(1).mean(); R=m[:,-q(.28,w):].any(1).mean()
    f=frozenset(k for k,v in zip('TBLR',(T,B,L,R)) if v>0.6)
    Y0,X0=int(s[0].start+y0),int(s[1].start+x0)
    nd=sum(1 for dy,dx in D if X0+w-4<=dx<=X0+w+34 and Y0-4<=dy<=Y0+h+6)
    out.append(dict(y=Y0,x=X0,y1=Y0+h,x1=X0+w,sh=shapes.get(f,'?'),nd=nd))
# columns: chain top->bottom
out.sort(key=lambda g:g['y'])
cols=[]
for g in out:
    cx=(g['x']+g['x1'])/2; best=None
    for C in cols:
        l=C[-1]; lx=(l['x']+l['x1'])/2
        if abs(lx-cx)<24 and g['y']-l['y1']<260 and (best is None or abs(lx-cx)<best[0]): best=(abs(lx-cx),C)
    if best: best[1].append(g)
    else: cols.append([g])
cols=[C for C in cols if len(C)>=3]
cols.sort(key=lambda C:-C[0]['x'])   # right to left
json.dump(cols,open(pre+'_glyphs.json','w'))
rgb=im.convert('RGB'); d=ImageDraw.Draw(rgb)
for ci,C in enumerate(cols):
    for g in C:
        d.rectangle((g['x'],g['y'],g['x1'],g['y1']),outline=(255,0,0) if g['sh']=='?' else (0,160,0))
        d.text((g['x']-22,g['y']+8),g['sh']+str(g['nd']),fill=(0,0,255))
    d.text((C[0]['x'],C[0]['y']-14),str(ci),fill=(255,0,255))
rgb.save(pre+'_ann.png')
K=dict(zip('ABCDEFGHI',['akt','blu','cmw','dnx','eoy','fpz','gq','hr','is']))
for ci,C in enumerate(cols):
    print(ci,' '.join(g['sh']+str(g['nd']) for g in C),'|',''.join((K[g['sh']][g['nd']-1] if 1<=g['nd']<=len(K[g['sh']]) else '_') if g['sh'] in K else '?' for g in C))
