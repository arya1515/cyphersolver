"""Recover the key using the published plaintext's own 5-grams as the scorer."""
import random, re, sys
import segclimb
from segclimb import stream, text, build
import grid

P = re.sub('[^a-z]', '', open('plaintext_tna.txt').read().lower())
G = {P[i:i+5] for i in range(len(P)-4)}

class CQ:
    def score(self, s):
        return sum(1 for i in range(len(s)-4) if s[i:i+5] in G)

if __name__ == '__main__':
    S = stream(); q = CQ()
    rowb = []; acc = 0
    for r in grid.load():
        acc += len([c for c in r if grid.norm(c)]); rowb.append(acc)
    for W in (20, 21, 22):
        best = None
        for r in range(int(sys.argv[1])):
            rnd = random.Random(r)
            init = rowb[:-1]
            drop = rnd.sample(range(len(init)), 21 - (W - 1)) if W < 22 else []
            init = [x for i, x in enumerate(init) if i not in drop]
            res = segclimb.run(S, W, q, rnd, init)
            if best is None or res[0] > best[0]: best = res
        bs, cuts, order = best
        t = text(build(S, cuts, order)[0])
        print('W=%d score %d of %d possible' % (W, bs, len(t) - 4))
        print('   cuts', cuts, 'order', order)
        print('  ', t[:400])
