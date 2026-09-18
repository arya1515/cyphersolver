import sys, os, urllib.request, time
from PIL import Image, ImageDraw
ark='btv1b9061879d' if len(sys.argv)<3 else sys.argv[2]
rng=[int(x) for x in sys.argv[1].split('-')]
ids=list(range(rng[0],rng[1]+1))
UA={'User-Agent':'Mozilla/5.0'}
os.makedirs('corners',exist_ok=True)
ims=[]
for c in ids:
    fn=f'corners/{ark}_{c:03d}.jpg'
    if not os.path.exists(fn):
        url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f{c}/pct:74,0,26,13/900,/0/native.jpg'
        for t in range(4):
            try:
                open(fn,'wb').write(urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=120).read()); break
            except Exception as e:
                print(c,'fail',str(e)[:50]); time.sleep(5)
    try: ims.append((c,Image.open(fn).convert('L')))
    except Exception: pass
W=900; rowh=max(i.height for _,i in ims)
out=Image.new('L',(W+70,rowh*len(ims)),255); d=ImageDraw.Draw(out)
y=0
for c,im in ims:
    out.paste(im,(70,y)); d.text((6,y+10),f'c{c}',fill=0); y+=rowh
out.save(f'corners/stack_{ids[0]}_{ids[-1]}.png'); print(out.size)
