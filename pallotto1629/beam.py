"""Beam search that aligns a digit stream to known plaintext under a HARD key constraint.

The key must be a function code -> letter. A hypothesis that would map one code to two
different letters is killed outright, so a misaligned path cannot survive: it stops
earning confirmations and dies against the beam.

Score = confirmations (code already in the map and it agrees) minus repair penalties.
Repairs model transcription slips, nulls and crib/manuscript divergence.
"""
from solve import load_doc, norm_plain


class H:
    __slots__ = ('i', 'j', 'sc', 'mp', 'rep', 'par', 'op')

    def __init__(self, i, j, sc, mp, rep, par=None, op=None):
        self.i, self.j, self.sc, self.mp, self.rep = i, j, sc, mp, rep
        self.par, self.op = par, op


def beam(C, P, width=3000, slip=2.5, null=3.0, drop=3.0, w=2):
    """w = code width in digits."""
    n, m = len(C), len(P)
    start = H(0, 0, 0.0, {}, 0)
    cur = [start]
    best_done = None
    while cur:
        nxt = {}

        def push(h):
            k = (h.i, h.j)
            o = nxt.get(k)
            if o is None or h.sc > o.sc:
                nxt[k] = h

        for h in cur:
            i, j = h.i, h.j
            if j >= m or i + w > n:
                if best_done is None or h.sc > best_done.sc:
                    best_done = h
                continue
            # normal: w digits -> 1 letter
            code = C[i:i + w]
            ltr = P[j]
            t = h.mp.get(code)
            if t is None:
                mp = dict(h.mp)
                mp[code] = ltr
                push(H(i + w, j + 1, h.sc, mp, h.rep, h, ('S', code, ltr)))
            elif t == ltr:
                push(H(i + w, j + 1, h.sc + 1.0, h.mp, h.rep, h, ('=', code, ltr)))
            # else: hard conflict, no transition
            # repairs
            if h.rep < 400:
                if i + 1 <= n:
                    push(H(i + 1, j, h.sc - slip, h.mp, h.rep + 1, h, ('x', C[i:i + 1], '')))
                if i + w <= n:
                    push(H(i + w, j, h.sc - null, h.mp, h.rep + 1, h, ('N', code, '')))
                push(H(i, j + 1, h.sc - drop, h.mp, h.rep + 1, h, ('D', '', ltr)))
        if not nxt:
            break
        cur = sorted(nxt.values(), key=lambda x: -x.sc)[:width]
        if cur[0].j >= m or cur[0].i + w > n:
            pass
    # walk back
    h = best_done or (cur[0] if cur else start)
    ops = []
    g = h
    while g is not None and g.op is not None:
        ops.append(g.op)
        g = g.par
    ops.reverse()
    return h, ops


def report(h, ops):
    conf = sum(1 for k, c, l in ops if k == '=')
    new = sum(1 for k, c, l in ops if k == 'S')
    rep = sum(1 for k, c, l in ops if k in 'xND')
    return dict(score=round(h.sc, 1), letters=h.j, digits=h.i,
                confirmed=conf, assigned=new, repairs=rep, codes=len(h.mp))
