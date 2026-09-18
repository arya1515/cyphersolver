"""Hill-climb cluster->letter map for the Raince stream, scored by a space-free French 6-gram LM.
Initialised from the visual labelling of the cluster sheets against Tomokiyo's key."""
import json, pickle, random, sys, math

D = pickle.load(open('frns6.pkl', 'rb')); N = D['n']; P = D['p']; BACK = D['back']
ALPH = 'abcdefghilmnopqrstuy'          # letters the key uses (no j k w x z-rare)
CHOICES = list(ALPH) + ['', 'z']

def score(s):
    tot = 0.0
    for i in range(len(s)-N+1):
        d = P.get(s[i:i+N-1])
        tot += (d.get(s[i+N-1], BACK) if d else BACK)
    return tot

d = json.load(open('raince_tokens.json'))
lines = {}
for page in d['regions']:
    ts = [t for t in d['tokens'] if t['page'] == page]
    n = len(d['regions'][page]['lines'])
    lines[page] = [[t['cl'] for t in sorted([x for x in ts if x['line'] == k], key=lambda x: x['x0'])]
                   for k in range(n)]
# one long stream per page (lines run on)
streams = {p: [c for ln in ls for c in ln] for p, ls in lines.items()}

INIT = {1:'a',2:'a',3:'b',4:'a',5:'a',6:'q',7:'c',8:'c',9:'c',10:'u',11:'s',12:'s',13:'s',
        14:'t',15:'t',16:'t',17:'u',18:'l',19:'t',20:'a',21:'u',22:'u',23:'u',24:'h',25:'n',
        26:'e',27:'e',28:'n',29:'e',30:'e',31:'',32:'',33:'s',34:'t',35:'l',36:'d',37:'',
        38:'e',39:'n',40:'',41:'d',42:'n',43:'l',44:'y',45:'m',46:'t',47:'f',48:'',49:'m',
        50:'r',51:'r',52:'r',53:'e',54:'l',55:'e',56:'e',57:'i',58:'p',59:'p',60:'s',61:'s',
        62:'s',63:'o',64:'o',65:'o',66:'s',67:'',68:'',69:'i',70:'i'}

def decode(m):
    return {p: ''.join(m.get(c, '') for c in st) for p, st in streams.items()}

PEN = -2.9   # cost of dropping a token, so deleting is not free
def total(m):
    dec = decode(m)
    ndel = sum(1 for st in streams.values() for c in st if m.get(c, '') == '')
    return sum(score(t) for t in dec.values()) + ndel * PEN

m = dict(INIT)
best = total(m)
print('init', round(best/1, 1))
cls = sorted(streams and {c for st in streams.values() for c in st})
rng = random.Random(0)
improved = True; it = 0
while improved and it < 40:
    improved = False; it += 1
    order = cls[:]; rng.shuffle(order)
    for c in order:
        cur = m[c]; bl, bs = cur, best
        for L in CHOICES:
            if L == cur: continue
            m[c] = L; s = total(m)
            if s > bs: bs, bl = s, L
        m[c] = bl
        if bl != cur: best = bs; improved = True
    print('pass', it, round(best, 1))
json.dump({str(k): v for k, v in m.items()}, open('map_lm.json', 'w'))
# report control line
ctrl = [60,32,6,23,70,56,62,14,63,57,46,53,25,43,5,8,63,10,50,15,36,56,62,1,17,63,44,38,67,11,33,53,60,16,58,1,51,14,44,59,64,21,50,17,56,42,70,51,49,8,44]
print('control f29r20 ->', ''.join(m.get(c,'') for c in ctrl))
print('truth         -> squiestoitenlacourtdesavoyeestpartypourveniricy')
nl = sum(1 for c in m.values() if c == '')
print('nulls:', [k for k,v in m.items() if v==''], 'count', nl)
