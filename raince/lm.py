"""Character n-gram LM over period French, built from repo corpora."""
import re, pickle, os, math, unicodedata
from collections import defaultdict

def norm(t):
    t = unicodedata.normalize('NFD', t)
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    t = t.lower().replace('j', 'i').replace('v', 'u').replace('w', 'u')
    t = re.sub(r"[^a-z]+", ' ', t)
    return re.sub(r'  +', ' ', t)

class LM:
    def __init__(self, n=5):
        self.n = n; self.c = defaultdict(lambda: defaultdict(int))
    def train(self, txt):
        t = ' ' + norm(txt) + ' '
        n = self.n
        for i in range(len(t)-n):
            self.c[t[i:i+n-1]][t[i+n-1]] += 1
    def finalize(self):
        self.p = {}
        tot = defaultdict(int)
        for k, d in self.c.items():
            s = sum(d.values()); tot[k] = s
            self.p[k] = {ch: math.log((v+0.1)/(s+0.1*27)) for ch, v in d.items()}
        self.back = math.log(0.1/(0.1*27))
        self.c = None
    def score(self, s):
        s = ' ' + s + ' '; n = self.n; tot = 0.0
        for i in range(len(s)-n+1):
            d = self.p.get(s[i:i+n-1])
            tot += (d.get(s[i+n-1], self.back) if d else self.back)
        return tot

if __name__ == '__main__':
    import glob, sys
    lm = LM(5)
    files = (glob.glob('../dubellay/ref/legrand3_*.txt') + glob.glob('../nevers1593/*.txt')
             + glob.glob('../debosnys/corpus/fr*.txt'))
    tot = 0
    for f in files:
        try: t = open(f, encoding='utf-8', errors='ignore').read()
        except Exception: continue
        lm.train(t); tot += len(t)
    lm.finalize()
    pickle.dump(dict(n=lm.n, p=lm.p, back=lm.back), open('fr5.pkl', 'wb'))
    print('trained on', tot, 'chars from', len(files), 'files; contexts', len(lm.p))
