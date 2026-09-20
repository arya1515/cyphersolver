import urllib.request, time, os
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
ark='btv1b9059845t'; tag='fr3181'
os.makedirs('img',exist_ok=True)
for v in range(33,43):
    out=f'img/{tag}_v{v}.jpg'
    if os.path.exists(out) and os.path.getsize(out)>20000: continue
    url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f{v}/full/2500,/0/native.jpg'
    for att in range(5):
        try:
            d=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=240).read()
            open(out,'wb').write(d); print(out,len(d)); break
        except Exception as e:
            print(out,'retry',att,e); time.sleep(15+15*att)
    time.sleep(5)
print('done')
