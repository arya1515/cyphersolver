import json,re,os,time,urllib.request
C=open('bordeaux/decode/cookie.txt').read().strip()
def get(u):
  for t in range(6):
    try: return get1(u)
    except Exception as e: time.sleep(10*(t+1))
  return b''
def get1(u):
    r=urllib.request.Request(u,headers={'Cookie':C,'User-Agent':'Mozilla/5.0'}); return urllib.request.urlopen(r,timeout=60).read()
ids=[]
for l in open('it1583/sforza_views.jsonl',encoding='utf8'):
    v=json.loads(l); v=v[0] if isinstance(v,list) else v
    ids.append((v['id'],v.get('name','')))
for i,n in ids:
    h=get('https://de-crypt.org/decrypt-web/RecordsView/%s'%i).decode('utf8','ignore')
    for th in sorted(set(re.findall(r'filesrv/\?file=(IMG_R\d+_I\d+_P)\.(\w+)',h))):
        fn='it1583/keys/%s_%s.%s'%(n or i,th[0],th[1])
        if os.path.exists(fn): continue
        for ext in (th[1],'jpg','png'):
            b=get('https://de-crypt.org/decrypt-custom/filesrv/?file=%s.%s'%(th[0],ext))
            if len(b)!=17947 and len(b)>6000: open(fn.rsplit('.',1)[0]+'.'+ext,'wb').write(b); break
    time.sleep(.2)
print('done')
