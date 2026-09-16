# Score a control run: fraction of code groups mapped to the true unit, weighted by occurrence.
import sys, re, ast, collections
key = {}
for line in open('control_key.txt', encoding='utf-8'):
    x, u = line.rstrip('\n').split('\t')
    key[int(x)] = u
segs = []
for line in open('control.txt', encoding='utf-8'):
    for p in line.split(']', 1)[1].split('|'):
        toks = p.split()
        if toks and all(re.fullmatch(r'\d+', t) for t in toks):
            segs += [int(t) for t in toks]
cnt = collections.Counter(segs)
for f in sys.argv[1:]:
    txt = open(f, encoding='utf-8').read()
    m = re.search(r'MAP (\[.*\])', txt, re.S)
    if not m:
        print(f, 'no MAP'); continue
    mp = dict(ast.literal_eval(m.group(1)))
    ok = sum(cnt[c] for c in mp if key.get(c, '').replace('<', '').startswith('null') is False and mp[c] == key.get(c))
    tot = sum(cnt[c] for c in mp if not key.get(c, '').startswith('<null'))
    dist_ok = sum(1 for c in mp if mp[c] == key.get(c))
    best = re.search(r'BEST (-?[\d.]+)', txt)
    print(f, 'tokens correct %d/%d = %.0f%%' % (ok, tot, 100 * ok / tot), 'distinct correct %d/%d' % (dist_ok, len(mp)), 'score', best.group(1) if best else '?')
    wrong = [(c, key.get(c), mp[c], cnt[c]) for c in mp if mp[c] != key.get(c)]
    wrong.sort(key=lambda x: -x[3])
    print('  top wrong (code, true, got, n):', wrong[:15])
