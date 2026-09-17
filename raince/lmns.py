"""Space-free character 6-gram LM over period French."""
import re, pickle, math, unicodedata, glob
from collections import defaultdict

def norm(t):
    t = unicodedata.normalize('NFD', t)
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    t = t.lower().replace('j', 'i').replace('v', 'u').replace('w', 'u')
    return re.sub(r"[^a-z]+", '', t)

N = 6
c = defaultdict(lambda: defaultdict(int))
tot = 0
files = (glob.glob('../dubellay/ref/legrand3_*.txt') + glob.glob('../nevers1593/*.txt')
         + glob.glob('../debosnys/corpus/fr*.txt'))
for f in files:
    try: t = norm(open(f, encoding='utf-8', errors='ignore').read())
    except Exception: continue
    tot += len(t)
    for i in range(len(t)-N):
        c[t[i:i+N-1]][t[i+N-1]] += 1
p = {}
for k, d in c.items():
    s = sum(d.values())
    p[k] = {ch: math.log((v+0.08)/(s+0.08*26)) for ch, v in d.items()}
back = math.log(0.08/(0.08*26))
pickle.dump(dict(n=N, p=p, back=back), open('frns6.pkl', 'wb'))
print('chars', tot, 'contexts', len(p))
