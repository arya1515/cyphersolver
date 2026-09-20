"""Positive control.

Encipher the known plaintext with a random two-digit homophonic key, damage the
digit stream with transcription slips at a given rate, and ask whether the same
pipeline used on R286 recovers the key. Measured with the same held-out metric
and the same shuffled controls.

If the pipeline recovers synthetic text at the real noise level but not R286,
then R286 is not a two-digit homophonic encipherment of this plaintext.
"""
import random, sys
from collections import Counter, defaultdict
from solve import norm_plain
from align4 import align2r

FREQ = dict(a=11.7, e=11.8, i=11.3, o=9.8, n=6.9, r=6.4, t=5.6, l=6.5, s=5.0,
            c=4.5, d=3.7, u=5.1, p=3.0, m=2.5, v=2.1, g=1.6, f=1.2, b=0.9,
            h=1.5, q=0.5, z=0.5)


def make_key(rng):
    codes = ['%02d' % i for i in range(100)]
    rng.shuffle(codes)
    tot = sum(FREQ.values())
    key = {}
    i = 0
    for L, f in sorted(FREQ.items(), key=lambda x: -x[1]):
        n = max(1, round(f / tot * 100))
        for c in codes[i:i + n]:
            key[c] = L.upper()
        i += n
    for c in codes[i:]:
        key[c] = 'E'
    return key


def encipher(P, key, rng):
    inv = defaultdict(list)
    for c, l in key.items():
        inv[l].append(c)
    out = []
    for ch in P:
        opts = inv.get(ch)
        if not opts:
            opts = inv['E']
        out.append(rng.choice(opts))
    return ''.join(out)


def damage(C, rate, rng):
    """Insert/delete single digits at `rate` per digit."""
    out = []
    for d in C:
        r = rng.random()
        if r < rate / 2:
            continue                      # dropped digit
        out.append(d)
        if r > 1 - rate / 2:
            out.append(rng.choice('0123456789'))   # spurious digit
    return ''.join(out)


def learn(Cx, Px, iters=12):
    table = {}
    for _ in range(iters):
        sc, ops, endj = align2r(Cx, Px, table, W=160, hit=3.0, mis_pen=-25.0,
                                unk_pen=-0.3, slip_pen=8.0, null_pen=10.0, del_pen=10.0)
        v = defaultdict(Counter)
        for k, c, l in ops:
            if k == 'S':
                v[c][l] += 1
        new = {c: cc.most_common(1)[0][0] for c, cc in v.items()}
        if new == table:
            break
        table = new
    return table


def run(rate, seed=3):
    rng = random.Random(seed)
    P = norm_plain(open('crib153.txt', encoding='utf-8').read())
    key = make_key(rng)
    C = damage(encipher(P, key, rng), rate, rng)
    sp_d, sp_p = int(len(C) * 0.55), int(len(P) * 0.55)
    tbl = learn(C[:sp_d], P[:sp_p])
    # how much of the true key did we get back?
    agree = sum(1 for c, l in tbl.items() if key.get(c) == l)
    print('rate %.3f  digits %d  learned %d codes  TRUE-KEY AGREEMENT %d/%d = %.3f'
          % (rate, len(C), len(tbl), agree, len(tbl), agree / max(len(tbl), 1)))
    return agree / max(len(tbl), 1)


if __name__ == '__main__':
    for rate in (0.0, 0.005, 0.017, 0.04):
        run(rate)
