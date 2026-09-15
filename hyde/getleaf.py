import sys, urllib.request
HDR={'User-Agent':'Mozilla/5.0'}
ident=sys.argv[1]
for leaf in sys.argv[2:]:
    for url in ['https://archive.org/download/%s/page/n%s_w2000.jpg'%(ident,leaf),
                'https://iiif.archive.org/iiif/3/%s$%s/full/max/0/default.jpg'%(ident,leaf)]:
        try:
            d=urllib.request.urlopen(urllib.request.Request(url,headers=HDR),timeout=120).read()
            out='leaf%s.jpg'%leaf; open(out,'wb').write(d); print(out,len(d),url); break
        except Exception as e: print('fail',url,e)
