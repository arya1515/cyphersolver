"""Decode with a given systematic key and print details (UTF-8 to file)."""
import sys, os, io
sys.stdout = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'show_out.txt'), 'w', encoding='utf-8')
here = os.path.dirname(os.path.abspath(__file__))
from family import make_table, decode_segments, code2ch, segs, CONS, VOW, tokens, lp
import math

def key_from_name(cname, vo, fill, off):
    base = list(CONS)
    r = int(cname[3:]); rot = base[r:] + base[:r]
    if cname.startswith('rev'): rot = rot[::-1]
    return make_table(rot, list(vo), fill, off), rot

if __name__ == '__main__':
    cname, vo, fill, off, add = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
    tbl, rot = key_from_name(cname, vo, fill, off)
    print('consonant order', ''.join(rot), 'vowels', vo, fill, 'offset', off, 'additive', add)
    # print table
    print('    ' + '  '.join(vo))
    for c in rot:
        print(c, ' ', ' '.join('%02d' % tbl[c + v] for v in vo))
    print()
    # full token stream decode with positions
    print('tokens:', ' '.join(tokens))
    for seg, (sc, codes) in zip(segs, decode_segments(tbl, add)):
        nums = ['%02d' % tbl[s] for s in seg]
        print('segment', ' '.join(seg))
        print('        ', ' '.join(nums))
        print('  codes ', ' '.join(codes))
        print('  chars ', ' '.join(code2ch.get(c, '□') for c in codes), ' score %.1f' % sc)
        print()
