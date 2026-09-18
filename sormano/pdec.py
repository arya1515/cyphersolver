# -*- coding: utf-8 -*-
"""Print predicted plaintext per line from pred.json."""
import sys, os, json
from collections import defaultdict
SP = sys.argv[1]; tag = sys.argv[2] if len(sys.argv) > 2 else None
l0 = int(sys.argv[3]) if len(sys.argv) > 3 else 0
l1 = int(sys.argv[4]) if len(sys.argv) > 4 else 999
recs = json.load(open(os.path.join(SP, 'inv.json')))['recs']
pred = json.load(open(os.path.join(SP, 'pred.json')))
byline = defaultdict(list)
for r, p in zip(recs, pred):
    if tag and r['page'] != tag: continue
    if not (l0 <= r['line'] <= l1): continue
    byline[(r['page'], r['line'])].append((r['x0'], r['x1'], p))
for k in sorted(byline):
    rs = sorted(byline[k])
    out = []
    prev = None
    for x0, x1, p in rs:
        if prev is not None and x0-prev > 26: out.append(' ')
        out.append(p); prev = x1
    print('%s L%02d %s' % (k[0], k[1], ''.join(out)))
