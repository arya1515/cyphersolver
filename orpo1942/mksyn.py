import random, sys, dk, build_lm
L = int(sys.argv[1]); lens = [int(x) for x in sys.argv[2].split(',')]; seed = int(sys.argv[3]); out = sys.argv[4]
R = random.Random(seed)
txt = build_lm.clean(list(build_lm.texts())[2])
A = list(dk.AL); B = list(dk.AL); R.shuffle(A); R.shuffle(B); A = ''.join(A); B = ''.join(B)
with open(out, 'w') as f:
    f.write('# key %s %s\n' % (A, B))
    for i, n in enumerate(lens):
        s = R.randrange(10000, len(txt) - 1000); P = txt[s:s + n]
        f.write('# P%d %s\n' % (i, P))
        f.write('m%d\t%s\n' % (i, dk.encrypt(A, B, P, L)))
print(A, B)
