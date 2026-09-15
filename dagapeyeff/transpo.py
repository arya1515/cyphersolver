"""Search pair-level rearrangements of the D'Agapeyeff cipher with a substitution-invariant test.

A transposition does not change symbol frequencies, so frequency tests say nothing about it. What a
transposition does change is *adjacency*. English has far more repeated digrams than chance, and that
property survives any one-to-one substitution: if two positions hold the same pair of symbols, they hold
the same pair of plaintext letters whatever the key. So "count of repeated digrams" is a
substitution-invariant score for a candidate reading order.

Calibrated against English text of the same length, and against random shuffles of the same symbols.
"""
import collections, itertools, random, re, json, sys

from ct import DIGITS


def pairs_of(body=392):
    d = DIGITS[:body]
    return [d[i:i + 2] for i in range(0, len(d), 2)]


def digram_repeats(seq):
    dg = collections.Counter(zip(seq, seq[1:]))
    return sum(v - 1 for v in dg.values() if v > 1)


def calibrate(n=196, trials=400):
    """What does real English of length n give, and what does a random shuffle give?"""
    txt = open('../beale/lmcorpus/pg1342.txt', encoding='utf-8', errors='ignore').read().lower()
    txt = re.sub('[^a-z]', '', txt)
    rnd = random.Random(1)
    eng = []
    for _ in range(trials):
        i = rnd.randrange(0, len(txt) - n)
        eng.append(digram_repeats(list(txt[i:i + n])))
    pr = pairs_of()
    sh = []
    for _ in range(trials):
        s = pr[:]
        rnd.shuffle(s)
        sh.append(digram_repeats(s))
    return (sum(eng) / len(eng), sum(sh) / len(sh))


def readings(pr):
    """Yield (name, sequence) for plausible rearrangements of the pair list."""
    n = len(pr)
    yield 'identity', pr
    yield 'reversed', pr[::-1]
    divs = [d for d in range(2, n) if n % d == 0]
    for c in divs:
        r = n // c
        grid = [pr[i * c:(i + 1) * c] for i in range(r)]
        # write by rows, read by columns
        yield 'rows%dx%d->cols' % (r, c), [grid[i][j] for j in range(c) for i in range(r)]
        # write by rows, read by columns bottom-up (boustrophedon)
        yield 'rows%dx%d->cols alt' % (r, c), [grid[i][j] if j % 2 == 0 else grid[r - 1 - i][j]
                                               for j in range(c) for i in range(r)]
        # write by columns, read by rows  (the inverse of the first)
        g2 = [[pr[j * r + i] for j in range(c)] for i in range(r)]
        yield 'cols%dx%d->rows' % (r, c), [g2[i][j] for i in range(r) for j in range(c)]


def main():
    pr = pairs_of()
    eng, shuf = calibrate(len(pr))
    print('calibration: English of this length averages %.1f repeated digrams; '
          'random shuffles of these symbols average %.1f' % (eng, shuf))
    rows = []
    for name, seq in readings(pr):
        rows.append((digram_repeats(seq), name))
    rows.sort(reverse=True)
    print('\nreading orders by repeated digrams:')
    for v, name in rows:
        print('  %-24s %3d' % (name, v))
    # also: does striking nulls help any of the top orders?
    print('\nwith the book\'s null rule applied to the best orders:')
    for v, name in rows[:4]:
        seq = dict(readings(pr))[name]
        for period in (3, 4, 5):
            for off in range(period):
                kept = [p for i, p in enumerate(seq) if i % period != off]
                print('  %-22s period %d off %d -> %3d' % (name, period, off, digram_repeats(kept)))


if __name__ == '__main__':
    main()
