"""Re-decode f. 55 under the LM, giving the confusable homophones (r/s, e/o, l/t) both values."""
import re, sys
src = open('decode.py', encoding='utf-8').read()
ns = {}
exec(src.split('for n in sorted')[0], ns)
MAP, LINES = ns['MAP'], ns['LINES']
ALT = {'r':'r|s','s':'s|r','e':'e|o','o':'o|e','l':'l|t','t':'t|l','c':'c|i','i':'i|c'}
from lattice import decode
prev = 'cestpour'
for n in sorted(LINES):
    cands = []
    for t in LINES[n].split():
        v = MAP.get(t)
        if v is None: cands.append(['-'])
        elif v == '': cands.append(['-'])
        elif len(v) == 1: cands.append(ALT.get(v, v).split('|'))
        else: cands.append([v])
    best = decode(cands, beam=800, prefix=prev[-8:])[0][1][len(prev[-8:]):]
    print('%2d %s' % (n, best)); prev += best
