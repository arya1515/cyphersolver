"""Decode cipher.txt with the three-grid pigpen key of the Wilkes/Needham-Walsingham cipher.

Shapes in grid order (top-left to bottom-right): J U L / C O F / N 7 D.
Plain = a-i, dot below = k-s (no j), dot inside = t u w x y z (u = v).
"""
import sys

SHAPES = 'J U L C O F N 7 D'.split()
KEY = {}
for i, s in enumerate(SHAPES):
    KEY[s] = 'abcdefghi'[i]
    KEY[s + '.'] = 'klmnopqrs'[i]
    if i < 6:
        KEY[s + ':'] = 'tuwxyz'[i]

def decode(tokens):
    out = []
    for t in tokens:
        out.append(' ' if t == '|' else KEY.get(t, '?'))
    return ''.join(out)

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else __file__.replace('decode.py', 'cipher.txt')
    for line in open(path, encoding='utf8'):
        if line.startswith('#') or not line.strip():
            continue
        head, _, rest = line.partition('  ')
        print(f'{head:10s}', decode(rest.split()))
