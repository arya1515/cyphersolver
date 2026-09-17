# Joint clustering across pages. cluster_multi.py K out_prefix prefix1:nlines prefix2:nlines ...
import sys, json, numpy as np
from PIL import Image, ImageDraw
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
K=int(sys.argv[1]); out=sys.argv[2]; thr=160; S=28
feats=[]; meta=[]; thumbs=[]
for spec in sys.argv[3:]:
    pre,n=spec.split(':'); n=int(n)
    boxes=json.load(open(f'{pre}_glyphs.json'))
    for k in range(1,n+1):
        im=Image.open(f'{pre}_l{k:02d}.png'); a=np.asarray(im); H=a.shape[0]
        for j,(x0,y0,x1,y1,area) in enumerate(boxes[str(k)]):
            g=a[y0:y1,x0:x1]; g=(g<thr).astype(np.uint8)*255
            h,w=g.shape; s=max(h,w)
            canvas=np.zeros((s,s),np.uint8); canvas[(s-h)//2:(s-h)//2+h,(s-w)//2:(s-w)//2+w]=g
            t=np.asarray(Image.fromarray(canvas).resize((S,S),Image.BILINEAR)).astype(float)/255
            f=np.concatenate([t.ravel(), [3*w/H, 3*h/H, 3*y0/H, 3*y1/H]])
            feats.append(f); meta.append((pre,k,j)); thumbs.append(Image.fromarray(255-canvas).resize((40,40)))
X=np.array(feats); Xp=PCA(40,random_state=0).fit_transform(X)
km=KMeans(K,n_init=10,random_state=0).fit(Xp); lab=km.labels_
res={}
for (pre,k,j),l in zip(meta,lab): res.setdefault(pre,{}).setdefault(str(k),[]).append(int(l))
json.dump(res,open(f'{out}_clusters.json','w'))
np.save(f'{out}_feats.npy',Xp); json.dump(meta,open(f'{out}_meta.json','w'))
order=np.argsort(-np.bincount(lab))
print('sizes',[(int(c),int((lab==c).sum())) for c in order])
rows=[]
for c in order:
    idx=np.where(lab==c)[0]; idx=idx[np.linspace(0,len(idx)-1,min(30,len(idx))).astype(int)]
    row=Image.new('L',(30*42+60,42),255); ImageDraw.Draw(row).text((2,14),f'{c}:{(lab==c).sum()}',fill=0)
    for i,ii in enumerate(idx): row.paste(thumbs[ii],(60+i*42,1))
    rows.append(row)
M=Image.new('L',(rows[0].width,42*len(rows)),255)
for i,r in enumerate(rows): M.paste(r,(0,i*42))
M.save(f'{out}_montage.png'); print(M.size, len(meta),'glyphs')
