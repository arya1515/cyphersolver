"""Retrieve the five authorized DECODE records; never print or copy the cookie."""
import pathlib, re, urllib.request, json
ROOT = pathlib.Path(__file__).resolve().parent
COOKIE = ROOT.parent / 'bordeaux/decode/cookie.txt'
cookie = re.sub(r'^cookie:\s*', '', COOKIE.read_text(encoding='utf-8').strip(), flags=re.I)
base = 'https://de-crypt.org'
for rid in [1140,1141,1142,1143,1154]:
    url = f'{base}/decrypt-web/RecordsView/{rid}'
    req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0','Cookie':cookie})
    html = urllib.request.urlopen(req,timeout=60).read()
    (ROOT/'sources'/f'decode-{rid}.html').write_bytes(html)
    names = sorted(set(re.findall(r'filesrv/\?file=TH_([A-Za-z0-9_.]+)',html.decode('utf-8','replace'))))
    print(rid, names, flush=True)
    for name in names:
        out=ROOT/'img'/name
        out.parent.mkdir(exist_ok=True)
        if out.exists(): continue
        req=urllib.request.Request(base+'/decrypt-custom/filesrv/?file='+name,headers={'User-Agent':'Mozilla/5.0','Cookie':cookie,'Referer':url})
        with urllib.request.urlopen(req,timeout=60) as r:
            data=r.read()
            if len(data)==17947 or 'forbidden' in r.headers.get('Content-Disposition','').lower():
                raise SystemExit('Stored cookie rejected; no image saved.')
        out.write_bytes(data)
        print(name,len(data),flush=True)
