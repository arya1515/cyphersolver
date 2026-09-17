# Closed-inventory solver: same annealer as solver.py, but the unit inventory is Bazeries' Grand Chiffre de 1691
# (letters + nulls below 100; the 78 syllables, 255 words/stems and nulls above), plus the Veillane vocabulary.
# usage: python solver_gc.py ciphertext.txt [iters] [seed] [--key control_gc_key.txt]
import sys, random, os, collections, math
import solver as S
from gc_inventory import load, norm
table, LET, SYL, WOR, NUL, UNK = load()

EXTRA = """veillane rivole suze pignerol turin trane javan gumiane piosasque savoye capucins faubourg chasteau
estangs rendezvous cavalerie dragons infanterie hommes garnison troupes bataillons compagnies escadrons chevaux
mulets canon pieces boulets poudre grenades mineurs outils haches pain avoine vivres jours jour soir nuit pointe
heures heure matin marche partir chemin montagne ennemis monsieur ordre memoire lettre entreprise attaque
attaquer emporter enlever surprendre secours retirer postes poste quartier detachement sergens soldats officiers
mesures disposition entree vingt six sept demain""".split()

def inventory():
    low = list('abcdefghijlmnopqrstuvxyz') + [S.NULL]
    high = sorted(SYL) + sorted(WOR) + [norm(w) for w in EXTRA] + [S.NULL]
    seen = set(); H = []
    for u in high:
        if u not in seen:
            seen.add(u); H.append(u)
    return low, H

def prior(units):
    txt = open(os.path.join(S.CH, 'corpus_fr.txt'), encoding='utf-8').read()
    words = collections.Counter(txt.split())
    pri = {}
    for u in units:
        if u == S.NULL:
            pri[u] = 3000
        elif len(u) <= 2:
            pri[u] = txt.count(u) + 50
        else:
            # stems: count words starting with the stem
            pri[u] = sum(c for w, c in words.items() if w.startswith(u)) * 3 + 100
    return pri

if __name__ == '__main__':
    path = sys.argv[1]
    iters = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    random.seed(seed)
    toks = S.parse(path)
    low, high = inventory()
    pri = prior(set(low + high))
    cribs = [w for w in S.CRIBS if w in set(high) or len(w) >= 5]
    s = S.Solver(toks, low, high, pri, cribs=cribs)
    best = s.anneal(iters)
    print('BEST', round(best, 1))
    print(s.render_pretty())
    print(s.render())
    if '--key' in sys.argv:
        key = {}
        for l in open(sys.argv[sys.argv.index('--key') + 1], encoding='utf-8'):
            n, u = l.rstrip('\n').split('\t'); key[int(n)] = u
        ok = sum(1 for t in toks if s.map[t] == key.get(t))
        truth = dict(s.map); truth.update({t: key[t] for t in toks})
        print('TOKENS RECOVERED %d/%d = %.0f%%' % (ok, len(toks), 100 * ok / len(toks)))
        print('TRUE KEY SCORE', round(S.score_map(toks, truth, low, high, pri), 1))
        print('TRUTH', ''.join(key[t] for t in toks))
