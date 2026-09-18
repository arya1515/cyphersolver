"""lm.py — period-French language model for the Bethune decoders.

Corpus: bethune/xivrey/*.txt (Berger de Xivrey, Recueil des lettres missives de Henri IV, IA djvu text)
plus any extra .txt passed on the command line. Normalisation: lowercase, accents stripped, j->i, v->u,
everything outside a-z dropped, so the model lives in the same alphabet as the decipherment.

Provides
  Lex      unigram counts, vocabulary
  Bigram   P(w2|w1) with Katz-style backoff to the unigram
  CharLM   order-6 character model with stupid backoff, for out-of-vocabulary words
Cached to bethune/lm_cache.pkl (rebuild with --rebuild).
"""
import os, re, sys, math, pickle, glob, collections, unicodedata

CACHE = 'bethune/lm_cache.pkl'

def norm(s):
    s = unicodedata.normalize('NFKD', s.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.replace('j', 'i').replace('v', 'u').replace('œ', 'oe').replace('æ', 'ae')
    return re.sub(r'[^a-z]', '', s)

def norm_keep_spaces(s):
    return ' '.join(norm(w) for w in s.split() if norm(w))


def tokenise(txt):
    for w in re.findall(r"[A-Za-zÀ-ÿ']+", txt):
        w = norm(w)
        if w: yield w

def build(paths):
    uni = collections.Counter(); bi = collections.Counter()
    chars = collections.Counter()
    for p in paths:
        txt = open(p, encoding='utf-8', errors='ignore').read()
        ws = ['<s>']
        for w in tokenise(txt):
            if len(w) > 20: continue
            ws.append(w)
        for i, w in enumerate(ws):
            uni[w] += 1
            if i: bi[(ws[i-1], w)] += 1
    # character n-grams over the same words
    for w, c in uni.items():
        if w == '<s>': continue
        s = '^' + w + '$'
        for i in range(len(s)):
            for n in range(1, 7):
                if i-n+1 < 0: break
                chars[s[i-n+1:i+1]] += c
    return uni, bi, chars

class LM:
    def __init__(self, uni, bi, chars):
        self.uni = uni; self.bi = bi; self.chars = chars
        self.N = sum(v for k, v in uni.items() if k != '<s>')
        self.V = len(uni)
        self.logN = math.log(self.N)
        self.bi_ctx = collections.Counter()
        for (a, b), c in bi.items(): self.bi_ctx[a] += c
    def logp_uni(self, w):
        c = self.uni.get(w, 0)
        return math.log((c + 0.05)/(self.N + 0.05*self.V))
    def logp_bi(self, w1, w2, lam=0.72):
        c12 = self.bi.get((w1, w2), 0); c1 = self.bi_ctx.get(w1, 0)
        pu = math.exp(self.logp_uni(w2))
        p = (lam*(c12/c1) if c1 else 0.0) + (1-lam)*pu
        return math.log(max(p, 1e-12))
    def logp_char(self, w, order=6):
        """stupid-backoff character model; returns log P(word) for an unseen word."""
        s = '^' + w + '$'; lp = 0.0
        for i in range(1, len(s)):
            got = False
            for n in range(min(order, i+1), 1, -1):
                ctx = s[i-n+1:i]; full = s[i-n+1:i+1]
                cc = self.chars.get(ctx, 0)
                if cc >= 3:
                    cf = self.chars.get(full, 0)
                    if cf > 0:
                        lp += math.log(cf/cc); got = True; break
                    lp += math.log(0.4); got = True; break
            if not got:
                c1 = self.chars.get(s[i], 0)
                lp += math.log((c1+1)/(self.N*6))
        return lp

def load(rebuild=False, extra=()):
    if not rebuild and os.path.exists(CACHE):
        uni, bi, chars = pickle.load(open(CACHE, 'rb'))
    else:
        paths = sorted(glob.glob('bethune/xivrey/*.txt')) + list(extra)
        print('building LM from', len(paths), 'files', file=sys.stderr)
        uni, bi, chars = build(paths)
        pickle.dump((uni, bi, chars), open(CACHE, 'wb'), protocol=4)
    return LM(uni, bi, chars)

if __name__ == '__main__':
    lm = load(rebuild='--rebuild' in sys.argv)
    print('words', lm.N, 'vocab', lm.V, 'bigrams', len(lm.bi), 'char-ngrams', len(lm.chars))
    for w in ['cardinal', 'aldobrandin', 'promotion', 'espaigne', 'saincte', 'volonte', 'ambassadeur']:
        print(f'{w:14s} uni {lm.uni.get(w,0):6d}')
    for a, b in [('le', 'cardinal'), ('sa', 'saincte'), ('du', 'pape'), ('le', 'roy')]:
        print(f'P({b}|{a}) = {math.exp(lm.logp_bi(a,b)):.5f}')
