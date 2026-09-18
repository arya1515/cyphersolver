import numpy as np, pickle, sys
from PIL import Image, ImageDraw
from scipy.cluster.hierarchy import fcluster
d=pickle.load(open(sys.argv[1],'rb')); nc=int(sys.argv[2]); out=sys.argv[3]
lo=int(sys.argv[4]) if len(sys.argv)>4 else 0
hi=int(sys.argv[5]) if len(sys.argv)>5 else 999
lab=fcluster(d['Z'],nc,'maxclust'); bmps=d['bmps']
order=sorted(set(lab), key=lambda k:-(lab==k).sum())
order=order[lo:hi]
cell=76; maxper=12
rows=[]
for k in order:
    idx=[i for i,l in enumerate(lab) if l==k][:maxper]
    row=np.ones((cell,cell*(maxper+1)),np.uint8)*255
    for j,i in enumerate(idx):
        b=bmps[i]; h,w=b.shape
        sc=(cell-10)/max(h,w); nw,nh=max(1,int(w*sc)),max(1,int(h*sc))
        im=np.asarray(Image.fromarray((~b*255).astype('uint8')).resize((nw,nh),Image.BILINEAR))
        yo=(cell-nh)//2; xo=cell*(j+1)+(cell-nw)//2
        row[yo:yo+nh,xo:xo+nw]=im
    rows.append((k,int((lab==k).sum()),row))
img=np.ones((cell*len(rows),cell*(maxper+1)),np.uint8)*255
for r,(k,n,row) in enumerate(rows): img[r*cell:(r+1)*cell]=row
im=Image.fromarray(img).convert('RGB'); dr=ImageDraw.Draw(im)
for r,(k,n,_) in enumerate(rows): dr.text((4,r*cell+cell//2-6), f"{k}:{n}", fill=(200,0,0))
im.save(out); print(out, im.size, [(k,n) for k,n,_ in rows])
