"""Render the two letters with a hand-built key. Unknown symbols shown as [N]."""
import sys
from parse import load, is_cipher

KEY = {
    '10': 'c', '11': 'b', '14': 'l', '16': 'r', '18': 't', '19': 'a', '20': 'd', '21': 'i', '22': 'n',
    '24': 'm', '25': 's', '26': 'u', '27': 'e', '28': 'q', '29': 'a', '30': 'e', '34': 'a', '35': 'e',
    '36': 'i', '37': 'o',
}
# extra assignments can be passed on the command line:  13=p 23=h ...
for kv in sys.argv[1:]:
    k, v = kv.split('='); KEY[k] = v

def sym(t):
    if t.startswith('~'):
        b = KEY.get(t[1:]); return (b * 2) if b else f'[{t}]'
    n = int(t)
    if n >= 41: return f'{{{t}}}'
    return KEY.get(t, f'[{t}]')

for name, lines in load().items():
    print('---', name)
    for toks in lines:
        out = []
        for t in toks:
            out.append(sym(t) if is_cipher(t) else ' ' + t.replace('_', ' ') + ' ')
        print(''.join(out))
