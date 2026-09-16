# Nomenclator solver v2: simulated annealing over code->unit mapping, scored by a spaceless char 7-gram LM
# with the surrounding cleartext as context. Structural priors from the Croissy-era code sheets:
#  - codes below LOWMAX are single letters / a few bigrams / nulls;
#  - codes at step 10 (same ones digit) tend to be one consonant's syllables in the order a e i o u;
#  - run moves assign a whole step-10 chain to one consonant at once.
import re, random, math, sys, collections, unicodedata, time
from lm import LM
lm = LM()
LOWMAX = 80
import os
LAMBDA = float(os.environ.get('LAMBDA', '0.7'))   # bonus per emitted letter
NULLPEN = float(os.environ.get('NULLPEN', '3.0'))  # penalty per code mapped to null
PRIORW = float(os.environ.get('PRIORW', '1.0'))    # weight of the unit-prior term (-log p(unit) per code)

def norm(t):
    t = unicodedata.normalize('NFD', t)
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn').lower()
    t = re.sub(r"[^a-z' ]+", ' ', t)
    t = re.sub(r"'", ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

def parse(path):
    segs = []
    for line in open(path, encoding='utf-8'):
        if not line.startswith('['):
            continue
        line = line.split(']', 1)[1]
        items = []
        for p in line.split('|'):
            toks = p.split()
            if toks and all(re.fullmatch(r'\d+[_^]?', t) for t in toks):
                for t in toks:
                    items.append(('k', int(re.sub(r'[_^]', '', t))))
            else:
                items.append(('c', norm(p)))
        segs.append(items)
    return segs

CONS = 'bcdfghjlmnpqrstvxz'
VOW = 'aeiou'
NULL = ''
DOMAIN = """pape saintete sa bulles bulle evesques evesque eveschez evesche archevesques cardinal cardinaux assemblee
declaration declarer projet articles quatre regale clerge nommez nommes expedition expedier expedie obtenir accorder
accorde refuser refus difficulte difficultez satisfaction protestation prelats prelat eglise france rome cour roy
majeste vostre mesme aussy point rien ne ni ny pas jamais tousjours avant apres lettre lettres escrit escrire mander
mandez propos proposer propose proposition offrir offre demande demander demandez consentir consentement conditions
terminer finir affaire affaires negociation traitte traiter parole promesse promettre bref brefs constitution doctrine
foy sentimens sentiment souffrir souffre agreer agree approuver approuve recevoir receu signer signe signee sousmettre
soumission retracter retractation forme termes maniere mots parolles chose choses temps tems presse presser
empressement lenteur delay courrier ordinaire audience ottoboni cibo estrees forbin janson polignac spada altieri
panciatici casanate rubini secretaire estat dataire vacans vacants vaquans vacance pourvoir pourveu provisions
institution canonique juridiction siege saint apostolique vicaires empereur espagne venise""".split()

def inventory(extra_words=None):
    low = list('abcdefghijklmnopqrstuvxyz') + ['et', 'st', 'on', 'en', 'nt', 'ns', 'es', NULL]
    high = [c + v for c in CONS for v in VOW]
    high += ['en', 'on', 'an', 'in', 'un', 'es', 'er', 'ez', 'ou', 'oi', 'ai', 'au', 'eu', 'nt', 'st', 'ue', 'ie',
             'ent', 'ment', 'tion', 'qu', 'ch', 'ph', 'gn', NULL]
    words = collections.Counter(open('corpus_fr.txt', encoding='utf-8').read().split())
    top = [w for w, _ in words.most_common(500) if len(w) > 1]
    high += top + DOMAIN + (extra_words or [])
    def dedup(xs):
        seen = set(); out = []
        for u in xs:
            if u not in seen:
                seen.add(u); out.append(u)
        return out
    return dedup(low), dedup(high)

def unit_prior(units):
    txt = open('corpus_fr.txt', encoding='utf-8').read()
    words = collections.Counter(txt.split())
    pri = {}
    for u in units:
        if u == NULL:
            pri[u] = 3000
        elif len(u) <= 2 or u in ('ent', 'ment', 'tion'):
            pri[u] = txt.count(u) + 50
        else:
            pri[u] = words.get(u, 0) * 5 + 20
    return pri

class Solver:
    def __init__(self, segs, low, high, pri, fixed=None, runbonus=2.0, lowmax=LOWMAX):
        self.segs = segs
        self.codes = sorted({it[1] for s in segs for it in s if it[0] == 'k'})
        self.code_segs = collections.defaultdict(set)
        for i, s in enumerate(segs):
            for it in s:
                if it[0] == 'k':
                    self.code_segs[it[1]].add(i)
        self.fixed = fixed or {}
        self.runbonus = runbonus
        self.lowmax = lowmax
        self.low = low; self.high = high
        self.wlow = [pri[u] for u in low]; self.whigh = [pri[u] for u in high]
        tot = sum(pri[u] for u in set(low + high))
        self.logpri = {u: math.log(pri[u] / tot) for u in set(low + high)}
        self.map = {}
        for c in self.codes:
            pool, w = (low, self.wlow) if c < lowmax else (high, self.whigh)
            self.map[c] = random.choices(pool, w)[0]
        self.map.update(self.fixed)
        # step-10 runs among high codes
        cs = set(c for c in self.codes if c >= lowmax)
        self.runs = []
        for c in sorted(cs):
            if c - 10 in cs:
                continue
            run = [c]
            while run[-1] + 10 in cs:
                run.append(run[-1] + 10)
            if len(run) >= 2:
                self.runs.append(run)
        self.segscore = [self.score_seg(i) for i in range(len(segs))]
        self._struct = self.structural()

    def render_seg(self, i, m=None):
        m = m or self.map
        return ''.join(v if k == 'c' else m[v] for k, v in self.segs[i])

    def render_pretty(self, i):
        out = []
        for k, v in self.segs[i]:
            if k == 'c':
                out.append(' [' + v + '] ')
            else:
                u = self.map[v]
                out.append(('_' if u == NULL else u) + ('.' if len(u) > 2 else ''))
        return ''.join(out)

    def score_seg(self, i, m=None):
        t = self.render_seg(i, m)
        return lm.score(t) + LAMBDA * len(re.sub('[^a-z]', '', t))

    def structural(self):
        m = self.map; b = -NULLPEN * sum(1 for c in self.codes if m[c] == NULL)
        b += PRIORW * sum(self.logpri[m[c]] for c in self.codes)
        for c in self.codes:
            if c >= self.lowmax and c + 10 in m:
                u1, u2 = m[c], m[c + 10]
                if (len(u1) == 2 and len(u2) == 2 and u1[0] in CONS and u1[0] == u2[0] and u1[1] in VOW
                        and u2[1] in VOW and VOW.index(u1[1]) < VOW.index(u2[1])):
                    b += self.runbonus
        return b

    def total(self):
        return sum(self.segscore) + self._struct

    def propose(self):
        """returns dict code->new unit"""
        r = random.random()
        if r < 0.15 and self.runs:
            run = random.choice(self.runs)
            if any(c in self.fixed for c in run):
                return None
            C = random.choice(CONS)
            v0 = random.randint(0, max(0, 5 - len(run)))
            return {c: C + VOW[min(v0 + k, 4)] for k, c in enumerate(run)}
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
        cur = self.total(); best = cur; bestmap = dict(self.map)
        t0 = time.time()
        for it in range(iters):
            T = T0 * (T1 / T0) ** (it / iters)
            prop = self.propose()
            if not prop:
                continue
            old = {c: self.map[c] for c in prop}
            self.map.update(prop)
            segs = set().union(*(self.code_segs[x] for x in prop))
            newscores = {i: self.score_seg(i) for i in segs}
            newstruct = self.structural()
            delta = sum(newscores[i] - self.segscore[i] for i in segs) + newstruct - self._struct
            if delta >= 0 or random.random() < math.exp(delta / T):
                for i in segs:
                    self.segscore[i] = newscores[i]
                self._struct = newstruct
                cur += delta
                if cur > best:
                    best = cur; bestmap = dict(self.map)
            else:
                self.map.update(old)
            if log and it % log == 0:
                print(f'it {it} T {T:.2f} cur {cur:.1f} best {best:.1f} {time.time()-t0:.0f}s', flush=True)
        self.map = bestmap
        self.segscore = [self.score_seg(i) for i in range(len(self.segs))]
        self._struct = self.structural()
        return best

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'ciphertext.txt'
    iters = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    random.seed(seed)
    segs = parse(path)
    low, high = inventory()
    pri = unit_prior(low + high)
    S = Solver(segs, low, high, pri)
    print('codes', len(S.codes), 'runs', len(S.runs), 'units', len(low), len(high))
    best = S.anneal(iters)
    print('BEST', best)
    for i in range(len(segs)):
        print(S.render_pretty(i))
    print('MAP', sorted(S.map.items()))
