import sys, json, urllib.request, urllib.parse, os
HDR={'User-Agent':'Mozilla/5.0'}
def get(url, out=None):
    r=urllib.request.Request(url, headers=HDR)
    data=urllib.request.urlopen(r, timeout=60).read()
    if out:
        open(out,'wb').write(data); print('saved',out,len(data))
    return data

if sys.argv[1]=='imgs':
    for n in ['charlesii2a.jpg','charlesii2.jpg','charlesii2b.jpg','charlesii2c.jpg','charlesii3.jpg','kingston1.jpg']:
        try: get('https://cryptiana.web.fc2.com/code/'+n, 'img_'+n)
        except Exception as e: print(n, e)
elif sys.argv[1]=='search':
    q=sys.argv[2]
    url='https://archive.org/advancedsearch.php?'+urllib.parse.urlencode({'q':q,'fl[]':['identifier','title','year','creator'],'rows':50,'output':'json'}, doseq=True)
    d=json.loads(get(url))
    for doc in d['response']['docs']:
        print(doc.get('identifier'),'|',doc.get('year'),'|',str(doc.get('title'))[:90],'|',str(doc.get('creator'))[:40])
elif sys.argv[1]=='files':
    ident=sys.argv[2]
    d=json.loads(get('https://archive.org/metadata/'+ident))
    for f in d['files']:
        if f['name'].endswith(('.txt','djvu.xml','.pdf')) or 'ocr' in f['name'].lower(): print(f['name'], f.get('size'))
elif sys.argv[1]=='get':
    get(sys.argv[2], sys.argv[3])
