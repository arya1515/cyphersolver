import json, time, os, sys, urllib.request
ARK='btv1b10035574w'
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept':'*/*'}
def get(url, timeout=120):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout).read()
W=int(sys.argv[1]) if len(sys.argv)>1 else 1400
for i in range(1,441):
    fn=f'sweep/c{i:03d}.jpg'
    if os.path.exists(fn) and os.path.getsize(fn)>5000: continue
    url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ARK}/f{i}/full/{W},/0/native.jpg'
    for t in range(6):
        try:
            d=get(url); open(fn,'wb').write(d); print(i,len(d),flush=True); break
        except Exception as e:
            print(i,'fail',str(e)[:60],flush=True); time.sleep(20*(t+1))
    time.sleep(0.7)
print('DONE',flush=True)
