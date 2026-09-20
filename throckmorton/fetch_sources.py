"""Fetch only DECODE research sources; never print or copy the session cookie."""
import json, pathlib, re, urllib.request, sys, os

ROOT = pathlib.Path(__file__).resolve().parent
BASE = 'https://de-crypt.org'
cookie_path = pathlib.Path(os.environ.get('DECODE_COOKIE_FILE', str(ROOT.parent / 'bordeaux/decode/cookie.txt')))
cookie = cookie_path.read_text(encoding='utf-8').strip()
cookie = re.sub(r'^cookie:\s*', '', cookie, flags=re.I)

def get(url, authenticated=False):
    headers = {'User-Agent': 'Mozilla/5.0'}
    if authenticated:
        headers['Cookie'] = cookie
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=45) as r:
        data = r.read()
        if 'forbidden' in r.headers.get('Content-Disposition', '').lower() or len(data) == 17947:
            raise RuntimeError('Authentication rejected')
        return data

for rid in sys.argv[1:] or ['9220', '9262']:
    data = get(f'{BASE}/decrypt-web/RecordsView/{rid}', True)
    (ROOT / f'record_{rid}.html').write_bytes(data)
    names = sorted(set(re.findall(r'filesrv/\?file=(?:TH_)?((?:IMG|DOC)_[A-Za-z0-9_.]+)', data.decode('utf-8', errors='replace'))))
    print('record', rid, 'files', names, flush=True)
    for name in names:
        out = ROOT / 'images' / name
        out.parent.mkdir(exist_ok=True)
        if out.exists():
            continue
        image = get(f'{BASE}/decrypt-custom/filesrv/?file={name}', True)
        out.write_bytes(image)
        print(name, len(image), flush=True)
