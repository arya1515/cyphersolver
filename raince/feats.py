"""Re-run seg2.py's segmentation and save the per-token feature vectors (same order as
raince_tokens.json), so a per-letter classifier can be trained on them."""
import json, numpy as np
from PIL import Image
from scipy import ndimage
from scipy.ndimage import uniform_filter, gaussian_filter
REGIONS = [
    ('../f2984/c16_full.jpg','f29r',0.59,0.965,0.230,0.746),
    ('../f2984/c17_full.jpg','f30v',0.06,0.50,0.03,0.775),
    ('../f2984/c17_full.jpg','f31r',0.585,0.965,0.03,0.535),
    ('../f2984/c54_full.jpg','f105r',0.55,0.965,0.345,0.80),
]
SZ=24
ref=json.load(open('raince_tokens.json'))
feats=[]; order=[]
for img,name,x0f,x1f,y0f,y1f in REGIONS:
    im=Image.open(img).convert('L'); W,H=im.size
    x0,x1,y0,y1=int(W*x0f),int(W*x1f),int(H*y0f),int(H*y1f)
    reg=np.array(im.crop((x0,y0,x1,y1))).astype(float)
    bg=uniform_filter(reg,size=81); bw=(reg<bg-45)
    lab,n=ndimage.label(bw)
    r=ref['regions'][name]; pitch=r['pitch']; lines=r['lines']
    toks=[t for t in ref['tokens'] if t['page']==name]
    for t in toks:
        sub=lab[t['y0']:t['y1'], t['x0']:t['x1']]
        m=(sub>0).astype(float)
        h,w=m.shape; sc=SZ/max(h,w)
        pm=Image.fromarray((m*255).astype(np.uint8)).resize((max(1,int(w*sc)),max(1,int(h*sc))),Image.BILINEAR)
        canvas=Image.new('L',(SZ,SZ),0); canvas.paste(pm,((SZ-pm.width)//2,(SZ-pm.height)//2))
        a=gaussian_filter(np.array(canvas).astype(float)/255.0,1.0).ravel()
        lc=lines[t['line']]
        geo=np.array([(t['y0']-lc)/pitch,(t['y1']-lc)/pitch,(t['x1']-t['x0'])/pitch,(t['y1']-t['y0'])/pitch])*6.0
        feats.append(np.concatenate([a,geo])); order.append((name,t['line'],t['x0']))
X=np.array(feats,dtype=np.float32)
np.save('feats.npy',X); json.dump(order,open('feats_order.json','w'))
print(X.shape)
