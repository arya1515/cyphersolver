# Solver for the 1653 Bordeaux cipher (BL Add MS 4200 f.88) and matched controls.
# Design prior (Brienne's office, 1651-54: Brienne's Cipher 2 of 1651, Mazarin-Bordeaux key of 1654 by Lasry):
#   - letters = graphic signs + low plain numbers, homophonic, no order assumed;
#   - syllables = consecutive numbers running through the CV syllabary in alphabetical order, continuing from one
#     diacritic series into the next (with a few function words embedded alphabetically), gaps allowed;
#   - overbar numbers (and 3-digit groups) = nomenclature words: treated as unknown, they cut the text into segments.
# Score: spaceless char 6-gram LM (lm.py) on each segment + LAMBDA per emitted letter - NULLPEN per null letter.
import re, random, math, sys, os, collections, time, argparse
from lm import LM

CONS = 'bcdfghjlmnpqrstvxz'
VOW = 'aeiou'
WORDS = ['des', 'est', 'estre', 'et', 'faire', 'fait', 'il', 'on', 'ou', 'pour', 'que', 'qui', 'nos', 'tant', 'vous',
         'nous', 'par', 'les', 'le', 'la', 'de', 'ne', 'pas', 'plus', 'mais', 'avec', 'luy', 'son', 'sa', 'se', 'si',
         'en', 'un', 'une', 'y', 'ce', 'ils', 'elle', 'sur', 'dont', 'point']
LETFREQ = {'e': 17.0, 'a': 8.2, 's': 8.1, 'i': 7.5, 'n': 7.1, 't': 7.0, 'r': 6.6, 'u': 6.3, 'l': 5.5, 'o': 5.4,
           'd': 3.7, 'c': 3.3, 'p': 3.0, 'm': 3.0, 'v': 1.6, 'q': 1.4, 'f': 1.1, 'g': 1.0, 'b': 0.9, 'h': 0.7,
           'j': 0.6, 'x': 0.4, 'y': 0.3, 'z': 0.1}
OVERBAR = '‾'
UMLAUT = '¨'


def units(words=True):
    U = [c + v for c in CONS if c != 'q' for v in VOW] + ['qua', 'que', 'qui', 'quo']
    if words:
        U += [w for w in WORDS if w not in U]
    return sorted(set(U))


def load_tokens(path):
    toks = []
    for line in open(path, encoding='utf-8'):
        if line.startswith('#'):
            continue
        toks += line.split()
    return toks


def series_of(tok):
    m = re.fullmatch(r"(\d+)(['" + UMLAUT + OVERBAR + r"=-]?)", tok)
    if not m:
        return 'g', None
    return m.group(2) or '0', int(m.group(1))


class Problem:
    def __init__(self, toks, order="0'" + UMLAUT, letmax=45, primeletters=False):
        self.toks = toks
        self.primeletters = primeletters
        self.order = order
        self.cls = {}
        syl_slots = []
        self.free = []
        for t in set(toks):
            s, n = series_of(t)
            if s == OVERBAR or (s == '0' and n is not None and n >= 100):
                self.cls[t] = 'W'
            elif s == 'g' or s in '-=' or (s == '0' and n <= letmax) or (primeletters and s == "'"):
                self.cls[t] = 'L'
            else:
                self.cls[t] = 'S'
                if s in order:
                    syl_slots.append((order.index(s), n, t))
                else:
                    self.free.append(t)
        syl_slots.sort()
        self.slots = [t for _, _, t in syl_slots]          # ordered syllable slots
        self.letters = sorted(t for t in self.cls if self.cls[t] == 'L')
        self.segs = []
        cur = []
        for t in toks:
            if self.cls[t] == 'W':
                if cur:
                    self.segs.append(cur)
                cur = []
            else:
                cur.append(t)
        if cur:
            self.segs.append(cur)
        self.tok_segs = collections.defaultdict(set)
        for i, s in enumerate(self.segs):
            for t in s:
                self.tok_segs[t].add(i)


