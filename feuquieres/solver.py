# Solver for the Feuquieres -> Catinat letter (Pignerol, 25 Jan 1691): simulated annealing over a
# code-group -> unit mapping, scored by the spaceless French 7-gram LM built for the Chaulnes attempt,
# a unit prior, a per-letter bonus, a null penalty and a crib bonus.  Design prior (from the frequency skew
# of the letter and the sister 1702 Catinat code): groups below LOWMAX are single letters (with homophones)
# or nulls; groups from LOWMAX up are CV syllables, common letter groups or words.  No positional order is
# assumed inside either block (two-part "petit chiffre").
#
# usage: python solver.py ciphertext.txt [iters] [seed] [--fixed k=unit,...]
import re, random, math, sys, os, collections, unicodedata, time
HERE = os.path.dirname(os.path.abspath(__file__))
CH = os.path.join(HERE, '..', 'chaulnes')
sys.path.insert(0, CH)
from lm import LM
lm = LM(os.path.join(CH, 'lm7.pkl'))

LOWMAX = int(os.environ.get('LOWMAX', '100'))
LAMBDA = float(os.environ.get('LAMBDA', '0.7'))
NULLPEN = float(os.environ.get('NULLPEN', '3.0'))
PRIORW = float(os.environ.get('PRIORW', '1.0'))
CRIBW = float(os.environ.get('CRIBW', '4.0'))
CONS = 'bcdfghjlmnpqrstvxz'
VOW = 'aeiou'
NULL = ''

