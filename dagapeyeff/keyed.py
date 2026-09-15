"""Two things at once for the D'Agapeyeff challenge.

1. Calibrate the frequency test. The "best case chi-squared against English" used in control.py is a
   lower bound over all substitution keys; to know whether 34.1 is bad we need the distribution of that
   same statistic for real English samples of the same length, and the distribution of the number of
   distinct letters used.

2. Attack a keyed columnar transposition of the 196 cells. Repeated digrams are invariant to the
   substitution, so we can hill-climb column orders on that score alone without ever guessing the
   Polybius square. If a real transposition is present, the correct column order should push the count
   toward the English level (about 76) and well clear of the shuffle level (about 68).
"""
import collections, random, re, sys

from ct import DIGITS
from control import cells, freq_chi2_vs_english, digram_repeats

CHAL = cells(DIGITS[:392])


def calibrate_freq(n=196, ncells=25, trials=3000, seed=11):
    txt = open('../beale/lmcorpus/pg1342.txt', encoding='utf-8', errors='ignore').read().lower()
    txt = re.sub('[^a-z]', '', txt)
    rnd = random.Random(seed)
    chis, dis = [], []
    for _ in range(trials):
        i = rnd.randrange(0, len(txt) - n)
        c = collections.Counter(txt[i:i + n])
        chis.append(freq_chi2_vs_english(list(c.values()), ncells))
        dis.append(len(c))
    chis.sort()
    return chis, dis


def hillclimb_columns(seq, ncols, restarts=12, iters=4000, seed=0):
    """Maximise repeated digrams over column orders of a columnar transposition."""
    n = len(seq)
    if n % ncols:
        return None
    nrows = n // ncols
    cols = [seq[c * nrows:(c + 1) * nrows] for c in range(ncols)]   # ciphertext written in columns
    rnd = random.Random(seed)
    best = (-1, None)
    for _ in range(restarts):
        order = list(range(ncols))
        rnd.shuffle(order)

        def build(o):
            grid = [cols[c] for c in o]
            return [grid[c][r] for r in range(nrows) for c in range(ncols)]

        cur = digram_repeats(build(order))
        improved = True
        it = 0
        while improved and it < iters:
            improved = False
            for a in range(ncols):
                for b in range(a + 1, ncols):
                    order[a], order[b] = order[b], order[a]
                    v = digram_repeats(build(order))
                    it += 1
                    if v > cur:
                        cur = v
                        improved = True
                    else:
                        order[a], order[b] = order[b], order[a]
        if cur > best[0]:
            best = (cur, list(order))
    return best


def main():
    print('=== 1. calibrating the frequency test on real English (196 letters, 3000 samples)')
    chis, dis = calibrate_freq()
    obs_chi = freq_chi2_vs_english(list(collections.Counter(CHAL).values()), 25)
    worse = sum(1 for c in chis if c >= obs_chi)
    print('   English best-case chi2: median %.1f, 95th pct %.1f' % (chis[len(chis) // 2], chis[int(.95 * len(chis))]))
    print('   challenge = %.1f  -> %.1f%% of English samples are this bad or worse' % (obs_chi, 100 * worse / len(chis)))
    dc = collections.Counter(dis)
    fewer = sum(v for k, v in dc.items() if k <= 18)
    print('   distinct letters: English median %d; challenge uses 18; %.2f%% of English samples use <= 18'
          % (sorted(dis)[len(dis) // 2], 100 * fewer / len(dis)))

    print('\n=== 2. keyed columnar transposition, scored on repeated digrams (substitution-invariant)')
    print('   observed as written: %d ; random shuffle ~68 ; English ~76' % digram_repeats(CHAL))
    for ncols in (4, 7, 14, 28):
        r = hillclimb_columns(CHAL, ncols, restarts=int(sys.argv[1]) if len(sys.argv) > 1 else 10)
        if r:
            print('   %2d columns -> best %d repeated digrams  order %s' % (ncols, r[0], r[1]))


if __name__ == '__main__':
    main()
