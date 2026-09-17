import urllib.request, time, os
H={'User-Agent':'Mozilla/5.0'}
for s in range(329,378):
    for kind,url,out in [('img',f'https://api.digitale-sammlungen.de/iiif/image/v2/bsb10720287_{s:05d}/full/full/0/default.jpg',f'img/t2_{s:04d}.jpg'),
                         ('hocr',f'https://api.digitale-sammlungen.de/ocr/bsb10720287/{s}',f'hocr/{s}.html')]:
        if os.path.exists(out) and os.path.getsize(out)>1000: continue
        for a in range(5):
            try:
                d=urllib.request.urlopen(urllib.request.Request(url,headers=H),timeout=90).read()
                open(out,'wb').write(d); break
            except Exception as e:
                time.sleep(3*(a+1))
        time.sleep(0.3)
print('done')
