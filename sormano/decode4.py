# -*- coding: utf-8 -*-
import sys, json
from collections import defaultdict
def main(sp, page=None, f='refined.json'):
    D = json.load(open(sp+'/'+f))
    byline = defaultdict(list)
    for r in D['recs']:
        if page is None or r['page'] == page: byline[(r['page'], r['line'])].append(r)
    for k in sorted(byline):
        rs = sorted(byline[k], key=lambda r: r['x0'])
        print('%s L%02d  %s' % (k[0], k[1], ''.join(
            '.' if r['let'] == '~' else ('*' if r['let'] == '?' else r['let']) for r in rs)))
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