class Solver:
    def __init__(self, prob, U, lm, lam=0.6, nullpen=4.0, seed=0, nullok=False):
        random.seed(seed)
        self.nullok = nullok
        self.p = prob; self.U = U; self.lm = lm; self.lam = lam; self.nullpen = nullpen
        self.letters = list(LETFREQ)
        self.letw = [LETFREQ[c] for c in self.letters]
        self.map = {}
        for t in prob.letters:
            self.map[t] = random.choices(self.letters, self.letw)[0]
        k = len(prob.slots)
        self.idx = sorted(random.sample(range(len(U)), k))
        for t, i in zip(prob.slots, self.idx):
            self.map[t] = U[i]
        for t in prob.free:
            self.map[t] = random.choice(U)
        self.segscore = [self.score_seg(i) for i in range(len(prob.segs))]
        self.struct = self.structural()

    def render(self, seg):
        return ''.join(self.map[t] for t in seg)

    def score_seg(self, i):
        txt = self.render(self.p.segs[i])
        return self.lm.score(txt) + self.lam * len(txt)

    def structural(self):
        return -self.nullpen * sum(1 for t in self.p.letters if self.map[t] == '')

    def total(self):
        return sum(self.segscore) + self.struct

    def propose(self):
        r = random.random()
        p = self.p
        if r < 0.40 and p.letters:
            t = random.choice(p.letters)
            new = random.choices(self.letters, self.letw)[0] if (self.nullok and random.random() > 0.03) else random.choices(self.letters, self.letw)[0]
            if self.nullok and random.random() < 0.03:
                new = ''
            if new == self.map[t]:
                return None
            return {t: new}, None
        if r < 0.50 and len(p.letters) > 1:
            a, b = random.sample(p.letters, 2)
            if self.map[a] == self.map[b]:
                return None
            return {a: self.map[b], b: self.map[a]}, None
        if r < 0.85 and p.slots:
            i = random.randrange(len(p.slots))
            lo = self.idx[i-1] if i > 0 else -1
            hi = self.idx[i+1] if i + 1 < len(p.slots) else len(self.U)
            if hi - lo <= 2:
                return None
            new = random.randint(lo + 1, hi - 1)
            if new == self.idx[i]:
                return None
            return {p.slots[i]: self.U[new]}, [(i, new)]
        if r < 0.95 and p.slots:
            i = random.randrange(len(p.slots)); j = min(len(p.slots) - 1, i + random.randint(0, 12))
            d = random.choice([-3, -2, -1, 1, 2, 3])
            lo = self.idx[i-1] if i > 0 else -1
            hi = self.idx[j+1] if j + 1 < len(p.slots) else len(self.U)
            if self.idx[i] + d <= lo or self.idx[j] + d >= hi:
                return None
            ch = [(k, self.idx[k] + d) for k in range(i, j + 1)]
            return {p.slots[k]: self.U[v] for k, v in ch}, ch
        if p.free:
            t = random.choice(p.free)
            new = random.choice(self.U)
            if new == self.map[t]:
                return None
            return {t: new}, None
        return None

    def anneal(self, iters=300000, T0=3.0, T1=0.1, log=50000):
        cur = self.total(); best = cur; bestmap = dict(self.map); bestidx = list(self.idx)
        t0 = time.time()
        for it in range(iters):
            T = T0 * (T1 / T0) ** (it / iters)
            prop = self.propose()
            if not prop:
                continue
            chg, idxch = prop
            old = {t: self.map[t] for t in chg}
            self.map.update(chg)
            segs = set().union(*(self.p.tok_segs[t] for t in chg))
            newscores = {i: self.score_seg(i) for i in segs}
            newstruct = self.structural()
            delta = sum(newscores[i] - self.segscore[i] for i in segs) + newstruct - self.struct
            if delta >= 0 or random.random() < math.exp(delta / T):
                for i in segs:
                    self.segscore[i] = newscores[i]
                self.struct = newstruct
                if idxch:
                    for k, v in idxch:
                        self.idx[k] = v
                cur += delta
                if cur > best:
                    best = cur; bestmap = dict(self.map); bestidx = list(self.idx)
            else:
                self.map.update(old)
            if log and it % log == 0:
                print(f'  it {it} T {T:.2f} cur {cur:.1f} best {best:.1f} {time.time()-t0:.0f}s', flush=True)
        self.map = bestmap; self.idx = bestidx
        self.segscore = [self.score_seg(i) for i in range(len(self.p.segs))]
        self.struct = self.structural()
        return best


def decode_text(prob, m):
    out = []
    for t in prob.toks:
        if prob.cls[t] == 'W':
            out.append(' [' + t + '] ')
        else:
            u = m[t]
            out.append(u.upper() if len(u) > 1 else (u or '_'))
    return ''.join(out)


def accuracy(prob, m, truth):
    ok = tot = 0
    for t in prob.toks:
        if prob.cls[t] == 'W':
            continue
        tot += 1
        if truth.get(t) == m.get(t):
            ok += 1
    return ok / tot


def read_truth(path):
    truth = {}
    for line in open(path, encoding='utf-8'):
        if line.strip() and not line.startswith('#'):
            k, v = line.rstrip('\n').split('\t')
            truth[k] = v
    return truth


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cipher'); ap.add_argument('--truth'); ap.add_argument('--iters', type=int, default=300000)
    ap.add_argument('--seeds', type=int, default=3); ap.add_argument('--order', default="0'" + UMLAUT)
    ap.add_argument('--lam', type=float, default=0.6); ap.add_argument('--nullpen', type=float, default=4.0)
    ap.add_argument('--letmax', type=int, default=45); ap.add_argument('--nowords', action='store_true'); ap.add_argument('--primeletters', action='store_true')
    ap.add_argument('--truthscore', action='store_true'); ap.add_argument('--nullok', action='store_true')
    ap.add_argument('--seed0', type=int, default=0); ap.add_argument('--T0', type=float, default=3.0); ap.add_argument('--T1', type=float, default=0.1)
    a = ap.parse_args()
    toks = load_tokens(a.cipher)
    prob = Problem(toks, order=a.order, letmax=a.letmax, primeletters=a.primeletters)
    U = units(words=not a.nowords)
    lm = LM()
    print(f'{len(toks)} tokens; letters {len(prob.letters)} slots {len(prob.slots)} free {len(prob.free)} '
          f'W {sum(1 for t in prob.cls if prob.cls[t]=="W")}; {len(prob.segs)} segments; {len(U)} units')
    truth = read_truth(a.truth) if a.truth else None
    if truth and a.truthscore:
        s = Solver(prob, U, lm, a.lam, a.nullpen)
        s.map = {t: truth.get(t, '') for t in prob.cls if prob.cls[t] != 'W'}
        s.segscore = [s.score_seg(i) for i in range(len(prob.segs))]; s.struct = s.structural()
        print('TRUE KEY score', round(s.total(), 1))
    for seed in range(a.seed0, a.seed0 + a.seeds):
        s = Solver(prob, U, lm, a.lam, a.nullpen, seed=seed, nullok=a.nullok)
        best = s.anneal(a.iters, T0=a.T0, T1=a.T1)
        acc = accuracy(prob, s.map, truth) if truth else float('nan')
        print(f'seed {seed} best {best:.1f} acc {acc:.3f}')
        print(decode_text(prob, s.map)[:1500])
        print('KEY:', ' '.join(f'{t}={s.map[t] or "_"}' for t in prob.letters + prob.slots + prob.free))
