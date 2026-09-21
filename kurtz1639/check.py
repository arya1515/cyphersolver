"""Print one transcription file line by line with each cipher token's value, for checking against the image.

    python check.py tr/IMG_R4736_I27769_P1.txt
Each line: the line number, the decoded string, then token:value pairs.
"""
import sys
from parse import tokens_of
from decode import loadkey
from solve2 import value

h, s = loadkey()
for n, line in enumerate(open(sys.argv[1], encoding='utf-8'), 1):
    t = line.strip()
    if not t or t == '#' or t.startswith('# '):
        continue
    if t.startswith('##'):
        print(n, t); continue
    pairs, dec = [], []
    for it in tokens_of(t):
        if it[0] == 'clear':
            dec.append('{' + it[1] + '}')
        else:
            v = value(it[1], h, s) if '?' not in it[1] else '?'
            pairs.append(f'{it[1]}:{v}'); dec.append(v)
    print(f'{n:3d} {"".join(dec)}\n    {" ".join(pairs)}')
