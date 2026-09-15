"""Retry Gallica until the IIIF manifest of BnF 500 de Colbert 401 loads, then download the folios we need."""
import json, time, re, os, urllib.request, sys
ARK='btv1b10035574w'
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept':'*/*'}
def get(url, timeout=120):
    req=urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=timeout).read()
man=None
for attempt in range(40):
    try:
        raw=get(f'https://gallica.bnf.fr/iiif/ark:/12148/{ARK}/manifest.json')
        man=json.loads(raw); break
    except Exception as e:
        print(time.strftime('%H:%M:%S'),'manifest attempt',attempt,'failed:',str(e)[:80], flush=True); time.sleep(300)
if not man: print('GIVEUP'); sys.exit(1)
json.dump(man,open('manifest.json','w'))
canv=man['sequences'][0]['canvases']
print('label:',man.get('label'),'canvases:',len(canv), flush=True)
want=['143','233','239','288','321','333']
os.makedirs('img',exist_ok=True)
for i,c in enumerate(canv):
    lab=str(c.get('label',''))
    if any(re.search(r'\b'+w+r'\b',lab) for w in want):
        url=c['images'][0]['resource']['@id']
        # request full resolution via IIIF
        full=re.sub(r'/full/[^/]+/0/','/full/full/0/',url)
        fn=f"img/{i+1:04d}_{re.sub(r'[^A-Za-z0-9]+','_',lab)[:30]}.jpg"
        for t in range(5):
            try:
                open(fn,'wb').write(get(full,timeout=300)); print('saved',fn,lab,flush=True); break
            except Exception as e:
                print('img fail',fn,str(e)[:60],flush=True); time.sleep(60)
print('DONE',flush=True)
