import sys, os, time, urllib.request
ark,a,b=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); W=int(sys.argv[4]) if len(sys.argv)>4 else 300
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
d=f'th_{ark}'; os.makedirs(d,exist_ok=True)
for i in range(a,b+1):
    fn=f'{d}/c{i:03d}_{W}.jpg'
    if os.path.exists(fn): continue
    url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f{i}/full/{W},/0/native.jpg'
    for t in range(6):
        try: open(fn,'wb').write(urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=120).read()); break
        except Exception as e: print(i,'fail',e,flush=True); time.sleep(10*(t+1))
    time.sleep(0.5)
print('done',ark)
