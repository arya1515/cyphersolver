"""Retrieve public catalogued June 24 images as possible key controls."""
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent
document = json.loads((ROOT / 'vestigia/v1280.json').read_text(encoding='utf-8'))['props']['document']
for index, item in enumerate(document['files'], 1):
    target = ROOT / 'img/v' / f'control1280_{index}.jpg'
    if not target.exists():
        with urllib.request.urlopen(item['web_url'], timeout=45) as response:
            data = response.read()
        target.write_bytes(data)
    print(index, item['name'], target.stat().st_size, flush=True)
