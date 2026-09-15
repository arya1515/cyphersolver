"""Is the 7-token near-repeat in the 22 May 1648 letter real, or an artefact of a small alphabet?

struct.py finds this in the Worsley letter:

    position 14   2 20 3 230 388 45 36
    position 79   1 20 2 230 388 46 36

Four of the seven positions match exactly and the other three differ by exactly 1. Under the
Sept-Nov nomenclator, codes that differ by 1 are different letters (2=h, 3=g; 45=n, 46=o), so this
pattern is not what that design produces. It is what a design produces in which each letter owns a
run of consecutive numbers - the arrangement used in, for example, the 1653 Bramhall-to-Ormond
cipher printed in the Ormonde calendar.

Before reading anything into it, test whether a 112-token message with this code-frequency profile
throws up such a match by accident. The null shuffles the observed multiset of codes, which holds
the length, the alphabet and every code's frequency fixed and destroys only the order.

Usage: python nearrepeat.py [trials]
"""
import collections, random, sys

import letters as L


def best_near_repeat(seq, tol=1):
    """Length of the longest pair of non-overlapping k-grams differing by at most tol per position.

    Requires at least one position to differ, so an exact repeat does not count: the question is
    specifically about near-matches.
    """
    n = len(seq)
    best = 0
    for i in range(n):
        for j in range(i + 1, n):
            k = 0
            diff = False
            while j + k < n and i + k < j:
                d = abs(seq[i + k] - seq[j + k])
                if d > tol:
                    break
                if d:
                    diff = True
                k += 1
            if diff and k > best:
                best = k
    return best


def longest_exact_repeat(seq):
    n = len(seq)
    best = 0
    for i in range(n):
        for j in range(i + 1, n):
            k = 0
            while j + k < n and i + k < j and seq[i + k] == seq[j + k]:
                k += 1
            best = max(best, k)
    return best


def main():
    trials = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    for let in L.ALL:
        seq = L.codes(let)
        obs = best_near_repeat(seq, tol=1)
        obs_ex = longest_exact_repeat(seq)
        rnd = random.Random(20210505)
        pool = list(seq)
        hits = hits_ex = 0
        dist = collections.Counter()
        for _ in range(trials):
            rnd.shuffle(pool)
            v = best_near_repeat(pool, tol=1)
            dist[v] += 1
            if v >= obs:
                hits += 1
            if longest_exact_repeat(pool) >= obs_ex and obs_ex:
                hits_ex += 1
        print('\n%s   [%s]' % (L.name(let), let['status']))
        print('   codes %d, distinct %d' % (len(seq), len(set(seq))))
        print('   longest exact repeat      : %d   p = %.5f' % (obs_ex, hits_ex / trials))
        print('   longest near-repeat (+-1) : %d   p = %.5f  (%d of %d shuffles matched or beat it)'
              % (obs, hits / trials, hits, trials))
        print('   null distribution of near-repeat length: %s'
              % ', '.join('%d:%.3f' % (k, dist[k] / trials) for k in sorted(dist) if dist[k] / trials > 0.001))


if __name__ == '__main__':
    main()
