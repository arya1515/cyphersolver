"""uscompare.py -- convergence check across usolve runs: token-weighted agreement of the unit mappings.
usage: python uscompare.py us_real_11.json us_real_12.json ...
"""
import sys, json, itertools
truth = None
if '--truth' in sys.argv:
    i = sys.argv.index('--truth'); truth = json.load(open(sys.argv[i+1]))['key']; del sys.argv[i:i+2]
runs = [json.load(open(f)) for f in sys.argv[1:]]
names = [f.split('_')[-1].split('.')[0] for f in sys.argv[1:]]
code_to_plain = {}
if truth:
    for e, c in truth.items(): code_to_plain.setdefault(c.lstrip('.'), []).append(('.' if c.startswith('.') else '') + e)
for r, n in zip(runs, names):
    print(f'seed {n}: score {r["score"]:.1f}' + (f'  accuracy {r["accuracy"]:.3f}' if 'accuracy' in r else ''))
counts = runs[0]['counts']; tot = sum(counts.values())
print('\npairwise token-weighted agreement (same element, or overlapping polyphonic set):')
for (i, a), (j, b) in itertools.combinations(enumerate(runs), 2):
    agree = 0
    for s, c in counts.items():
        if s in a['mapping'] and s in b['mapping'] and set(a['mapping'][s]) & set(b['mapping'][s]): agree += c
    print(f'  {names[i]} vs {names[j]}: {agree/tot:.3f}')
print('\nper-unit mappings (units with >= 30 tokens):')
for s, c in sorted(counts.items(), key=lambda kv: -kv[1]):
    if c < 30: break
    tr = ('  TRUE:' + '/'.join(code_to_plain.get(s.rstrip('.'), ['-']))) if truth else ''
    print(f'  {s:>4} {c:4d}  ' + '  '.join(f"{n}:{'/'.join(r['mapping'].get(s, ['?']))}" for r, n in zip(runs, names)) + tr)