def norm(t):
    t = unicodedata.normalize('NFD', t)
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn').lower()
    t = re.sub(r"[^a-z' ]+", ' ', t)
    t = re.sub(r"'", ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

def parse(path):
    toks = []
    for line in open(path, encoding='utf-8'):
        if line.startswith('#'):
            continue
        toks += [int(x) for x in line.split()]
    return toks

# vocabulary of the Veillane enterprise (Catinat to Feuquieres, 12 and 19 Jan 1691; Feuquieres' Memoires)
DOMAIN = """veillane rivole rivoli suze pignerol turin trane javan gumiane piosasque cumiane savoye savoie
capucins faubourg fauxbourg chasteau estangs estang rendezvous cavalerie dragons infanterie hommes pied garnison
troupes bataillons bataillon regiment regimens compagnies escadrons chevaux mulets canon pieces boulets poudre
grenades mineurs mines outils haches pain avoine vivres jours jour soir nuit pointe heures heure matin marche
marcher partir partiray partiront chemin chemins montagne plaine defiles ennemis ennemy roy majeste monseigneur
monsieur ordre ordres memoire lettre advis nouvelles prisonniers deserteur courrier gardes allemands lorraine
macel fusiliers gendarmes quiers pianesse moncaglier carmagnole saluces carignan casal po pragelas chaumont
briancon cezanne oulx fenestrelle uxeau balboutet meane exilles grancey artois bourbon perigord robec cambresis
sarre vexin clerambault bretagne ferrand cray entreprise expedition attaquer attaque emporter enlever surprendre
secourir secours retirer retraite postes poste quartiers quartier convoy detachement detachemens detaches
sergens soldats officiers capitaine lieutenant colonel major brigadier guide espion paysan advertir avertir
mander mandez escrire escrit response responds recevoir receu joindre jonction mesures disposition
diligence justesse execution reussir reussite succes precaution quantite nombre partie moitie livres""".split()

PERIOD = """estre este estoit estoient ay avons avez ont sçay scay sçavoir scavoir mesme mesmes tousjours jusques
aussy ainsy cecy celuy luy icy ny aujourdhuy escrit escrire escris mandé mande mander mandez faict fait faire
peult peut tres humble obeissant serviteur honneur vostre nostre vos nos leurs qu il elle ils elles nous vous
je me te se le la les de des du au aux un une et ou mais si que qui quoy dont pour par sur sous dans en y a
avec sans contre entre depuis apres avant devant derriere selon suivant lorsque quand comme point pas plus
moins bien fort tout tous toute toutes rien chose choses temps tems heure heures matin soir nuit jour jours""".split()

DOMAIN_N = {norm(w) for w in DOMAIN}

CRIBS = ['veillane', 'rivole', 'suze', 'pignerol', 'turin', 'trane', 'javan', 'gumiane', 'piosasque', 'savoye',
         'capucins', 'faubourg', 'chasteau', 'estangs', 'cavalerie', 'dragons', 'infanterie', 'garnison', 'canon',
         'mulets', 'chevaux', 'boulets', 'poudre', 'grenades', 'mineurs', 'outils', 'pain', 'avoine', 'ennemis',
         'troupes', 'bataillons', 'rendezvous', 'pointe', 'monsieur', 'majeste', 'entreprise']

def inventory(extra_words=None):
    low = list('abcdefghijklmnopqrstuvxyz') + ['et', 'st', 'on', 'en', 'nt', 'ns', 'es', NULL]
    high = [c + v for c in CONS for v in VOW]
    high += ['en', 'on', 'an', 'in', 'un', 'es', 'er', 'ez', 'ou', 'oi', 'ai', 'au', 'eu', 'nt', 'st', 'ue', 'ie',
             'ent', 'ment', 'tion', 'qu', 'ch', 'ph', 'gn', 'que', 'qui', 'qua', 'quo', NULL]
    words = collections.Counter(open(os.path.join(CH, 'corpus_fr.txt'), encoding='utf-8').read().split())
    top = [w for w, _ in words.most_common(500) if len(w) > 1]
    high += top + [norm(w) for w in DOMAIN + PERIOD] + (extra_words or [])
    seen = set(); L = []; H = []
    for u in low:
        if u not in seen: seen.add(u); L.append(u)
    seen = set()
    for u in high:
        if u not in seen: seen.add(u); H.append(u)
    return L, H

def unit_prior(units):
    txt = open(os.path.join(CH, 'corpus_fr.txt'), encoding='utf-8').read()
    words = collections.Counter(txt.split())
    pri = {}
    for u in units:
        if u == NULL:
            pri[u] = 3000
        elif len(u) <= 2 or u in ('ent', 'ment', 'tion', 'que', 'qui', 'qua', 'quo'):
            pri[u] = txt.count(u) + 50
        else:
            pri[u] = words.get(u, 0) * 5 + (200 if u in DOMAIN_N else 20)
    return pri

def split_word(word, classes):
    """Split word into units matching a class pattern ('L' letter, 'H' high). Returns list of units or None."""
    res = []
    def rec(i, k):
        if i == len(word):
            return k == len(classes)
        if k >= len(classes):
            return False
        cls = classes[k]
        if cls == 'L':
            res.append(word[i]);
            if rec(i + 1, k + 1): return True
            res.pop()
            return False
        # high: try longest word remainder, syllables (CV), bigrams
        for L in (len(word) - i, 4, 3, 2):
            if L < 2 or i + L > len(word):
                continue
            u = word[i:i+L]
            ok = (L == len(word) - i and L >= 3) or (L == 2 and u[0] in CONS and u[1] in VOW) or u in ('en', 'on', 'an', 'in', 'ou', 'oi', 'ai', 'au', 'eu', 'ent', 'ment', 'tion', 'que', 'qui')
            if ok:
                res.append(u)
                if rec(i + L, k + 1): return True
                res.pop()
        return False
    return res if rec(0, 0) else None

class Solver:
    def __init__(self, toks, low, high, pri, fixed=None, lowmax=LOWMAX, cribs=None):
        self.toks = toks
        self.codes = sorted(set(toks))
        self.fixed = fixed or {}
        self.lowmax = lowmax
        self.low = low; self.high = high
        self.wlow = [pri[u] for u in low]; self.whigh = [pri[u] for u in high]
        tot = sum(pri[u] for u in set(low + high))
        self.logpri = {u: math.log(pri[u] / tot) for u in set(low + high)}
        self.cribs = cribs if cribs is not None else CRIBS
        self.map = {}
        for c in self.codes:
            pool, w = (low, self.wlow) if c < lowmax else (high, self.whigh)
            self.map[c] = random.choices(pool, w)[0]
        self.map.update(self.fixed)
        self.cur = self.total()

    def render(self, m=None):
        m = m or self.map
        return ''.join(m[t] for t in self.toks)

    def render_pretty(self, m=None):
        m = m or self.map
        out = []
        for t in self.toks:
            u = m[t]
            out.append('_' if u == NULL else (u if len(u) <= 2 else u + '.'))
        return ' '.join(out)

    def total(self, m=None):
        m = m or self.map
        t = self.render(m)
        s = lm.score(t) + LAMBDA * len(t)
        s -= NULLPEN * sum(1 for c in self.codes if m[c] == NULL)
        s += PRIORW * sum(self.logpri[m[c]] for c in self.codes)
        if CRIBW:
            # each crib word rewarded at most twice, so the search cannot farm the bonus
            s += CRIBW * sum(len(w) * min(t.count(w), 2) for w in self.cribs)
        return s

    def propose(self):
        r = random.random()
        if r < 0.10 and self.cribs:
            # crib placement: choose a word and a position; split according to classes
            w = random.choice(self.cribs)
            n = random.randint(1, min(len(w), 6))
            i = random.randint(0, len(self.toks) - n)
            codes = self.toks[i:i+n]
            if any(c in self.fixed for c in codes):
                return None
            classes = ''.join('L' if c < self.lowmax else 'H' for c in codes)
            units = split_word(w, classes)
            if not units:
                return None
            prop = {}
            for c, u in zip(codes, units):
                if c in prop and prop[c] != u:
                    return None
                if u not in self.logpri:
                    return None
                prop[c] = u
            return prop
        c = random.choice(self.codes)
        if c in self.fixed:
            return None
        if r < 0.9:
            pool, w = (self.low, self.wlow) if c < self.lowmax else (self.high, self.whigh)
            new = random.choices(pool, w)[0]
            if new == self.map[c]:
                return None
            return {c: new}
        c2 = random.choice(self.codes)
        if c2 == c or c2 in self.fixed or (c < self.lowmax) != (c2 < self.lowmax):
            return None
        return {c: self.map[c2], c2: self.map[c]}

    def anneal(self, iters=200000, T0=3.0, T1=0.15, log=20000):
        cur = self.cur; best = cur; bestmap = dict(self.map)
        t0 = time.time()
        for it in range(iters):
            T = T0 * (T1 / T0) ** (it / iters)
            prop = self.propose()
            if not prop:
                continue
            old = {c: self.map[c] for c in prop}
            self.map.update(prop)
            new = self.total()
            delta = new - cur
            if delta >= 0 or random.random() < math.exp(delta / T):
                cur = new
                if cur > best:
                    best = cur; bestmap = dict(self.map)
            else:
                self.map.update(old)
            if log and it % log == 0:
                print(f'it {it} T {T:.2f} cur {cur:.1f} best {best:.1f} {time.time()-t0:.0f}s', flush=True)
        self.map = bestmap
        self.cur = best
        return best

def score_map(toks, m, low, high, pri):
    s = Solver(toks, low, high, pri, fixed=m)
    s.map = dict(m)
    return s.total()

if __name__ == '__main__':
    path = sys.argv[1]
    iters = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    random.seed(seed)
    toks = parse(path)
    low, high = inventory()
    pri = unit_prior(set(low + high))
    fixed = {}
    if '--fixed' in sys.argv:
        for kv in sys.argv[sys.argv.index('--fixed') + 1].split(','):
            k, v = kv.split('=')
            fixed[int(k)] = v if v != '_' else NULL
    s = Solver(toks, low, high, pri, fixed=fixed)
    best = s.anneal(iters)
    print('BEST', round(best, 1))
    print(s.render_pretty())
    print(s.render())
    print('MAP', sorted(s.map.items()))
