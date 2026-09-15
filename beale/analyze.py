"""Summarise results_gutenberg.tsv: per (mode,cipher) top rows by stage-2 quad score and by stage-1 mean."""
import sys, csv, collections
rows = []
for line in open('results_gutenberg.tsv', encoding='utf-8', errors='ignore'):
    p = line.rstrip('\n').split('\t')
    if len(p) < 12: continue
    bid, title, auth, nw, mode, cn, o, mean, cv, z, q, d = p[:12]
    rows.append(dict(id=bid, title=title, auth=auth, nw=int(nw), mode=mode, cn=cn, o=int(o), mean=float(mean), cv=float(cv), z=float(z), q=float(q) if q else None, d=d))
print('rows', len(rows), 'books', len({r['id'] for r in rows}))
by = collections.defaultdict(list)
for r in rows: by[(r['mode'], r['cn'])].append(r)
for k, rs in sorted(by.items()):
    qs = [r for r in rs if r['q'] is not None]
    print(f"\n== {k[0]} {k[1]}: {len(rs)} rows, {len(qs)} stage-2 evaluated")
    for r in sorted(qs, key=lambda r: -r['q'])[:8]:
        print(f"  quad {r['q']:.2f} mean {r['mean']:.3f} z {r['z']:.1f} off {r['o']} | #{r['id']} {r['title'][:45]} / {r['auth'][:25]}")
