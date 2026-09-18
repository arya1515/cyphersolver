import os,time,urllib.request
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'}
ark='btv1b90601558'
jobs=[(i,'1000,','btv1b90601558') for i in range(91,111)]+[(i,'full','hi') for i in [86,87,88,89,90,78,79,80,81,82,83,33,34,32,53,54,76,77]]+[(i,'1000,','btv1b90601558') for i in range(111,159)]
for i,sz,d in jobs:
    os.makedirs(d,exist_ok=True); fn=f'{d}/c{i:03d}.jpg'
    if os.path.exists(fn) and os.path.getsize(fn)>20000: continue
    url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f{i}/full/{sz}/0/native.jpg'
    for t in range(10):
        try:
            b=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=180).read(); open(fn,'wb').write(b); print(d,i,len(b),flush=True); break
        except Exception as e:
            print(i,'fail',str(e)[:50],flush=True); time.sleep(60*(t+1))
    time.sleep(6)
print('DONE',flush=True)
