import os, time, urllib.request, sys
UA={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36','Accept':'image/jpeg,*/*'}
want=[int(x) for x in sys.argv[1:]]
for c in want:
    fn=f'full16127/c{c}.jpg'
    if os.path.exists(fn) and os.path.getsize(fn)>100000: continue
    for t in range(8):
        try:
            d=urllib.request.urlopen(urllib.request.Request(f'https://gallica.bnf.fr/iiif/ark:/12148/btv1b90609766/f{c}/full/full/0/native.jpg',headers=UA),timeout=240).read()
            if len(d)>100000: open(fn,'wb').write(d); print(c,len(d),flush=True); break
            print(c,'short',len(d),flush=True); time.sleep(20*(t+1))
        except Exception as e:
            print(c,'fail',str(e)[:60],flush=True); time.sleep(20*(t+1))
    time.sleep(4)
print('REFETCH DONE',flush=True)
