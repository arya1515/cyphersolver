# -*- coding: utf-8 -*-
"""Decode with the 700-cluster label table."""
import sys, json
from collections import defaultdict

def load(sp):
    return {int(k): v for k, v in json.load(open(sp+'/full700.json')).items()}

def main(sp, page=None):
    L = load(sp)
    D = json.load(open(sp+'/clustered.json'))
    recs = [r for r in D['recs'] if page is None or r['page'] == page]
    byline = defaultdict(list)
    for r in recs: byline[(r['page'], r['line'])].append(r)
    for k in sorted(byline):
        rs = sorted(byline[k], key=lambda r: r['x0'])
        out = []
        for r in rs:
            ch = L.get(r['c'], '~')
            out.append('.' if ch == '~' else ('*' if ch == '?' else ch))
        print('%s L%02d  %s' % (k[0], k[1], ''.join(out)))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
