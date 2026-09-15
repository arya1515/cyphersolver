"""Exhaustive sweep of the simple transposition families on BLUME telegram 1 (615 letters), Spanish quadgrams.

Every family is expressed as a permutation of positions. For each permutation P both readings are tried:
plaintext = ct[P] and plaintext = ct[P^-1]. A planted control encrypts real Spanish with one member of each
family and checks it is found.

Families: rail fence (2-60 rails, all offsets); decimation / skip (every step coprime to n, every start);
route transpositions on grids of width 2-60 (rows written left-to-right, then read by: columns down, columns up,
snake columns, rows reversed, snake rows, diagonals, anti-diagonals, spiral in both senses from each corner).
"""
import math, sys
import numpy as np
from tg import CT
import trans

n = len(CT)
A = np.frombuffer(CT.encode(), dtype=np.uint8) - 97


def load_q():
    q = trans.Q()
    table = np.full(26 ** 4, q.floor, dtype=np.float32)
    for k, v in q.d.items():
        if len(k) == 4:
            table[((ord(k[0]) - 97) * 26 + ord(k[1]) - 97) * 676 + (ord(k[2]) - 97) * 26 + ord(k[3]) - 97] = v
    return table


T = load_q()


def score(idx_arr):
    s = A[idx_arr].astype(np.int64)
    code = ((s[:-3] * 26 + s[1:-2]) * 26 + s[2:-1]) * 26 + s[3:]
    return float(T[code].sum()) / (len(s) - 3)


def rail(r, off):
    cyc = 2 * (r - 1)
    rows = [[] for _ in range(r)]
    for i in range(n):
        p = (i + off) % cyc
        rows[p if p < r else cyc - p].append(i)
    return [i for row in rows for i in row]


def grid_routes(w):
    h = math.ceil(n / w)
    pos = lambda r, c: r * w + c
    valid = lambda r, c: pos(r, c) < n
    routes = {}
    routes['cols_down'] = [pos(r, c) for c in range(w) for r in range(h) if valid(r, c)]
    routes['cols_up'] = [pos(r, c) for c in range(w) for r in reversed(range(h)) if valid(r, c)]
    routes['cols_snake'] = [pos(r, c) for c in range(w) for r in (range(h) if c % 2 == 0 else reversed(range(h))) if valid(r, c)]
    routes['cols_rtl_down'] = [pos(r, c) for c in reversed(range(w)) for r in range(h) if valid(r, c)]
    routes['rows_rev'] = [pos(r, c) for r in range(h) for c in reversed(range(w)) if valid(r, c)]
    routes['rows_snake'] = [pos(r, c) for r in range(h) for c in (range(w) if r % 2 == 0 else reversed(range(w))) if valid(r, c)]
    routes['diag'] = [pos(r, d - r) for d in range(h + w) for r in range(h) if 0 <= d - r < w and valid(r, d - r)]
    routes['antidiag'] = [pos(r, w - 1 - (d - r)) for d in range(h + w) for r in range(h) if 0 <= d - r < w and valid(r, w - 1 - (d - r))]
    # spirals over the full h x w rectangle, skipping cells beyond n
    def spiral(cw=True):
        top, bot, left, right = 0, h - 1, 0, w - 1; out = []
        while top <= bot and left <= right:
            if cw:
                out += [pos(top, c) for c in range(left, right + 1)]
                out += [pos(r, right) for r in range(top + 1, bot + 1)]
                if top < bot: out += [pos(bot, c) for c in range(right - 1, left - 1, -1)]
                if left < right: out += [pos(r, left) for r in range(bot - 1, top, -1)]
            else:
                out += [pos(r, left) for r in range(top, bot + 1)]
                out += [pos(bot, c) for c in range(left + 1, right + 1)]
                if left < right: out += [pos(r, right) for r in range(bot - 1, top - 1, -1)]
                if top < bot: out += [pos(top, c) for c in range(right - 1, left, -1)]
            top += 1; bot -= 1; left += 1; right -= 1
        return [p for p in out if p < n]
    routes['spiral_cw'] = spiral(True)
    routes['spiral_ccw'] = spiral(False)
    return {k: v for k, v in routes.items() if len(v) == n and len(set(v)) == n}


def candidates():
    for r in range(2, 61):
        for off in range(2 * (r - 1)):
            yield 'rail r=%d off=%d' % (r, off), rail(r, off)
    for step in range(2, n):
        if math.gcd(step, n) == 1:
            for start in range(0, n, 1 if step < 40 else 5):
                yield 'skip step=%d start=%d' % (step, start), [(start + step * i) % n for i in range(n)]
    for w in range(2, 61):
        for name, rt in grid_routes(w).items():
            yield 'route w=%d %s' % (w, name), rt
            yield 'route w=%d %s reversed' % (w, name), rt[::-1]


def sweep(top=12):
    best = []
    count = 0
    for name, perm in candidates():
        P = np.array(perm)
        inv = np.empty(n, dtype=np.int64); inv[P] = np.arange(n)
        for tag, idx in (('fwd', P), ('inv', inv)):
            s = score(idx); count += 1
            best.append((s, name + ' ' + tag, idx))
        if len(best) > 2000:
            best.sort(key=lambda x: -x[0]); del best[top * 5:]
    best.sort(key=lambda x: -x[0])
    return count, best[:top]


if __name__ == '__main__':
    count, best = sweep()
    print('%d readings scored; Spanish text scores about -4.1, shuffled -6.3, ciphertext as-is %.3f' % (count, score(np.arange(n))))
    for s, name, idx in best:
        print('  %.3f  %-40s %s' % (s, name, ''.join(chr(97 + A[i]) for i in idx[:60])))
