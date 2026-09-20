# -*- coding: utf-8 -*-
"""Resolve a transcribed Lope Hurtado token string against key_codes.tsv.
Only 'confirmed' values are applied; 'probable' ones are shown in <angle brackets>
so they can never be mistaken for evidence. Unknown tokens print as ?tok."""
import sys, csv, io, os
HERE = os.path.dirname(os.path.abspath(__file__))
CONF, PROB = {}, {}
for r in csv.reader(io.open(os.path.join(HERE,'key_codes.tsv'), encoding='utf-8'), delimiter='\t'):
    if not r or r[0].startswith('#') or r[0] == 'code':
        continue
    (CONF if len(r) > 2 and r[2] == 'confirmed' else PROB)[r[0]] = r[1]

def one(t):
    if t in CONF: return CONF[t]
    if t in PROB: return '<%s>' % PROB[t]
    return '?' + t

def run(toks):
    out = [one(t) for t in toks]
    hit = sum(1 for o in out if not o.startswith('?'))
    return out, hit, len(out)

if __name__ == '__main__':
    toks = sys.argv[1:] or sys.stdin.read().split()
    out, hit, n = run(toks)
    print(' '.join(out))
    print('coverage: %d/%d tokens = %.0f%%' % (hit, n, 100.0*hit/n if n else 0))
