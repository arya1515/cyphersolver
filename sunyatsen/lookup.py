"""Lookup helper: python lookup.py 1842 5065 5068 3888 1979 ; ranges like 1830-1850 ; chars like 梅"""
import sys, os, csv
here = os.path.dirname(os.path.abspath(__file__))
out = open(os.path.join(here, 'lookup_out.txt'), 'w', encoding='utf-8')
tw, cn = {}, {}
for name, d in (('tw.csv', tw), ('cn.csv', cn)):
    for row in csv.DictReader(open(os.path.join(here, name), encoding='utf-8')):
        d[row['code']] = row['character']
ch2 = {v: k for k, v in tw.items()}
for a in sys.argv[1:]:
    if '-' in a:
        lo, hi = a.split('-')
        for n in range(int(lo), int(hi) + 1):
            c = '%04d' % n
            print(c, tw.get(c, '·'), cn.get(c, '·'), file=out)
    elif a.isdigit():
        print(a, 'tw:', tw.get(a, '·'), 'cn:', cn.get(a, '·'), file=out)
    else:
        for ch in a:
            print(ch, ch2.get(ch, '?'), file=out)
out.close()
