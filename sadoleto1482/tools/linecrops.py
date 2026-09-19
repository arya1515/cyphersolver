import sys,json
from PIL import Image, ImageOps
# linecrops.py glyphs.json prefix n_pieces up : one crop per segmented line, split into pieces
J=json.load(open(sys.argv[1])); pre=sys.argv[2]; n=int(sys.argv[3]); up=float(sys.argv[4])
im=Image.open(J['src']).convert('L'); ox,oy=J['offset']
for li,L in enumerate(J['lines']):
    ys=sorted((b[1]+b[3])/2 for b in L); yc=ys[len(ys)//2]+oy
    x0=min(b[0] for b in L)+ox-10; x1=max(b[2] for b in L)+ox+10
    w=(x1-x0)/n
    for k in range(n):
        a=int(x0+k*w-30); b=int(x0+(k+1)*w+30)
        c=ImageOps.autocontrast(im.crop((a,int(yc-48),b,int(yc+40))),cutoff=1)
        c.resize((int(c.size[0]*up),int(c.size[1]*up)),Image.LANCZOS).save(f'{pre}_L{li+1:02d}_{k}.png')
