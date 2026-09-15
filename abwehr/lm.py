"""Letter quadgram models for German, English and Dutch (umlauts folded: ae oe ue ss)."""
import collections, glob, math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
FOLD = [('ä', 'ae'), ('ö', 'oe'), ('ü', 'ue'), ('ß', 'ss'), ('é', 'e'), ('è', 'e'), ('ë', 'e'), ('ï', 'i'), ('à', 'a'),
        ('ê', 'e'), ('ô', 'o'), ('û', 'u'), ('ç', 'c'), ('ĳ', 'ij')]


def clean(t):
    t = t.lower()
    for a, b in FOLD: t = t.replace(a, b)
    return re.sub('[^a-z]', '', t)


def body(path):
    t = open(path, encoding='utf-8', errors='ignore').read()
    s = t.find('*** START'); e = t.find('*** END')
    return t[s if s > 0 else 0: e if e > 0 else len(t)]


class Q:
    def __init__(self, lang):
        pats = {'de': ['corpus/de*.txt'], 'nl': ['corpus/nl*.txt'], 'en': ['../beale/lmcorpus/pg1342.txt', '../beale/lmcorpus/pg2701.txt', '../beale/lmcorpus/pg98.txt', '../beale/lmcorpus/pg1400.txt']}[lang]
        cache = os.path.join(HERE, 'corpus', 'q4_%s.tsv' % lang)
        if os.path.exists(cache):
            d = {}
            for l in open(cache):
                k, v = l.split('\t'); d[k] = float(v)
            self.floor = d.pop('__floor__'); self.d = d
        else:
            cnt = collections.Counter()
            for p in pats:
                for f in glob.glob(os.path.join(HERE, p)):
                    s = clean(body(f))
                    cnt.update(s[i:i + 4] for i in range(len(s) - 3))
            tot = sum(cnt.values())
            self.d = {k: math.log10(v / tot) for k, v in cnt.items()}
            self.floor = math.log10(0.01 / tot)
            with open(cache, 'w') as fh:
                for k, v in self.d.items(): fh.write('%s\t%f\n' % (k, v))
                fh.write('__floor__\t%f\n' % self.floor)
        self.text_cache = None

    def score(self, s):
        d, f = self.d, self.floor
        return sum(d.get(s[i:i + 4], f) for i in range(len(s) - 3))

    def sample(self, lang, n, seed=0):
        import random
        pats = {'de': 'corpus/de*.txt', 'nl': 'corpus/nl*.txt', 'en': '../beale/lmcorpus/pg1342.txt'}[lang]
        s = clean(body(sorted(glob.glob(os.path.join(HERE, pats)))[0]))
        r = random.Random(seed).randrange(len(s) - n)
        return s[r:r + n]
