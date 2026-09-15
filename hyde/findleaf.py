import sys, json, gzip, urllib.request, re
HDR={'User-Agent':'Mozilla/5.0'}
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=HDR), timeout=120).read()
ident=sys.argv[1]
pat=sys.argv[2]
base='https://archive.org/download/%s/%s'%(ident,ident)
try:
    idx=json.loads(gzip.decompress(open(ident+'_pageindex.json.gz','rb').read()))
    txt=gzip.decompress(open(ident+'_searchtext.txt.gz','rb').read()).decode('utf-8')
except FileNotFoundError:
    a=get(base+'_hocr_pageindex.json.gz'); open(ident+'_pageindex.json.gz','wb').write(a)
    b=get(base+'_hocr_searchtext.txt.gz'); open(ident+'_searchtext.txt.gz','wb').write(b)
    idx=json.loads(gzip.decompress(a)); txt=gzip.decompress(b).decode('utf-8')
# idx: list of [start,end] byte offsets per page (utf-8)
raw=txt.encode('utf-8')
for i,ent in enumerate(idx):
    s,e=ent[0],ent[1]
    page=raw[s:e].decode('utf-8','replace')
    if re.search(pat,page):
        print('leaf',i, '|', re.sub(r'\s+',' ',page)[:200])
