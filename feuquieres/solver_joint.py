# Joint annealer over the two letters in the petit chiffre (Herleville 6 Sept 1690 + Feuquieres 25 Jan 1691),
# closed Grand-Chiffre inventory plus the vocabulary of the printed traduction and of the Veillane memoir as crib.
# usage: python solver_joint.py [iters] [seed]
import sys, random, os, collections, math
import solver as S
import solver_gc as G
from gc_inventory import norm

TRAD = """mande monsieur catinat roy permettoit permet demander contribution pays mondovi jugez convient service
exempter mesme permettre habitans dudit raser citadelle faire attendray impatience arrivee prochain ordinaire
scavoir comment aura reussy vostre entreprise chasteau villefranche pignerol""".split()

def inventory():
    low, high = G.inventory()
    extra = [norm(w) for w in TRAD]
    seen = set(high); H = list(high)
    for u in extra:
        if u not in seen:
            seen.add(u); H.append(u)
    return low, H

if __name__ == '__main__':
    iters = int(sys.argv[1]) if len(sys.argv) > 1 else 300000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    random.seed(seed)
    H = S.parse('herleville.txt'); F = S.parse('ciphertext.txt')
    toks = H + [999] + F
    low, high = inventory()
    pri = G.prior(set(low + high))
    for w in TRAD:
        pri[norm(w)] = max(pri.get(norm(w), 0), 400)
    cribs = sorted({norm(w) for w in TRAD if len(w) >= 4} | {w for w in S.CRIBS if len(w) >= 5})
    s = S.Solver(toks, low, high, pri, fixed={999: S.NULL}, cribs=cribs)
    best = s.anneal(iters)
    print('BEST', round(best, 1))
    mH = s.map
    print('HERLEVILLE:', ' '.join('_' if mH[t] == '' else mH[t] for t in H))
    print('FEUQUIERES:', ' '.join('_' if mH[t] == '' else mH[t] for t in F))
    print('MAP', sorted((k, v) for k, v in s.map.items() if k != 999))
