import re,json,sys,urllib.request
ck=open('C:/Users/dbour/cypher/bordeaux/decode/cookie.txt').read().strip()
def get(u,h={}):
    rq=urllib.request.Request(u,headers={'Cookie':ck,'User-Agent':'Mozilla/5.0',**h}); return urllib.request.urlopen(rq,timeout=60).read()
html=get('https://de-crypt.org/decrypt-web/RecordsView/9589').decode('utf-8','replace')
jwt=re.search(r'API_JWT_TOKEN"\s*[:=,]\s*"([^"]+)',html).group(1)
out=open('views.jsonl','a',encoding='utf-8')
for i in sys.argv[1:]:
    v=json.loads(get(f'https://de-crypt.org/decrypt-web/api/view/Records/{i}',{'X-Authorization':'Bearer '+jwt}))
    out.write(json.dumps(v,ensure_ascii=False)+'\n'); out.flush()
    h=get(f'https://de-crypt.org/decrypt-web/RecordsView/{i}').decode('utf-8','replace')
    open(f'rec{i}.htm','w',encoding='utf-8').write(h)
