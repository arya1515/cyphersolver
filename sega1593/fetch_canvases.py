import sys, os, time, urllib.request
# usage: fetch_canvases.py ARK WIDTH OUTDIR c1 c2 c3-c7 ...
ark=sys.argv[1]; W=sys.argv[2]; out=sys.argv[3]
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept':'*/*'}
os.makedirs(out,exist_ok=True)
cs=[]
for a in sys.argv[4:]:
    if '-' in a: x,y=a.split('-'); cs+=range(int(x),int(y)+1)
    else: cs.append(int(a))
for i in cs:
    fn=f'{out}/{ark}_c{i:03d}_w{W}.jpg'
    if os.path.exists(fn) and os.path.getsize(fn)>3000: continue
    url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f{i}/full/{W}/0/native.jpg'
    for t in range(6):
        try:
            d=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=180).read(); open(fn,'wb').write(d); print(i,len(d),flush=True); break
        except Exception as e:
            print(i,'fail',str(e)[:60],flush=True); time.sleep(20*(t+1))
    time.sleep(0.3)
print('DONE',flush=True)
