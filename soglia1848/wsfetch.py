import json,urllib.request,re,html,sys,urllib.parse
def get(title):
    u='https://it.wikisource.org/w/api.php?action=parse&format=json&prop=text&page='+urllib.parse.quote(title)
    r=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0 research'}),timeout=60)
    d=json.load(r); t=d['parse']['text']['*']
    t=re.sub(r'<br\s*/?>','\n',t); t=re.sub(r'</p>','\n\n',t); t=re.sub(r'<[^>]+>','',t); t=html.unescape(t)
    return t
if __name__=='__main__':
    t=get(sys.argv[1]); open(sys.argv[2],'w',encoding='utf8').write(t); print(len(t))
