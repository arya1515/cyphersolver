"""Emit the merged THE=972 table as a JS object for docs/armstrong.html:  {num: [reading, conf]}
conf: H = pencil interlinear decode (roll 13), C = cryptiana known-plaintext, M = uncertain pencil read, I = inferred."""
import json, sys
sys.argv = ['x', 'none']
import decode972 as d

out = {}
for n in sorted(d.tab):
    b = d.best(n)
    if b is None:
        continue
    r, c = b
    if '...' in r or 'null' in r:
        continue
    out[n] = [r.strip(), 'I' if c == '?' else c]
print('const KEY =', json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';')
print('//', len(out), 'entries', file=sys.stderr)
