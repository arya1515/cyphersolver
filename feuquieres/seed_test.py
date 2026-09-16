# How much crib does the control need?  Fix a fraction of the true mapping (by distinct group, chosen at random)
# and let the n-gram solver fill the rest; report recovery of the unfixed tokens.
# usage: python -X utf8 -u seed_test.py iters frac [frac ...]   -> seed_test.txt
import sys, random
argv = sys.argv; sys.argv = ['x']
import solver as S
iters = int(argv[1]); fracs = [float(x) for x in argv[2:]]
toks = S.parse('control.txt'); key = {}
for l in open('control_key.txt', encoding='utf-8'):
    n, u = l.rstrip('\n').split('\t'); key[int(n)] = u
truth = {c: key[c] for c in set(toks)}
S.CRIBW = 0.0
low, high = S.inventory(); pri = S.unit_prior(set(low + high))
out = open('seed_test.txt', 'a', encoding='utf-8')
for f in fracs:
    random.seed(7)
    codes = sorted(truth); random.shuffle(codes)
    fixed = {c: truth[c] for c in codes[:int(f * len(codes))]}
    s = S.Solver(toks, low, high, pri, fixed=fixed)
    best = s.anneal(iters, log=0)
    free = [t for t in toks if t not in fixed]
    hit = sum(1 for t in free if s.map[t] == truth[t])
    s2 = S.Solver(toks, low, high, pri, fixed=fixed); s2.map = dict(truth); ts = s2.total()
    line = f'fixed {f:.0%} of groups ({len(fixed)}): unfixed tokens recovered {hit}/{len(free)} = {100*hit/max(1,len(free)):.0f}%; best {best:.1f} truth {ts:.1f}\n    {s.render()[:160]}\n'
    print(line, flush=True); out.write(line); out.flush()
out.write('done\n')
