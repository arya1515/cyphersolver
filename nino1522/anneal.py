"""Many-to-one substitution annealer for the Niño 1522 block (cipher_p2.txt), scored by lang es-golden-age.
Usage: python nino1522/anneal.py [restarts] [fix=sign:letter,...]"""
import sys, random, math, re
sys.path.insert(0, '.')
from lang import lm

M = lm.load('es-golden-age')
CAP = 2   # at most two signs per letter (simple substitution with a few homophones)
A = 'abcdefghilmnopqrstuxyz'   # es-golden-age alphabet (early scheme: j->i, v->u)

def load():
    L = [l.rstrip('\n') for l in open('nino1522/cipher_p2.txt', encoding='utf-8') if not l.startswith('#')]
    t = ' '.join(L).replace('[mer por]', '').replace('[mer]', '')
    return ' '.join(t.split())

CT = load()
SIGNS = sorted(set(CT) - {' '})

def dec(k):
    return ''.join(' ' if c == ' ' else k[c] for c in CT)

def score(k):
    return M.score(lm.norm(dec(k), 'early'))

def run(fix, iters=40000, T0=3.0):
    k = dict(fix)
    for s in SIGNS:
        if s not in k:
            cnt = {}
            for v in k.values(): cnt[v] = cnt.get(v, 0) + 1
            k[s] = random.choice([c for c in A if cnt.get(c, 0) < CAP])
    free = [s for s in SIGNS if s not in fix]
    cur = score(k); best = (cur, dict(k))
    for i in range(iters):
        T = T0 * (1 - i / iters) + 0.05
        s = random.choice(free); old = k[s]
        cnt = {}
        for v in k.values(): cnt[v] = cnt.get(v, 0) + 1
        opts = [c for c in A if cnt.get(c, 0) < CAP and c != old]
        if not opts: continue
        k[s] = random.choice(opts)
        sc = score(k)
        if sc >= cur or random.random() < math.exp((sc - cur) / T):
            cur = sc
            if sc > best[0]: best = (sc, dict(k))
        else:
            k[s] = old
    return best

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    fix = {}
    if len(sys.argv) > 2:
        for p in sys.argv[2].split(','):
            a, b = p.split(':'); fix[a] = b
    res = sorted((run(fix) for _ in range(n)), key=lambda r: -r[0])
    for sc, k in res[:3]:
        print(round(sc, 1), ' '.join(f'{s}={k[s]}' for s in SIGNS))
        print('  ', dec(k))
