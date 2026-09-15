"""What kind of cipher are the two unread Isle of Wight letters, and is either attackable?

The published key is excluded (test_key.py). That leaves the question of whether anything can be
done without a key. For a nomenclator the answer is almost entirely determined by repetition: a
code group that occurs once carries no statistical information at all, so the fraction of the
message that is hapax is an upper bound on how much of it any analysis can ever recover.

Measured here, for both unread letters and for the two solved ones as controls:

  * inventory and hapax rate - how much of the text repeats
  * the two-part profile - where the letter codes and the word codes sit, found from the data
    rather than assumed, by looking at which code values carry the repeats
  * repeated n-grams - the only real handle on a nomenclator without a key
  * the adjacency hypothesis - contemporary Royalist nomenclators (e.g. Bramhall to Ormond, 1653)
    assign runs of consecutive numbers to one letter. If these letters do too, codes differing by
    1 or 2 should be interchangeable in repeated contexts.
  * whether the two unread letters use the same cipher as each other

Usage: python structure.py
"""
import collections, itertools, math

import letters as L
import key as K


def hapax(seq):
    c = collections.Counter(seq)
    return sum(1 for v in c.values() if v == 1), len(c), len(seq)


def ic(seq):
    c = collections.Counter(seq)
    n = len(seq)
    return sum(v * (v - 1) for v in c.values()) / (n * (n - 1)) if n > 1 else 0.0


def ngrams(seq, k):
    return collections.Counter(tuple(seq[i:i + k]) for i in range(len(seq) - k + 1))


def repeats(seq, k):
    return {g: v for g, v in ngrams(seq, k).items() if v > 1}


def near_repeats(seq, k, tol=1):
    """Pairs of k-grams that match except at positions where the codes differ by <= tol.

    Under an adjacency design (consecutive numbers = homophones of one letter) a repeated phrase
    will show up as a near-repeat rather than an exact one.
    """
    out = []
    for i in range(len(seq) - k + 1):
        for j in range(i + k, len(seq) - k + 1):
            a, b = seq[i:i + k], seq[j:j + k]
            d = [abs(x - y) for x, y in zip(a, b)]
            if all(x <= tol for x in d) and any(d):
                out.append((i, j, a, b))
    return out


def section(title):
    print('\n' + '=' * 96)
    print(title)
    print('=' * 96)


def main():
    section('1. INVENTORY   how much of each message repeats at all')
    print('%-34s %6s %8s %8s %8s %8s' % ('letter', 'codes', 'distinct', 'hapax', 'hapax%', 'IC'))
    for let in L.ALL:
        s = L.codes(let)
        h, d, n = hapax(s)
        print('%-34s %6d %8d %8d %7.0f%% %8.4f  %s'
              % (L.name(let)[:34], n, d, h, 100.0 * h / n, ic(s), let['status'][:18]))
    print("""
   A nomenclator message is readable only through the codes that recur. Where the hapax rate is
   this high, most of the plaintext has no statistical shadow at all.""")

    section('2. TWO-PART PROFILE   which code values carry the repeats')
    for let in L.UNREAD:
        s = L.codes(let)
        c = collections.Counter(s)
        print('\n%s   (%d codes, max %d)' % (L.name(let), len(s), max(s)))
        band = collections.Counter()
        for v, n in c.items():
            band[(v // 50) * 50] += n
        print('   band   codes  distinct   mean uses')
        for b in sorted(band):
            vals = [v for v in c if (v // 50) * 50 == b]
            print('   %3d-%3d %6d %9d %10.2f' % (b, b + 49, band[b], len(vals),
                                                 band[b] / len(vals)))
        top = [(v, n) for v, n in c.most_common() if n > 1]
        print('   repeated codes: %s' % (', '.join('%d x%d' % (v, n) for v, n in top) or 'none'))

    section('3. REPEATED n-GRAMS   the only handle on a nomenclator without its key')
    for let in L.ALL:
        s = L.codes(let)
        print('\n%s' % L.name(let))
        found = False
        for k in (2, 3, 4, 5, 6, 7):
            r = repeats(s, k)
            if r:
                found = True
                for g, v in sorted(r.items(), key=lambda x: -len(x[0])):
                    print('   %d-gram x%d: %s' % (k, v, ' '.join(map(str, g))))
        if not found:
            print('   none')

    section('4. ADJACENCY HYPOTHESIS   are consecutive numbers homophones of one letter?')
    print("""   Contemporary Royalist practice (Bramhall to Ormond 1653) gives each letter a run of
   three consecutive numbers. If either unread letter is built that way, repeated phrases will
   appear as near-repeats whose mismatches are all small.""")
    for let in L.UNREAD:
        s = L.codes(let)
        print('\n%s' % L.name(let))
        for k in (4, 5, 6, 7):
            nr = near_repeats(s, k, tol=2)
            for i, j, a, b in nr:
                d = [x - y for x, y in zip(a, b)]
                print('   %d-gram at %d and %d:  %s  /  %s   diffs %s'
                      % (k, i, j, ' '.join(map(str, a)), ' '.join(map(str, b)), d))

    section('5. ARE THE TWO UNREAD LETTERS IN THE SAME CIPHER AS EACH OTHER?')
    a = set(L.codes(L.MAY22))
    b = set(L.codes(L.AUG1))
    print('   22 May distinct codes : %d   (max %d)' % (len(a), max(a)))
    print('   1 Aug distinct codes  : %d   (max %d)' % (len(b), max(b)))
    print('   shared                : %d   %s' % (len(a & b), sorted(a & b)))
    exp = len(a) * len(b) / 615.0
    print('   expected shared if both drew uniformly from 1-615: %.1f' % exp)
    print("""
   The 1 August letter's own postscript settles the historical question: "This Cypher which now I
   write in, is that which was sent you by the noble frend who conveis this Letter to you from me."
   Charles is telling his son he has switched to a newly delivered cipher.""")

    section('6. HOW MUCH PLAINTEXT IS AT STAKE')
    for let in L.UNREAD:
        s = L.codes(let)
        lo = sum(1 for n in s if n <= 107)
        hi = len(s) - lo
        print('   %-34s about %d letters + %d word codes  ~= %d characters of English'
              % (L.name(let)[:34], lo, hi, lo + int(hi * 4.5)))


if __name__ == '__main__':
    main()
