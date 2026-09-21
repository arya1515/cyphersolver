"""Retrieve the previously uncached Hungarian-archive images for R1102."""
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
doc = json.loads((ROOT / 'vestigia/v1286.json').read_text(encoding='utf-8'))['props']['document']
for entry in doc['files']:
    name = entry.get('name', '')
    if not name.startswith('HU_MNL_OL_X_10891_DF_294367_'):
        continue
    target = ROOT / 'img/v' / ('v1286_mnl_' + name)
    if target.exists():
        print('cached', target.name, target.stat().st_size)
        continue
    request = urllib.request.Request(entry['web_url'], headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    target.write_bytes(data)
    print('saved', target.name, len(data))
