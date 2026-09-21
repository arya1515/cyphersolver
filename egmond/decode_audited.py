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

# Preserve the main-line transcript and replay insertions separately in their
# manuscript order. Token anchors are checked against the visible neighbours.
complete = decoded.copy()
for n, anchor in [(7, ['B', 'V', 'CE']), (15, ['J', 'V', 'CE'])]:
    insertion = json.loads((root / f'insertion{n}.json').read_text())
    tokens = lines[n - 1].split()
    matches = [i for i in range(len(tokens) - len(anchor) + 1)
               if tokens[i:i + len(anchor)] == anchor]
    assert len(matches) == 1, (n, matches)
    i = matches[0]
    added = ''.join(key[t] for t in insertion['tokens'])
    assert added == insertion['reading']
    complete[n - 1] = (''.join(key[t] for t in tokens[:i]) + '{' + added + '}'
                       + ''.join(key[t] for t in tokens[i:]))
(root / 'complete_raw_reading.txt').write_text('\n'.join(complete) + '\n', encoding='utf-8')
edition = json.loads((root / 'diplomatic_lines.json').read_text(encoding='utf-8'))
assert len(edition) == len(complete)
for n, (spaced, raw) in enumerate(zip(edition, complete), 1):
    assert ''.join(spaced.lower().split()) == raw, (n, spaced, raw)
all_tokens = [t for line in lines for t in line.split()]
for n in (7, 15):
    all_tokens += json.loads((root / f'insertion{n}.json').read_text())['tokens']
(root / 'body_complete_tokens.txt').write_text(' '.join(all_tokens) + '\n')
print('BODY WITH INSERTIONS:', '\n'.join(complete))
