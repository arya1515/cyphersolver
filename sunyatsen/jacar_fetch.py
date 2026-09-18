"""Fetch a JACAR item: metadata text (printed) and the raw PDF (saved to jacar/<ref>.pdf).
The raw path is embedded in the /das/image/<ref> page."""
import sys, re, html, os, urllib.request, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
here = os.path.dirname(os.path.abspath(__file__))
B = 'https://www.jacar.archives.go.jp'
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=120).read()
def meta(ref):
    t = get(B + '/das/meta/' + ref).decode('utf-8', 'replace')
    t = re.sub(r'<script.*?</script>', '', t, flags=re.S); t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    t = re.sub(r'\s+', ' ', t); i = t.find('件名標題'); j = t.find('URIをコピー')
    return t[i:j]
def pdf(ref):
    p = os.path.join(here, 'jacar', ref + '.pdf')
    if os.path.exists(p): return p
    t = get(B + '/das/image/' + ref).decode('utf-8', 'replace')
    m = re.search(r'"path":"([^"]+?\.pdf)"', t)
    open(p, 'wb').write(get(B + m.group(1).replace(chr(92), '')))
    return p
if __name__ == '__main__':
    for ref in sys.argv[1:]:
        print('=====', ref); print(meta(ref)[:4000])
        if '--pdf' in os.environ.get('JF', ''): print(pdf(ref))
