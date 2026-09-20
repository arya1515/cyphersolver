import os,sys,re,time,urllib.request
HERE=os.path.dirname(os.path.abspath(__file__))
BASE="https://de-crypt.org"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
op=urllib.request.build_opener(urllib.request.ProxyHandler({}))
for rec in range(int(sys.argv[1]),int(sys.argv[2])+1):
    p=os.path.join(HERE,"rec%d.htm"%rec)
    if os.path.exists(p) and os.path.getsize(p)>2000: continue
    try:
        r=urllib.request.Request(BASE+"/decrypt-web/RecordsView/%d"%rec,headers={"User-Agent":UA})
        open(p,"wb").write(op.open(r,timeout=60).read())
        print(rec,"ok",os.path.getsize(p))
    except Exception as e:
        print(rec,"ERR",e)
    time.sleep(0.4)
