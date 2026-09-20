"""Fetch a page region of fr. 16093 by canvas index. Default region = right-hand page of the opening."""
import sys, os, time, urllib.request
ARK='btv1b90074656'
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept':'*/*'}
REG=os.environ.get('REG','pct:48,0,52,100'); W=int(os.environ.get('W','2400'))
tag=REG.replace(':','').replace(',','_')
os.makedirs('img',exist_ok=True)
for a in sys.argv[1:]:
    i=int(a); fn=f'img/r{i:03d}_{tag}_w{W}.jpg'
    if os.path.exists(fn) and os.path.getsize(fn)>5000: print(i,'have',flush=True); continue
    url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ARK}/f{i}/{REG}/{W},/0/native.jpg'
    for t in range(6):
        try:
            d=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=240).read()
            open(fn,'wb').write(d); print(i,len(d),fn,flush=True); break
        except Exception as e:
            print(i,'fail',str(e)[:70],flush=True); time.sleep(8*(t+1))
    time.sleep(0.4)
print('DONE',flush=True)
