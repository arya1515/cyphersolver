# Annealer over H+F with the hand-derived partial key fixed, LM + prior only (no crib bonus).
import sys, random
import solver as S, solver_gc as G, solver_trad as T
sys.stdout.reconfigure(encoding='utf-8')
iters = int(sys.argv[1]); seed = int(sys.argv[2])
random.seed(seed)
S.CRIBW = 0.0
H = S.parse('herleville.txt'); F = S.parse('ciphertext.txt')
toks = H + [999] + F
low, high = T.inventory()
for l in open('key_partial.txt', encoding='utf-8'):
    if l.strip():
        u = T.uv(l.rstrip('
').split('	')[1])
        if u not in high: high.append(u)
        if u not in low and len(u) == 1: low.append(u)
pri = G.prior(set(low + high))
fixed = {999: S.NULL}
for l in open('key_partial.txt', encoding='utf-8'):
    if l.strip():
        g, u = l.rstrip('\n').split('\t'); fixed[int(g)] = T.uv(u)
s = S.Solver(toks, low, high, pri, fixed=fixed, cribs=[])
best = s.anneal(iters)
print('BEST', round(best, 1))
print('HERLEVILLE:', ' '.join('_' if s.map[t] == '' else s.map[t] for t in H))
print('FEUQUIERES:', ' '.join('_' if s.map[t] == '' else s.map[t] for t in F))
print('MAP', sorted((k, v) for k, v in s.map.items() if k != 999))
