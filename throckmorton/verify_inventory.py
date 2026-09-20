"""Audit cached DECODE image references without exposing authentication data."""
import hashlib, json, pathlib, re
from html import unescape

root = pathlib.Path(__file__).resolve().parent
records = json.loads((root / 'concordance.json').read_text(encoding='utf-8'))
inventory = []
for rid in [r['record'][1:] for r in records] + ['9257', '9260', '9261', '9262']:
    html = (root / f'record_{rid}.html').read_text(encoding='utf-8')
    names = sorted(set(re.findall(r'filesrv/\?file=(?:TH_)?((?:IMG|DOC)_[A-Za-z0-9_.]+)', html)))
    files = []
    for name in names:
        data = (root / 'images' / name).read_bytes()
        assert data[:3] == b'\xff\xd8\xff', name
        files.append(dict(name=name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest()))
    fields = {}
    for field in ['name', 'current_holder', 'author', 'receiver', 'creation_date', 'additional_information']:
        m = re.search(r'<span id="el_records_' + field + r'">(.*?)</span>', html, re.S)
        if m:
            fields[field] = unescape(re.sub('<[^>]+>', ' ', m[1])).strip()
    inventory.append(dict(record='R'+rid, metadata=fields, files=files))
    print('R'+rid, len(files), fields.get('current_holder', ''), fields.get('creation_date', ''))
(root / 'verified_inventory.json').write_text(json.dumps(inventory, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
target = [f for r in inventory[:20] for f in r['files']]
keys = [f for r in inventory[20:] for f in r['files']]
print('Target:',len(target),'references;',len({f['sha256'] for f in target}),'unique images')
print('Keys:',len(keys),'references;',len({f['sha256'] for f in keys}),'unique images')
