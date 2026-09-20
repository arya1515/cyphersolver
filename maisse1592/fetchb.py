"""Fetch canvases/regions of Brienne 13 = NAF 6984 (ark btv1b100904592), the clear copies."""
import sys, os, time, urllib.request
ARK='btv1b100904592'
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept':'*/*'}
REG=os.environ.get('REG','full'); W=int(os.environ.get('W','1400'))
tag=REG.replace(':','').replace(',','_')
os.makedirs('br',exist_ok=True)
for a in sys.argv[1:]:
    i=int(a); fn=f'br/b{i:03d}_{tag}_w{W}.jpg'
    if os.path.exists(fn) and os.path.getsize(fn)>5000: print(i,'have',flush=True); continue
    url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ARK}/f{i}/{REG}/{W},/0/native.jpg'
    for t in range(6):
        try:
            d=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=240).read()
            open(fn,'wb').write(d); print(i,len(d),flush=True); break
        except Exception as e:
            print(i,'fail',str(e)[:70],flush=True); time.sleep(8*(t+1))
    time.sleep(0.3)
print('DONE',flush=True)
