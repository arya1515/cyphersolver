"""Climb column order AND column cut points over the continuous cell stream."""
import random, re, sys
import grid, masc
from rebreak import EXP

def stream():
    return [grid.norm(c) for r in grid.load() for c in r if grid.norm(c)]

def text(toks):
    return ''.join('' if (t.isdigit() or t == 'likelyhood') else re.sub('[^a-z]', '', EXP.get(t, t.lower())) for t in toks)

def build(S, cuts, order):
    b = [0] + cuts + [len(S)]
    C = [S[b[i]:b[i+1]] for i in range(len(b)-1)]
    depth = max(len(c) for c in C)
    out = []
    for k in range(depth):
        for i in order:
            if k < len(C[i]): out.append(C[i][k])
    return out, C

def run(S, W, q, rnd, init=None):
    n = len(S)
    if init: cuts = init[:]
    else:
        cuts = sorted(rnd.sample(range(15, n-15), W-1))
        cuts = [round(n*(i+1)/W) for i in range(W-1)]
    order = list(range(W)); rnd.shuffle(order)
    sc = lambda c, o: q.score(text(build(S, c, o)[0]))
    best = sc(cuts, order)
    for it in range(40):
        imp = False
        for a in range(W):
            for b in range(W):
                if a == b: continue
                o = order[:]; x = o.pop(a); o.insert(b, x)
                v = sc(cuts, o)
                if v > best: best, order, imp = v, o, True
        for i in range(W-1):
            for d in (-3, -2, -1, 1, 2, 3):
                c = cuts[:]; c[i] += d
                lo = c[i-1] if i else 0; hi = c[i+1] if i < W-2 else n
                if not (lo + 10 < c[i] < hi - 10): continue
                v = sc(c, order)
                if v > best: best, cuts, imp = v, c, True
        if not imp: break
    return best, cuts, order

if __name__ == '__main__':
    q = masc.Q(); S = stream()
    W = int(sys.argv[1]); R = int(sys.argv[2])
    rowb = []; acc = 0
    for r in grid.load():
        acc += len([c for c in r if grid.norm(c)]); rowb.append(acc)
    res = []
    for r in range(R):
        rnd = random.Random(r)
        init = None
        if W == 21: init = [x for x in rowb[:-1] if x != rowb[20]]   # merge rows 21+22
        if W == 22: init = rowb[:-1]
        if W == 20: init = [x for x in rowb[:-1] if x not in (rowb[20], rowb[15])]
        bs, cuts, order = run(S, W, q, rnd, init)
        res.append((bs, cuts, order))
        print(r, round(bs), text(build(S, cuts, order)[0])[:100], flush=True)
    res.sort(reverse=True)
    bs, cuts, order = res[0]
    toks, C = build(S, cuts, order)
    print('best', round(bs), 'cuts', cuts, 'order', order)
    print(' '.join(toks))
