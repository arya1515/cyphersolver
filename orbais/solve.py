"""Anneal glyph->letter map for the cipher groups of BnF fr. 3413 no. 62, scored with the
space-free French 6-gram LM (raince/frns6.pkl) over the groups *in their clear-text context*.
Glyph ids are my transcription labels (see NOTES.md). FIX = readings confirmed by cribs."""
import pickle, random, math, sys
D = pickle.load(open('../raince/frns6.pkl', 'rb')); N = D['n']; P = D['p']; BACK = D['back']
def score(s):
    t = 0.0
    for i in range(len(s)-N+1):
        d = P.get(s[i:i+N-1]); t += (d.get(s[i+N-1], BACK) if d else BACK)
    return t
def norm(s): return ''.join(c for c in s.lower().replace('j','i').replace('v','u') if c.isalpha())

# (left context, glyph list, right context)
G = [
 ("sontfortprofonsetinscrutables", "B1 I B1 E S1 W H4 X R DASH T", "declaredeuxiours"),
 ("declaredeuxiours", "F3 D3 O H E N", "deuantcettenouuellelon"),
 ("ilneuousfaultriendirepourcequitouche", "PHI O P V X T S1", "ilnefaultoublier"),
 ("ilnefaultoublier", "E2 V B R M OOO E W C8 PHI2 O N", "quevoussauezpourbeaucoupderaisons"),
 ("deuoiravousescrireestantsiaccabledaffairespourestresonaisnedemeschargemons", "W V S1 I9 N", "detenuduneffiebure"),
 ("maintenantquevousseresa", "U O S1 OOO R E NN A X ETA N E", "silhistoireesturaye"),
 ("etneloublieraux occasionsdepuisque".replace(' ',''), "MR F3 TAU X L N NABLA V I9 OOO N E", "aesteretire"),
 ("aesteretire", "T U E PHI U N ETA DASH SEVEN B PHI Z2", "qui"),
 ("qui", "W L N E I9 R X X", "pluspaticulierementquenulautre"),
 ("uostretreshumbleseruiteur", "Z2 V R M HH", "presentesestreshumblesrecommandations"),
]
FIX = dict(W='c', V='a', S1='s', I9='i', N='n', R='r', O='o', OOO='t', E='e', M='o', B='p', C8='t', PHI2='i', U='u')
PRIOR = dict(X='e', DASH='a', T='t', PHI='u', ETA='g', H4='h', L='l', NABLA='m', Z2='b', D3='d', P='p', E2='l', B1='u')
glyphs = sorted({g for _, gs, _ in G for g in gs.split()})
free = [g for g in glyphs if g not in FIX]
ALPH = 'abcdefghilmnopqrstuxyz'
CH = list(ALPH) + ['']
def total(m):
    t = 0.0
    for l, gs, r in G:
        s = norm(l)[-12:] + ''.join(m[g] for g in gs.split()) + norm(r)[:12]
        t += score(s)
    t -= 3.0 * sum(1 for g in free if m[g] == '')          # nulls cost
    t += 1.5 * sum(1 for g in free if PRIOR.get(g) == m[g])  # soft prior from Tomokiyo's table
    return t
def run(seed):
    random.seed(seed); m = dict(FIX); m.update({g: PRIOR.get(g, random.choice(ALPH)) for g in free})
    cur = total(m); best = (cur, dict(m)); T = 3.0
    for it in range(40000):
        g = random.choice(free); old = m[g]; m[g] = random.choice(CH)
        new = total(m)
        if new >= cur or random.random() < math.exp((new-cur)/T): cur = new
        else: m[g] = old
        if cur > best[0]: best = (cur, dict(m))
        T = max(0.05, T*0.9998)
    return best
if __name__ == '__main__':
    for seed in range(int(sys.argv[1]) if len(sys.argv) > 1 else 6):
        sc, m = run(seed)
        print(round(sc, 1), ' | '.join(''.join(m[g] for g in gs.split()) for _, gs, _ in G))
        print('   ', {g: m[g] for g in free})
