import re,urllib.request,glob,os
ck=open('C:/Users/dbour/cypher/bordeaux/decode/cookie.txt').read().strip()
os.makedirs('img',exist_ok=True)
for f in glob.glob('rec*.htm'):
    for n in sorted(set(re.findall(r'filesrv/\?file=TH_((?:IMG|DOC)_[^"\'&]+)',open(f,encoding='utf-8').read()))):
        rq=urllib.request.Request('https://de-crypt.org/decrypt-custom/filesrv/?file='+n,headers={"Referer":"https://de-crypt.org/decrypt-web/RecordsView/1","Cookie":ck,'User-Agent':'Mozilla/5.0'})
        open('img/'+n,'wb').write(urllib.request.urlopen(rq,timeout=120).read()); print(n)
    for n in sorted(set(re.findall(r'filesrv/\?file=(DOC_[^"\'&]+)',open(f,encoding='utf-8').read()))): print('DOC',n)
