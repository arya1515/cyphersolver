# -*- coding: utf-8 -*-
"""Second pass: resolve '?' clusters and cipher glyphs hiding in '~' clusters.

For each glyph in a '?' or '~' cluster, find the nearest centroid among
confidently labelled clusters.  Accept it when the distance is small relative
to that cluster's own spread, or (for '~') when both line neighbours are
already cipher letters and the distance is moderate.
"""
import sys, json
import numpy as np
from collections import defaultdict

def main(sp, inv='clustered.json', out='refined.json'):
    L = {int(k): v for k, v in json.load(open(sp+'/full700.json')).items()}
    D = json.load(open(sp+'/'+inv))
    recs = D['recs']
    Z = np.load(sp+'/Z.npy'); C = np.load(sp+'/C.npy'); keep = np.load(sp+'/keep.npy')
    good = sorted(c for c, v in L.items() if v not in '~?')
    Cg = C[good]
    # spread of each good cluster = median member distance
    spread = {}
    byc = defaultdict(list)
    for zi, ri in enumerate(keep):
        byc[recs[ri]['c']].append(zi)
    for c in good:
        idx = byc.get(c, [])
        spread[c] = float(np.median(np.linalg.norm(Z[idx]-C[c], axis=1))) if idx else 1.0
    zpos = {int(ri): zi for zi, ri in enumerate(keep)}
    # initial letters
    for r in recs:
        r['let'] = L.get(r['c'], '~') if r['c'] >= 0 else '~'
        r['src'] = 'c'
    byline = defaultdict(list)
    for i, r in enumerate(recs): byline[(r['page'], r['line'])].append(i)
    n_q = n_t = 0
    for key, idxs in byline.items():
        idxs.sort(key=lambda i: recs[i]['x0'])
        for p, i in enumerate(idxs):
            r = recs[i]
            if r['let'] not in '?~' or i not in zpos: continue
            z = Z[zpos[i]]
            d = np.linalg.norm(Cg - z, axis=1)
            j = int(d.argmin()); c = good[j]; dd = float(d[j])
            ratio = dd / max(spread[c], 1e-6)
            if r['let'] == '?':
                if ratio < 1.6: r['let'] = L[c]; r['src'] = 'q'; n_q += 1
            else:
                lp = recs[idxs[p-1]]['let'] if p > 0 else '~'
                ln = recs[idxs[p+1]]['let'] if p+1 < len(idxs) else '~'
                ctx = (lp not in '~?') + (ln not in '~?')
                if (ctx == 2 and ratio < 1.5) or ratio < 1.0:
                    r['let'] = L[c]; r['src'] = 't'; n_t += 1
    json.dump(D, open(sp+'/'+out, 'w'))
    print('resolved ?:', n_q, ' recovered from ~:', n_t,
          ' decoded total:', sum(1 for r in recs if r['let'] not in '~?'))

if __name__ == '__main__':
    main(sys.argv[1])
