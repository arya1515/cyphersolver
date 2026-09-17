import sys, os, time, urllib.request
ark='btv1b9060724s'; a=int(sys.argv[1]); b=int(sys.argv[2]); W=sys.argv[3] if len(sys.argv)>3 else 'full'
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept':'*/*'}
os.makedirs('img',exist_ok=True)
for i in range(a,b+1):
    fn=f'img/c{i:03d}.jpg'
    if os.path.exists(fn) and os.path.getsize(fn)>5000: continue
    url=f'https://gallica.bnf.fr/iiif/ark:/12148/{ark}/f{i}/full/{W}/0/native.jpg'
    for t in range(8):
        try:
            d=urllib.request.urlopen(urllib.request.Request(url,headers=UA),timeout=180).read(); open(fn,'wb').write(d); print(i,len(d),flush=True); break
        except Exception as e:
            print(i,'fail',str(e)[:60],flush=True); time.sleep(20*(t+1))
    time.sleep(1.0)
print('DONE',flush=True)
