# Crib-dragging over the spelled stretches of the Feuquieres letter.
# Model: groups < LOWMAX are letters (2-3 homophones each) or nulls; groups >= LOWMAX are syllables / words.
# A crib word placed on a run of low groups must satisfy: same group -> same letter (within the window and
# globally).  Different groups may carry the same letter (homophones), but a letter may not have more than
# KMAX homophones.  Beam search over compatible placements; score = letters covered + frequency plausibility.
import re, sys, math, collections, itertools, unicodedata
LOWMAX = 100
KMAX = 3

def norm(t):
    t = unicodedata.normalize('NFD', t)
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn').lower()
    return re.sub(r"[^a-z]", '', t)

toks = [int(x) for l in open('ciphertext.txt', encoding='utf-8') if not l.startswith('#') for x in l.split()]
cnt = collections.Counter(toks)
low = [t for t in toks if t < LOWMAX]
lowcnt = collections.Counter(low)
N_low = len(low)

# runs of consecutive low groups
runs = []
i = 0
while i < len(toks):
    if toks[i] < LOWMAX:
        j = i
        while j < len(toks) and toks[j] < LOWMAX:
            j += 1
        runs.append((i, toks[i:j]))
        i = j
    else:
        i += 1

# French letter frequencies (approx., 17th-c. prose)
FREQ = dict(e=.172, a=.082, s=.081, i=.074, n=.071, t=.070, r=.066, u=.063, l=.055, o=.054, d=.037, c=.032,
            m=.030, p=.029, v=.017, q=.014, f=.011, b=.009, g=.009, h=.008, j=.005, x=.004, y=.004, z=.002, k=.0001, w=.0001)

def plaus(g, x, k=2.5):
    """log-plausibility of group g (count lowcnt[g]) being one of ~k homophones of letter x."""
    lam = max(N_low * FREQ.get(x, .001) / k, 0.3)
    n = lowcnt[g]
    return n * math.log(lam) - lam - math.lgamma(n + 1)

CRIBS = """veillane rivole rivoli suze pignerol turin trane javan gumiane piosasque piossasque cumiane savoye
capucins fauxbourg faubourg chasteau estangs estang rendezvous cavalerie dragons infanterie hommes pied garnison
troupes bataillons bataillon regiment compagnies escadrons chevaux mulets canon pieces boulets poudre grenades
mineurs mines outils haches pain avoine vivres jours jour soir nuit pointe heures heure matin marche marcher partir
partiray chemin chemins montagne plaine ennemis ennemy monseigneur monsieur ordre ordres memoire lettre advis
nouvelles prisonniers deserteur courrier gardes allemands lorraine fusiliers gendarmes carmagnole saluces carignan
pragelas chaumont briancon fenestrelle entreprise expedition attaquer attaque emporter enlever surprendre secourir
secours retirer retraite postes poste quartiers quartier convoy detachement detachemens detaches sergens soldats
officiers capitaine lieutenant colonel major brigadier guide espion paysan advertir avertir mander mandez escrire
mesures disposition diligence justesse execution reussir precaution quantite nombre partie moitie livres
entree pointe vingt sixieme septieme demain lundy mardy mercredy jeudy vendredy samedy dimanche janvier
honneur serviteur obeissant humble tousjours jusques aussy ainsy aujourdhuy escrit mande faict peult vostre nostre
lorsque quand comme point moins bien fort toute toutes rien chose choses temps tems
seroit seront pourront pourray pourrez faudra faudroit falloit arriver arriveray partiront trouver trouveray
joindre joindray rendre rendray rendez rendront sortir sortiray marcheray attaqueray envoyer envoyeray
porter porteront prendre prendray mener meneray conduire passer passeray""".split()
CRIBS = sorted({norm(w) for w in CRIBS if len(norm(w)) >= 5}, key=len, reverse=True)

def placements():
    out = []
    for ri, (pos, run) in enumerate(runs):
        for w in CRIBS:
            L = len(w)
            if L > len(run):
                continue
            for off in range(len(run) - L + 1):
                win = run[off:off+L]
                m = {}
                ok = True
                inv = collections.defaultdict(set)
                for g, x in zip(win, w):
                    if m.get(g, x) != x:
                        ok = False; break
                    m[g] = x
                    inv[x].add(g)
                if not ok or any(len(s) > KMAX for s in inv.values()):
                    continue
                sc = sum(plaus(g, x) for g, x in m.items())
                out.append((ri, off, w, m, sc))
    return out

def compatible(m1, m2, inv1):
    inv = collections.defaultdict(set)
    for x, s in inv1.items():
        inv[x] |= s
    for g, x in m2.items():
        if m1.get(g, x) != x:
            return None
        inv[x].add(g)
        if len(inv[x]) > KMAX:
            return None
    return inv

def render(m):
    out = []
    for t in toks:
        if t < LOWMAX:
            out.append(m.get(t, '.'))
        else:
            out.append('[%d]' % t)
    return ''.join(out)

if __name__ == '__main__':
    print('low tokens', N_low, 'runs', len(runs), 'runs>=4', sum(1 for _, r in runs if len(r) >= 4))
    P = placements()
    print('placements', len(P))
    # per run, best placements
    byrun = collections.defaultdict(list)
    for p in P:
        byrun[p[0]].append(p)
    for ri, (pos, run) in enumerate(runs):
        if len(run) >= 5:
            cands = sorted(byrun[ri], key=lambda p: -(len(p[2]) * 0.6 + p[4] / 4))[:8]
            print('run', ri, 'pos', pos, run, '->', [(w, off, round(sc, 1)) for _, off, w, m, sc in cands])
    # beam search over long-word placements
    longP = [p for p in P if len(p[2]) >= 6]
    longP.sort(key=lambda p: -(len(p[2]) + p[4] / 3))
    beam = [({}, collections.defaultdict(set), 0.0, [])]
    for step in range(8):
        new = []
        for m, inv, sc, hist in beam:
            used = {h[0] for h in hist}
            for ri, off, w, pm, psc in longP[:400]:
                if ri in used:
                    continue
                inv2 = compatible(m, pm, inv)
                if inv2 is None:
                    continue
                m2 = dict(m); m2.update(pm)
                new.append((m2, inv2, sc + len(w) + psc / 3, hist + [(ri, off, w)]))
        if not new:
            break
        new.sort(key=lambda b: -b[2])
        # dedupe by mapping
        seen = set(); beam = []
        for b in new:
            key = tuple(sorted(b[0].items()))
            if key in seen: continue
            seen.add(key); beam.append(b)
            if len(beam) >= 60: break
    for m, inv, sc, hist in beam[:5]:
        print('\nSCORE', round(sc, 1), hist)
        print('key', sorted(m.items()))
        print(render(m))
