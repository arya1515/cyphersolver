"""D'Agapeyeff: drop the bijection assumption.

solve.py assumed one cell = one letter and swapped letters between cells, which is the right attack
only if the square is a plain one-to-one Polybius. The measured cell distribution says otherwise: 13
cells carry 188 of the 196 positions at roughly equal weight (9 to 20 each) and 5 more are nearly
absent. Too flat for one-to-one English, and too *few* distinct cells - 196 letters of English use
about 22.

Two readings fit that shape, and both break the bijection:
  * homophonic - common letters hold several cells each, which is what flattens the counts;
  * polyphonic - one cell stands for several letters, which is what reduces the count of distinct cells.

This solver allows any mapping from cells to letters (many cells to one letter, or one cell used for a
letter group), annealed on an English quadgram score, with restarts. It also runs the identical search
on shuffles of the same symbols as a control, so a "good" score can be judged against what the method
manufactures from noise.
"""
import collections, json, math, random, sys

from ct import DIGITS

AL = 'abcdefghijklmnopqrstuvwxyz'


def load_lm(path='../beale/en_lm.json'):
    d = json.load(open(path))
    q = d['quad']
    tot = sum(q.values())
    return {k: math.log10(v / tot) for k, v in q.items()}, math.log10(0.05 / tot)


LM, FLOOR = load_lm()


def score(s):
    return sum(LM.get(s[i:i + 4], FLOOR) for i in range(len(s) - 3)) / max(1, len(s) - 3)


def cells(body=392):
    d = DIGITS[:body]
    return [d[i:i + 2] for i in range(0, len(d), 2)]


def anneal(seq, restarts=24, iters=30000, seed=0, t0=1.2, t1=0.02):
    syms = sorted(set(seq))
    rnd = random.Random(seed)
    # bias the starting map toward frequent English letters for frequent cells
    order = [s for s, _ in collections.Counter(seq).most_common()]
    best = (-99.0, None)
    for r in range(restarts):
        if r == 0:
            key = {s: 'etaoinshrdlucmwfgypbvkxjqz'[i % 26] for i, s in enumerate(order)}
        else:
            key = {s: rnd.choice('etaoinshrdlucmwfgypb') for s in syms}
        cur = ''.join(key[c] for c in seq)
        cs = score(cur)
        for it in range(iters):
            T = t0 * (t1 / t0) ** (it / iters)
            s = rnd.choice(syms)
            old = key[s]
            new = rnd.choice(AL)
            if new == old:
                continue
            key[s] = new
            ns = score(''.join(key[c] for c in seq))
            if ns > cs or rnd.random() < math.exp((ns - cs) / max(T, 1e-6)):
                cs = ns
            else:
                key[s] = old
        if cs > best[0]:
            best = (cs, dict(key))
    pt = ''.join(best[1][c] for c in seq)
    return best[0], best[1], pt


def main():
    seq = cells()
    restarts = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    sc, key, pt = anneal(seq, restarts=restarts)
    print('real ciphertext : score %.3f' % sc)
    print('  distinct letters used by the key: %d' % len(set(key.values())))
    print('  ' + pt)
    rnd = random.Random(101)
    ctrl = []
    for t in range(3):
        s = seq[:]
        rnd.shuffle(s)
        cs, _, cpt = anneal(s, restarts=max(4, restarts // 4), seed=100 + t)
        ctrl.append(cs)
        print('control shuffle %d: score %.3f  %s' % (t, cs, cpt[:70]))
    print('\nreal %.3f  vs controls %s (mean %.3f)' % (sc, ['%.3f' % c for c in ctrl], sum(ctrl) / len(ctrl)))
    print('real English of this length scores about -4.8')


if __name__ == '__main__':
    main()
