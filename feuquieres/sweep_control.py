# Calibration sweep on the synthetic control: for several objective weightings, decompose the score of the true key
# and of the solver's best solution, and report token recovery.  Writes sweep_control.txt as it goes.
# usage: python -u sweep_control.py iters
import sys, random, re, os, importlib
iters = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
sys.argv = ['x']
import solver as S

def decompose(s, m):
    t = ''.join(m[x] for x in s.toks)
    lmsc = S.lm.score(t); letters = len(t)
    nulls = sum(1 for c in s.codes if m[c] == S.NULL)
    pri = sum(s.logpri[m[c]] for c in s.codes)
    crib = sum(len(w) * min(t.count(w), 2) for w in s.cribs)
    return dict(lm=round(lmsc, 1), letters=letters, nulls=nulls, prior=round(pri, 1), crib=crib)

toks = S.parse('control.txt')
key = {}
for l in open('control_key.txt', encoding='utf-8'):
    n, u = l.rstrip('\n').split('\t'); key[int(n)] = u
truth = {c: key[c] for c in set(toks)}
out = open('sweep_control.txt', 'a', encoding='utf-8')
configs = [(0.7, 1.0, 4.0), (0.7, 1.0, 0.0), (0.3, 1.0, 2.0), (0.7, 0.3, 2.0), (0.3, 0.3, 0.0), (1.0, 0.3, 2.0)]
for lam, pw, cw in configs:
    S.LAMBDA, S.PRIORW, S.CRIBW = lam, pw, cw
    low, high = S.inventory(); pri = S.unit_prior(set(low + high))
    random.seed(1)
    s = S.Solver(toks, low, high, pri)
    s.map = dict(truth); ts = s.total(); td = decompose(s, truth)
    s = S.Solver(toks, low, high, pri)
    best = s.anneal(iters, log=0)
    hit = sum(1 for t in toks if s.map[t] == truth[t]); bd = decompose(s, s.map)
    line = (f'LAMBDA={lam} PRIORW={pw} CRIBW={cw} | truth {ts:.1f} {td} | best {best:.1f} {bd} | '
            f'recovered {hit}/{len(toks)} ({100*hit/len(toks):.0f}%)\n    {s.render()[:160]}\n')
    print(line, flush=True); out.write(line); out.flush()
out.write('done\n'); out.close()
