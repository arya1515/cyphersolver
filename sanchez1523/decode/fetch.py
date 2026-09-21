import os,re,sys,time,urllib.request
HERE=os.path.dirname(os.path.abspath(__file__))
IMG=os.path.join(os.path.dirname(HERE),"img"); os.makedirs(IMG,exist_ok=True)
BASE="https://de-crypt.org"; FORB=17947
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"
ck=re.sub(r'^cookie:\s*','',open(os.path.join(HERE,'cookie.txt'),encoding='utf-8').read().strip(),flags=re.I)
op=urllib.request.build_opener(urllib.request.ProxyHandler({}))
for rec in [int(x) for x in sys.argv[1:]]:
    h=open(os.path.join(HERE,"rec%d.htm"%rec),encoding='utf-8',errors='ignore').read()
    for name in sorted(set(re.findall(r'filesrv/\?file=TH_([A-Za-z0-9_.]+)',h))):
        out=os.path.join(IMG,name)
        if os.path.exists(out) and os.path.getsize(out) not in (0,FORB): print(rec,name,"have"); continue
        r=urllib.request.Request(BASE+"/decrypt-custom/filesrv/?file="+name,headers={
            "User-Agent":UA,"Cookie":ck,"Referer":BASE+"/decrypt-web/RecordsView/%d"%rec})
        try: d=op.open(r,timeout=180).read()
        except Exception as e: print(rec,name,"ERR",e); continue
        if len(d)==FORB: print(rec,name,"FORBIDDEN (cookie stale)"); sys.exit(1)
        open(out,"wb").write(d); print(rec,name,len(d))
        time.sleep(0.5)
