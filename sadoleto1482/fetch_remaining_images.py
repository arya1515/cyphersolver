"""Complete the cache for the original/clear witnesses currently under review."""
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
folder = ROOT / 'img/v'
for record in (1283, 1284, 1318, 1319):
    doc = json.loads((ROOT / f'vestigia/v{record}.json').read_text(encoding='utf-8'))['props']['document']
    for entry in doc['files']:
        name = entry['name']
        if any(p.name.endswith(name) for p in folder.iterdir()):
            continue
        target = folder / f'v{record}_additional_{name}'
        req = urllib.request.Request(entry['web_url'], headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read()
        target.write_bytes(data)
        print('saved', target.name, len(data), flush=True)
