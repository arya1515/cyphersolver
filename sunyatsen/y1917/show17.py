import sys, os, io
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from family import code2ch, CONS, make_table
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
base = list(CONS); ROT = base[7:] + base[:7]
T = make_table(ROT, list('aeuoi'), 'vow', 1)
INV = {v: k for k, v in T.items()}
if __name__ == '__main__':
    print('consonants', ''.join(ROT), 'vowels aeuoi, vowel-major, 01..99,00')
    print('     ' + '   '.join('aeuoi'))
    for c in ROT: print(c, '  ', ' '.join('%02d' % T[c+v] for v in 'aeuoi'))
    s = sys.argv[1] if len(sys.argv) > 1 else ''
    for a in (0, 1):
        sy = [s[i:i+2] for i in range(a, len(s)-1, 2)]
        n = ['%02d' % T[x] if x in T else '??' for x in sy]
        c = [n[i]+n[i+1] for i in range(0, len(n)-1, 2)]
        print(a, ' '.join('%s%s=%s%s' % (sy[2*i], sy[2*i+1], cc, code2ch.get(cc, '□')) for i, cc in enumerate(c)))
