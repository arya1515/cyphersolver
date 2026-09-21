"""Replay explicit image-audit tokens; never infer missing letters from words."""
import json
from pathlib import Path

root = Path(__file__).resolve().parent
key = json.loads((root / 'audited_key.json').read_text(encoding='utf-8'))['tokens']
audit = json.loads((root / 'body_audit.json').read_text(encoding='utf-8'))
lines = (root / 'body_revision3.txt').read_text().splitlines()
decoded = [''.join(key[t] for t in line.split()) for line in lines]
(root / 'body_revision3_reading.txt').write_text('\n'.join(decoded) + '\n', encoding='utf-8')
for n, line in enumerate(decoded, 1):
    print(f'{n:02} {"audited" if n in audit["audited_lines"] else "DRAFT"}: {line}')
address = json.loads((root / 'address_audited.json').read_text(encoding='utf-8'))
reading = [''.join(address['key'][t] for t in line) for line in address['lines']]
(root / 'address_reading.txt').write_text('\n'.join(reading) + '\n', encoding='utf-8')
print('ADDRESS:', ' / '.join(reading))
