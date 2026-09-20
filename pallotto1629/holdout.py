"""Held-out test: does a two-digit key learned on the first part of R286
predict the rest, better than the same key randomly permuted?

Non-circular: the table is frozen before it sees the held-out region, and the
control permutes the letters among the codes, keeping every other property.
"""
import random
from collections import Counter, defaultdict
from solve import load_doc, norm_plain
from align4 import align2r

C, _ = load_doc('decode/R286.txt')
P = norm_plain(open('crib153.txt', encoding='utf-8').read())

SPLIT_D = int(len(C) * 0.55)
SPLIT_P = int(1785 * 0.55)          # ~ letters covered by that many digits, if w=2

Ctr, Cte = C[:SPLIT_D], C[SPLIT_D:]
Ptr, Pte = P[:SPLIT_P], P[SPLIT_P:SPLIT_P + 1200]


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


def evaluate(table, Cx, Px):
    """Align with the table FROZEN; count exact confirmations."""
    sc, ops, endj = align2r(Cx, Px, table, W=160, hit=3.0, mis_pen=-25.0,
                            unk_pen=-0.3, slip_pen=8.0, null_pen=10.0, del_pen=10.0)
    hit = sum(1 for k, c, l in ops if k == 'S' and table.get(c) == l)
    tot = sum(1 for k, c, l in ops if k == 'S')
    return hit, tot, endj, sc


if __name__ == '__main__':
    tbl = learn(Ctr, Ptr)
    print('learned codes:', len(tbl))
    h, t, e, sc = evaluate(tbl, Cte, Pte)
    print('HELD OUT   : confirmations %d over %d letters = %.3f   DPscore %.0f' % (h, e, h/max(e,1), sc))
    letters = list(tbl.values())
    rng = random.Random(7)
    scores = []
    for r in range(8):
        sh = letters[:]
        rng.shuffle(sh)
        ctrl = dict(zip(tbl.keys(), sh))
        hh, tt, ee, ss = evaluate(ctrl, Cte, Pte)
        scores.append((hh/max(ee,1), ss))
    print('CONTROLS   : %s' % ' '.join('%.3f' % a for a,b in scores))
    print('control rate mean %.3f, DPscore mean %.0f' % (sum(a for a,b in scores)/len(scores), sum(b for a,b in scores)/len(scores)))
