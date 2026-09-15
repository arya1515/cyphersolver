"""lmns.py -- no-space letter 5-gram LM in cipher orthography (no h except ch+e/i, no doubled letters,
u=v, i=j) built from corpus_it.txt (build_it_lm.py). Cached in lm_ns.bin (pickle).
Interpolated absolute discounting. Provides logp(history, char) and an insertion bonus LAMBDA equal to the
mean per-letter cost on held-out text, so that output length is not penalised a priori."""
import pickle, pathlib, re, math, collections
HERE = pathlib.Path(__file__).parent
N = 5; D = 0.75
ALPHABET = 'abcdefgilmnopqrstuz'

def normalize_cipher_orthography(text):
    t = text.replace(' ', '')
    t = re.sub(r'ch(?=[ei])', 'K', t)         # protect ch before e/i
    t = t.replace('h', '').replace('K', 'ch')
    t = t.replace('k', 'c').replace('w', 'i').replace('y', 'i').replace('x', 's')
    t = re.sub(r'([^aeiou])\1', r'\1', t)      # no doubled consonants
    t = re.sub('[^' + ALPHABET + ']', '', t)
    return t

ROMAN = re.compile(r'^[ivxlcdm]+$')
KEEP = {'mi', 'vi', 'li', 'di', 'ci', 'il', 'vidi', 'dici', 'mili', 'cimici'}
def clean_words(words):
    """Drop Roman numerals (OCR of dates and folio numbers), which otherwise make 'iii' cheap."""
    return [w for w in words if not (len(w) >= 2 and ROMAN.match(w) and w not in KEEP)]

class LM:
    def __init__(self, counts, ctxtot, ctxtypes, unigram):
        self.counts = counts; self.ctxtot = ctxtot; self.ctxtypes = ctxtypes; self.uni = unigram
        self.memo = {}
        self.LAMBDA = 2.3
    def prob(self, hist, c):
        key = hist + c
        v = self.memo.get(key)
        if v is not None: return v
        if not hist:
            p = self.uni.get(c, 1e-6)
        else:
            tot = self.ctxtot.get(hist)
            lower = self.prob(hist[1:], c)
            if not tot:
                p = lower
            else:
                cnt = self.counts.get(hist + c, 0)
                p = (max(cnt - D, 0) + D * self.ctxtypes[hist] * lower) / tot
        self.memo[key] = p
        return p
    def logp(self, hist, c):
        if len(hist) > N-1: hist = hist[-(N-1):]
        return math.log(self.prob(hist, c))
    def score(self, text):
        s = 0.0
        for i, c in enumerate(text):
            s += self.logp(text[max(0, i-N+1):i], c)
        return s

def build(force=False):
    cache = HERE / 'lm_ns.bin'
    if cache.exists() and not force:
        d = pickle.load(open(cache, 'rb'))
        lm = LM(d['counts'], d['ctxtot'], d['ctxtypes'], d['unigram']); lm.LAMBDA = d['LAMBDA']
        return lm
    raw = (HERE / 'corpus_it.txt').read_text(encoding='utf-8')
    raw = ' '.join(clean_words(raw.split()))
    text = normalize_cipher_orthography(raw)
    held = text[-60000:]; train = text[:-60000]
    print('LM train letters', len(train), 'held', len(held))
    counts = collections.Counter()
    for n in range(2, N+1):
        for i in range(len(train) - n + 1):
            counts[train[i:i+n]] += 1
    ctxtot = collections.Counter(); ctxtypes = collections.Counter()
    for g, c in counts.items():
        ctx = g[:-1]; ctxtot[ctx] += c; ctxtypes[ctx] += 1
    uni = collections.Counter(train); tot = sum(uni.values())
    unigram = {c: (v + 1) / (tot + len(ALPHABET)) for c, v in uni.items()}
    counts = {g: c for g, c in counts.items() if c >= 2 or len(g) <= 3}
    lm = LM(counts, dict(ctxtot), dict(ctxtypes), unigram)
    lam = -lm.score(held) / len(held)
    lm.LAMBDA = lam
    lm.memo = {}
    print(f'held-out mean cost per letter: {lam:.3f} nats')
    pickle.dump({'counts': lm.counts, 'ctxtot': lm.ctxtot, 'ctxtypes': lm.ctxtypes, 'unigram': lm.uni, 'LAMBDA': lam}, open(cache, 'wb'))
    return lm

if __name__ == '__main__':
    import sys
    lm = build(force='--force' in sys.argv)
    print('lambda', lm.LAMBDA)
    for t in ['nostrosignoreascrittoavostrasignoria', 'zqpfkdrtlmzzbbccddeeffg', 'lasuamaestacesareaefrancia']:
        print(t, f'{lm.score(t)/len(t):.3f}')
