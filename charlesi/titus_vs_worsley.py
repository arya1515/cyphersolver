"""Is the unread Worsley cipher of 22 May 1648 the same nomenclator as the Titus cipher?

The question is not idle. On 22 May 1648 Charles wrote from Carisbrooke to Captain Silius Titus and
to Edward Worsley on the same day, about the same escape. The contemporary letter-code preserved by
Peter Barwick makes Titus "W" and Worsley "Z", and the King's letter of 16 May has Worsley carrying
the post to Titus at Southampton. The Titus cipher is effectively published: Hillier printed fifteen
of those letters in 1852 with the decipherment set beside the code groups. The Worsley letter is not.

So: run the two repertoires against each other. This needs no key reconstruction and no guessing -
it compares which numbers each cipher actually uses.

Two statistics:

  1. Occupancy. Every nomenclator has a shape: bands of numbers it uses heavily, bands it leaves
     empty. If two messages come from one key, the smaller message's numbers should fall where the
     larger one's do.
  2. A permutation test on the one band that matters. The Titus letters use the low 100s constantly;
     the Worsley letter has no code between 98 and 203 at all. Draw 112 codes from the observed Titus
     usage distribution and ask how often that happens.

Usage: python titus_vs_worsley.py
"""
import collections, random, re, sys

import letters as L
import hillier as H


def titus_codes():
    """Every cipher group in the ciphered passages of Hillier's Titus letters.

    Taken from runs of at least three colon-separated numbers, which is what a ciphered passage
    looks like in his setting and what nothing else in the book looks like. Page numbers, years and
    footnote markers do not occur in runs of that shape.
    """
    t = H.load()
    out = []
    for m in re.finditer(r'(?:\d{1,3}\s*:\s*){2,}\d{1,3}', t):
        out.extend(int(x) for x in re.findall(r'\d{1,3}', m.group(0)))
    return out


def bands(seq, w=50, top=750):
    b = collections.Counter()
    for v in seq:
        b[(v // w) * w] += 1
    return b


def main():
    tc = titus_codes()
    wc = L.codes(L.MAY22)
    ac = L.codes(L.AUG1)
    print('Titus letters (Hillier 1852): %d code groups, %d distinct, range %d-%d'
          % (len(tc), len(set(tc)), min(tc), max(tc)))
    print('Worsley 22 May 1648         : %d code groups, %d distinct, range %d-%d'
          % (len(wc), len(set(wc)), min(wc), max(wc)))
    print('Prince Charles 1 Aug 1648   : %d code groups, %d distinct, range %d-%d'
          % (len(ac), len(set(ac)), min(ac), max(ac)))

    print('\n=== 1. OCCUPANCY BY BAND  (share of each message falling in each band of 50)')
    bt, bw, ba = bands(tc), bands(wc), bands(ac)
    allb = sorted(set(bt) | set(bw) | set(ba))
    print('%-12s %14s %14s %14s' % ('band', 'Titus', 'Worsley', '1 Aug'))
    for b in allb:
        print('%4d-%-7d %8d %5.1f%% %8d %5.1f%% %8d %5.1f%%'
              % (b, b + 49,
                 bt[b], 100.0 * bt[b] / len(tc),
                 bw[b], 100.0 * bw[b] / len(wc),
                 ba[b], 100.0 * ba[b] / len(ac)))

    print('\n=== 2. THE DEAD BAND 98-203')
    lo, hi = 98, 203
    t_in = sum(1 for v in tc if lo <= v <= hi)
    w_in = sum(1 for v in wc if lo <= v <= hi)
    a_in = sum(1 for v in ac if lo <= v <= hi)
    p_t = t_in / len(tc)
    print('   Titus   : %d of %d code groups lie in 98-203  (%.1f%%)' % (t_in, len(tc), 100 * p_t))
    print('   Worsley : %d of %d' % (w_in, len(wc)))
    print('   1 Aug   : %d of %d' % (a_in, len(ac)))
    print('   If the Worsley letter were drawn from the Titus repertoire, the expected count is'
          ' %.1f.' % (p_t * len(wc)))
    print('   P(none at all) = (1-%.4f)^%d = %.3g' % (p_t, len(wc), (1 - p_t) ** len(wc)))

    print('\n=== 3. PERMUTATION TEST  (draw from the observed Titus usage distribution)')
    rnd = random.Random(16480522)
    trials = 200000
    hits_band = hits_max = both = 0
    wmax = max(wc)
    for _ in range(trials):
        s = [tc[rnd.randrange(len(tc))] for _ in range(len(wc))]
        b = not any(lo <= v <= hi for v in s)
        m = max(s) <= wmax
        hits_band += b
        hits_max += m
        both += b and m
    print('   none in 98-203              : %d / %d  p = %.5f' % (hits_band, trials, hits_band / trials))
    print('   nothing above %d            : %d / %d  p = %.5f' % (wmax, hits_max, trials, hits_max / trials))
    print('   both                        : %d / %d  p = %.5f' % (both, trials, both / trials))

    print('\n=== 4. SHARED AND EXCLUSIVE CODES')
    st, sw = set(tc), set(wc)
    print('   in both repertoires : %d  %s' % (len(st & sw), sorted(st & sw)))
    print('   Worsley only        : %d  %s' % (len(sw - st), sorted(sw - st)))
    print('   Titus codes above the Worsley maximum (%d): %d distinct'
          % (wmax, len({v for v in st if v > wmax})))


if __name__ == '__main__':
    main()
