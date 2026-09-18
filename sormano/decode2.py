# -*- coding: utf-8 -*-
"""Render decoded cipher text per line, with clear-hand runs marked."""
import sys, json
from collections import defaultdict
import labels

def main(jsonf, page=None):
    D = json.load(open(jsonf))
    recs = [r for r in D['recs'] if page is None or r['page'] == page]
    byline = defaultdict(list)
    for r in recs: byline[(r['page'], r['line'])].append(r)
    L = labels.L
    for k in sorted(byline, key=lambda k: (k[0], k[1])):
        rs = sorted(byline[k], key=lambda r: r['x0'])
        out = []
        for r in rs:
            ch = L.get(r['c'], '~')
            if ch == '~': out.append('.')
            elif ch == '?': out.append('*')
            else: out.append(ch)
        print('%s L%02d  %s' % (k[0], k[1], ''.join(out)))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
