"""Fetch canvases of fr. 16093 (ark btv1b90074656) by canvas index."""
import sys, os, time, urllib.request
ARK='btv1b90074656'
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept':'*/*'}
W=int(os.environ.get('W','1500'))
os.makedirs('img',exist_ok=True)
for a in sys.argv[1:]:
    i=int(a)
    fn=f'img/c{i:03d}_w{W}.jpg'
    if os.path.exists(fn) and os.path.getsize(fn)>5000:
        print(i,'have',os.path.getsize(fn),flush=True); continue
    url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ARK}/f{i}/full/{W},/0/native.jpg'
    for t in range(6):
        try:
            d=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=180).read()
            open(fn,'wb').write(d); print(i,len(d),flush=True); break
        except Exception as e:
            print(i,'fail',str(e)[:60],flush=True); time.sleep(8*(t+1))
    time.sleep(0.4)
print('DONE',flush=True)
