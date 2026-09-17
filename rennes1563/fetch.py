import urllib.request, time, sys, os
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
jobs=[
 ('btv1b10033942k',[70,71,72,73,179,180,181],'c390'),
 ('btv1b100339594',[112,113,114,115],'c392'),
 ('btv1b9059845t',[53,54,55,56,57,58,59],'fr3181'),
]
os.makedirs('img',exist_ok=True)
for ark,views,tag in jobs:
    for v in views:
        out=f'img/{tag}_v{v}.jpg'
        if os.path.exists(out) and os.path.getsize(out)>20000: continue
        url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f{v}/full/2500,/0/native.jpg'
        for att in range(5):
            try:
                d=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=240).read()
                open(out,'wb').write(d)
                print(out,len(d)); break
            except Exception as e:
                print(out,'retry',att,e); time.sleep(20+20*att)
        time.sleep(6)
print('done')
