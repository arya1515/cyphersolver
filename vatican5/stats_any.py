import sys, collections
p = sys.argv[1]
toks = []
for line in open(p):
    toks += line.split()
d = [t[0] for t in toks]
c = collections.Counter(d); n = len(d)
print('digits', n, ' '.join(f'{k}:{c[k]}' for k in sorted(c)))
bg = collections.Counter(a + b for a, b in zip(d, d[1:]))
print('    ' + ''.join(f'{x:>5}' for x in '0123456789'))
for a in '0123456789': print(f'{a}   ' + ''.join(f'{bg[a+b]:>5}' for b in '0123456789'))
print('doubles', sum(bg[x+x] for x in '0123456789'), 'top', bg.most_common(12))
