import sys, os, solve
HERE = os.path.dirname(os.path.abspath(__file__))
lp = solve.bigrams([sys.argv[1]])
d = solve.load()
for line in open(os.path.join(HERE, 'runs.txt'), encoding='utf8'):
    if line.startswith('#') or '|' not in line: continue
    rid, b, w, a = [x.strip() for x in line.split('|')]
    signs = [x for x in w.split() if not x.startswith('[')]
    print(rid, '...', b[-30:], '|', ' / '.join(' '.join(o) for s, o in solve.phrase(b, signs, a, d, lp)), '|', a[:30])
