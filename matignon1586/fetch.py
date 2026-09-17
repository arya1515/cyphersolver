import sys, os, time, urllib.request
ark=sys.argv[1]; W=int(sys.argv[2]); out=sys.argv[3]
idx=[int(x) for x in sys.argv[4].split(',')] if len(sys.argv)>4 else []
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
os.makedirs(out,exist_ok=True)
for i in idx:
    fn=f'{out}/c{i:03d}.jpg'
    if os.path.exists(fn) and os.path.getsize(fn)>20000: print(i,'have',flush=True); continue
    url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f{i}/full/{W},/0/native.jpg'
    for t in range(6):
        try:
            d=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=240).read()
            open(fn,'wb').write(d); print(i,len(d),flush=True); break
        except Exception as e:
            print(i,'fail',str(e)[:70],flush=True); time.sleep(8*(t+1))
    time.sleep(0.3)
print('DONE',flush=True)
