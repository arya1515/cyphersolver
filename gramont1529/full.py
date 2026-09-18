import sys, os, time, urllib.request
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
os.makedirs('full',exist_ok=True)
for spec in sys.argv[1:]:
    ark,i=spec.split(':'); fn=f'full/{ark}_c{int(i):03d}.jpg'
    if os.path.exists(fn) and os.path.getsize(fn)>50000: continue
    url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f{i}/full/full/0/native.jpg'
    for t in range(8):
        try: d=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=300).read(); open(fn,'wb').write(d); print(spec,len(d),flush=True); break
        except Exception as e: print(spec,'fail',e,flush=True); time.sleep(20*(t+1))
    time.sleep(8)
