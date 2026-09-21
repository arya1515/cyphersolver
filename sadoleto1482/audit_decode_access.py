"""Read DECODE record attachment listings without printing credentials."""
import html
import json
from pathlib import Path
import re
import sys
import urllib.request

ROOT = Path(__file__).resolve().parent
cookie = (ROOT.parent / 'bordeaux/decode/cookie.txt').read_text(encoding='utf-8').strip()
cookie = re.sub(r'^cookie:\s*', '', cookie, flags=re.I)
if '--image-test' in sys.argv:
    url = 'https://de-crypt.org/decrypt-custom/filesrv/?file=IMG_R1101_I5655_P2.png'
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0', 'Cookie': cookie,
        'Referer': 'https://de-crypt.org/decrypt-web/RecordsView/1101'})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read()
        disposition = response.headers.get('Content-Disposition', '')
        content_type = response.headers.get('Content-Type', '')
    from hashlib import sha256
    old = (ROOT / 'img/IMG_R1101_I5655_P2.png').read_bytes()
    result = {'bytes': len(data), 'content_type': content_type,
              'forbidden_disposition': 'forbidden' in disposition.lower(),
              'matches_cached_image': sha256(data).digest() == sha256(old).digest(),
              'known_forbidden_size': len(data) == 17947}
    (ROOT / 'decode_image_access_test.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))
    sys.exit(0)
results = []
for record in (1101, 1102, 1103, 1106):
    for page in ('RecordsView', 'DocumentsList', 'AssociatedRecordsList', 'ImagesList'):
        route = f'{page}/{record}' if page == 'RecordsView' else f'{page}?showmaster=records&fk_id={record}'
        url = 'https://de-crypt.org/decrypt-web/' + route
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Cookie': cookie})
        with urllib.request.urlopen(req, timeout=45) as response:
            text = response.read().decode('utf-8', errors='replace')
            final_url = response.url
        tables = re.findall(r'<table\b.*?</table>', text, flags=re.S | re.I)
        clean = []
        for table in tables:
            table = re.sub(r'<script\b.*?</script>', '', table, flags=re.S | re.I)
            plain = html.unescape(re.sub(r'<[^>]*>', ' ', table))
            plain = re.sub(r'\s+', ' ', plain).strip()
            clean.append(plain)
        row = {'record': record, 'page': page,
               'login_reported': bool(re.search(r'"isLoggedIn"\s*:\s*true', text)),
               'redirected_to_login': '/login' in final_url.lower(),
               'images': sorted(set(re.findall(r'(?:TH_)?(IMG_R\d+_I\d+_P[^"&<>\s]+)', text))),
               'no_records_reported': 'No records found' in text,
               'tables': clean}
        results.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
        (ROOT / 'decode_access_audit.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
