# Character n-gram LM over letters only (spaces stripped). Same design as chaulnes/lm.py, order 6.
# Corpus: ../chaulnes/corpus_fr.txt (Recueil Rome II, Gerin, 6.1 M chars) + Guizot's appendix of Bordeaux's
# despatches 1653-58 (guizot_docs_raw.txt, 0.42 M chars, OCR), all reduced to a-z.
import math, collections, pickle, re, sys, unicodedata
N = 6

def norm(t):
    t = unicodedata.normalize('NFD', t)
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn').lower()
    return re.sub(r'[^a-z]+', ' ', t)

def train(out='lm6.pkl'):
    t = open('../chaulnes/corpus_fr.txt', encoding='utf-8').read()
    t += ' ' + norm(open('guizot_docs_raw.txt', encoding='utf-8').read())
    open('corpus_fr.txt', 'w', encoding='utf-8').write(re.sub(r'\s+', ' ', t))
    t = re.sub(r'[^a-z]', '', t)
    cnts = [collections.Counter() for _ in range(N + 1)]
    for n in range(1, N + 1):
        c = cnts[n]
        for i in range(len(t) - n + 1):
            c[t[i:i+n]] += 1
    # prune singletons at high orders to keep the pickle small
    for n in range(4, N + 1):
        cnts[n] = collections.Counter({k: v for k, v in cnts[n].items() if v > 1})
    pickle.dump((N, cnts, len(t)), open(out, 'wb'))
    print('trained on', len(t), 'letters')

class LM:
    def __init__(self, path='lm6.pkl', order=None):
        self.N, self.cnts, self.total = pickle.load(open(path, 'rb'))
        if order:
            self.N = min(order, self.N)
        self.V = 26
        self.cache = {}

    def logp(self, ctx, ch):
        key = ctx + ch
        v = self.cache.get(key)
        if v is not None:
            return v
        v = math.log(self._p(ctx, ch, len(ctx) + 1))
        self.cache[key] = v
        return v

    def _p(self, ctx, ch, n):
        if n == 1:
            return (self.cnts[1][ch] + 1) / (self.total + self.V)
        den = self.cnts[n-1][ctx]
        lower = self._p(ctx[1:], ch, n - 1)
        if den == 0:
            return lower
        num = self.cnts[n][ctx + ch]
        d = 0.75
        return max(num - d, 0) / den + (d * max(1, min(den, 10)) / den) * lower

    def score(self, text):
        text = re.sub(r'[^a-z]', '', text)
        s = 0.0
        for i in range(len(text)):
            ctx = text[max(0, i - self.N + 1):i]
            s += self.logp(ctx, text[i])
        return s

if __name__ == '__main__':
    train()
    lm = LM()
    for s in ['le parlement a este dissous par le general', 'xq zzk pql mmn a rt ee oo',
              'vous avez faites pour obtenir l expedition des bulles', 'les les que pour les de les que']:
        t = re.sub(r'[^a-z]', '', s)
        print(round(lm.score(s) / len(t), 3), s)
