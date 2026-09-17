# Annealer over the petit-chiffre key scored by (a) how much of the Herleville decode reproduces the printed
# traduction (matched 5-grams of the traduction, each counted once), (b) the French 7-gram LM on both decodes,
# (c) a unit prior.  Robust to the traduction's free wording: only exact 5-letter runs count.
# usage: python solver_trad.py [iters] [seed]
import sys, random, math, os, collections, time
import solver as S
import solver_gc as G
from gc_inventory import norm, load
sys.stdout.reconfigure(encoding='utf-8')
lm = S.lm
_T, LET, SYL, WOR, _N, _U = load()
def uv(w): return w.replace('v', 'u').replace('j', 'i')

P1 = "je mande a monsieur de catinat que le roy vous permettoit de demander la contribution au pays de mondovi et que si vous jugez quil convient au service du roy de les exempter mesme de permettre aux habitans dudit pays de raser la citadelle dudit mondovi de le faire"
P2 = "jattendray avec impatience larrivee du prochain ordinaire pour scavoir comment aura reussy vostre entreprise sur le chasteau de villefranche"
TRAD = uv((P1 + ' ' + P2).replace(' ', ''))
K = 5
TGRAMS = collections.Counter(TRAD[i:i+K] for i in range(len(TRAD) - K + 1))
EXTRA = """mondovi villefranche catinat contribution citadelle habitans exempter raser permett permettoit permettre
impatience prochain ordinaire jugez demander comment aura reussy attendray mande monsieur veillane rivole suze pignerol
turin trane javan gumiane piosasque savoye capucins faubourg chasteau estangs rendezvous cavalerie dragons infanterie
garnison troupes bataillons chevaux mulets canon pieces boulets poudre grenades mineurs outils pain avoine vivres jour
soir nuit pointe heure matin marche partir chemin ennemis ordre lettre entreprise attaque secours retirer poste
quartier detachement officiers mesures entree vingt six sept demain""".split()

def inventory():
    letters = list('abcdefghilmnopqrstuxyz')
    low = letters + [S.NULL]
    high = sorted({uv(s) for s in SYL}) + sorted({uv(w) for w in WOR}) + [uv(norm(w)) for w in EXTRA] + letters + [S.NULL]
    seen = set(); H = []
    for u in high:
        if u not in seen:
            seen.add(u); H.append(u)
    return low, H

class Trad:
    def __init__(self, H, F, low, high, pri, lam=0.7, w_trad=6.0, w_lm=1.0, w_pri=0.6, seed=1):
        self.H, self.F = H, F
        self.codes = sorted(set(H) | set(F))
        self.low, self.high = low, high
        self.wl = [pri[u] for u in low]; self.wh = [pri[u] for u in high]
        tot = sum(pri[u] for u in set(low + high))
        self.logpri = {u: math.log(pri[u] / tot) for u in set(low + high)}
        self.lam, self.w_trad, self.w_lm, self.w_pri = lam, w_trad, w_lm, w_pri
        self.rnd = random.Random(seed)
        self.map = {}
        for c in self.codes:
            pool, w = (low, self.wl) if c < 100 else (high, self.wh)
            self.map[c] = self.rnd.choices(pool, w)[0]

    def render(self, toks):
        return ''.join(self.map[t] for t in toks)

    def trad_score(self, h):
        seen = collections.Counter(h[i:i+K] for i in range(len(h) - K + 1))
        return sum(min(c, TGRAMS[g]) for g, c in seen.items() if g in TGRAMS)

    def total(self):
        h = self.render(self.H); f = self.render(self.F)
        s = self.w_trad * self.trad_score(h)
        s += self.w_lm * (lm.score(h + f) + self.lam * (len(h) + len(f)))
        s += self.w_pri * sum(self.logpri[self.map[c]] for c in self.codes)
        s -= 3.0 * sum(1 for c in self.codes if self.map[c] == S.NULL)
        return s

    def propose(self):
        r = self.rnd.random()
        c = self.rnd.choice(self.codes)
        if r < 0.85:
            pool, w = (self.low, self.wl) if c < 100 else (self.high, self.wh)
            new = self.rnd.choices(pool, w)[0]
            return {c: new} if new != self.map[c] else None
        c2 = self.rnd.choice(self.codes)
        if c2 == c or (c < 100) != (c2 < 100):
            return None
        return {c: self.map[c2], c2: self.map[c]}

    def anneal(self, iters, T0=4.0, T1=0.1, log=20000):
        cur = self.total(); best = cur; bestmap = dict(self.map); t0 = time.time()
        for it in range(iters):
            T = T0 * (T1 / T0) ** (it / iters)
            prop = self.propose()
            if not prop:
                continue
            old = {c: self.map[c] for c in prop}
            self.map.update(prop)
            new = self.total()
            d = new - cur
            if d >= 0 or self.rnd.random() < math.exp(d / T):
                cur = new
                if cur > best:
                    best, bestmap = cur, dict(self.map)
            else:
                self.map.update(old)
            if log and it % log == 0:
                print('it %d T %.2f cur %.1f best %.1f trad %d %.0fs' % (it, T, cur, best, self.trad_score(self.render(self.H)), time.time() - t0), flush=True)
        self.map = bestmap
        return best

if __name__ == '__main__':
    iters = int(sys.argv[1]) if len(sys.argv) > 1 else 300000
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    H = S.parse('herleville.txt'); F = S.parse('ciphertext.txt')
    low, high = inventory()
    pri = G.prior(set(low + high))
    for w in EXTRA:
        pri[uv(norm(w))] = max(pri.get(uv(norm(w)), 0), 300)
    t = Trad(H, F, low, high, pri, seed=seed)
    best = t.anneal(iters)
    print('BEST', round(best, 1), 'trad 5-grams matched', t.trad_score(t.render(H)), 'of', sum(TGRAMS.values()))
    print('HERLEVILLE:', ' '.join('_' if t.map[g] == '' else t.map[g] for g in H))
    print('FEUQUIERES:', ' '.join('_' if t.map[g] == '' else t.map[g] for g in F))
    print('MAP', sorted(t.map.items()))
