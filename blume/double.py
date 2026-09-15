"""Double columnar transposition: planted control first, then the telegram.

Decryption undoes key2 then key1. Search: alternate hill-climbing of the two permutations under Spanish
quadgrams, with restarts, for a given width pair.

Usage: python double.py control | python double.py real W1min W1max W2min W2max restarts
"""
import math, random, sys
import trans
from tg import CT
from trans import decrypt, col_lengths, clean


def encrypt(p, order):
    w = len(order); lens = col_lengths(len(p), w)
    cols = [''.join(p[r * w + c] for r in range(lens[c])) for c in range(w)]
    return ''.join(cols[c] for c in order)


def dd(ct, o1, o2):
    return decrypt(decrypt(ct, o2), o1)


def mutate(o, rnd):
    o = o[:]; w = len(o); r = rnd.random()
    if r < 0.5:
        a, b = rnd.sample(range(w), 2); o[a], o[b] = o[b], o[a]
    elif r < 0.85:
        a, b = sorted(rnd.sample(range(w + 1), 2)); blk = o[a:b]; del o[a:b]
        k = rnd.randrange(len(o) + 1); o[k:k] = blk
    else:
        k = rnd.randrange(1, w); o = o[k:] + o[:k]
    return o


def climb2(ct, w1, w2, q, rnd, iters=60000):
    o1 = list(range(w1)); rnd.shuffle(o1); o2 = list(range(w2)); rnd.shuffle(o2)
    cur = q.score(dd(ct, o1, o2)); best = (cur, o1[:], o2[:])
    T = 30.0
    for it in range(iters):
        if rnd.random() < 0.5: n1, n2 = mutate(o1, rnd), o2
        else: n1, n2 = o1, mutate(o2, rnd)
        v = q.score(dd(ct, n1, n2))
        if v > cur or rnd.random() < math.exp((v - cur) / T):
            o1, o2, cur = n1, n2, v
            if v > best[0]: best = (v, o1[:], o2[:])
        T = max(0.3, T * 0.99990)
    return best


def main():
    q = trans.Q(); n = len(CT); rnd = random.Random(3)
    if sys.argv[1] == 'control':
        t = open('corpus/es15532.txt', encoding='utf-8', errors='ignore').read()
        pt = clean(t[300000:305000])[:615]
        for w1, w2 in ((8, 11), (13, 17)):
            k1 = list(range(w1)); rnd.shuffle(k1); k2 = list(range(w2)); rnd.shuffle(k2)
            ct = encrypt(encrypt(pt, k1), k2)
            assert dd(ct, k1, k2) == pt
            best = max((climb2(ct, w1, w2, q, rnd) for _ in range(3)), key=lambda x: x[0])
            print('planted %d/%d: best %.3f, true %.3f, %s' % (w1, w2, best[0] / (n - 3), q.score(pt) / (n - 3), dd(ct, best[1], best[2])[:60]), flush=True)
    else:
        a, b, c, d, R = (int(x) for x in sys.argv[2:7])
        res = []
        for w1 in range(a, b + 1):
            for w2 in range(c, d + 1):
                best = max((climb2(CT, w1, w2, q, rnd, iters=30000) for _ in range(R)), key=lambda x: x[0])
                res.append((best[0] / (n - 3), w1, w2, dd(CT, best[1], best[2])))
                print('%2d/%2d %.3f %s' % (w1, w2, res[-1][0], res[-1][3][:60]), flush=True)
        res.sort(reverse=True)
        print('best', res[:3])


if __name__ == '__main__':
    main()
