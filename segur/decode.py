"""Render the letters with a given key. usage: decode.py key.json [files...]
key.json: {"letters": {"13": "a", ...}, "blocks": {"64": "b", ...}, "names": {"pi": "[Casimir]", ...}}
Prints (1) the running text with clear French in upper case and unknown tokens in {}, (2) a token/letter table."""
import json, sys, re
from solve import parse, BLOCK0, NBLK
key = json.load(open(sys.argv[1], encoding='utf-8'))
files = sys.argv[2:] or ['ct_233.txt', 'ct_239.txt', 'ct_288.txt']
L = {int(k): v for k, v in key['letters'].items()}; B = {int(k): v for k, v in key['blocks'].items()}
N = key.get('names', {})
VOW = 'aeiou'
def dec(t):
    t = t.rstrip('?')
    if t.isdigit():
        n = int(t)
        if n in L: return L[n]
        if BLOCK0 <= n < BLOCK0 + 5 * NBLK:
            c = B.get(BLOCK0 + 5 * ((n - BLOCK0) // 5), '?'); return c + VOW[(n - BLOCK0) % 5]
        return '{%s}' % t
    return N.get(t, '{%s}' % t)
for fn in files:
    print('=' * 20, fn)
    for line in open(fn, encoding='utf-8'):
        if line.startswith('#'): continue
        line = line.replace('INS', '[INS]').replace('/INS', '[/INS]')
        out = []
        for part in re.split(r'(\[[^\]]*\])', line.strip()):
            if part.startswith('['): out.append(part[1:-1].upper())
            else: out.append(''.join(dec(t) for t in part.split()))
        print(' '.join(out))
    if '-v' in sys.argv[1:]:
        pass
