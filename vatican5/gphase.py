"""Is there a GLOBAL two-digit phase in IA-2, rather than one that restarts at each null?

Every phase test run here so far reset the grid at each null, on the assumption that 4 separates
words. The chancery's own instruction, printed by Meister at p.223, says otherwise: names are
abbreviated "con il segno della nulla in fine della lettera o sillaba" - the null closes a letter or a
syllable carrying an abbreviation. If that is what 4 does, it is one more symbol in the stream, not a
reset, and taking phase 0 from each null was measuring nothing.

So test the grid globally. Three ways, each with the null treated differently, because if 4 occupies a
slot the parity carries through it and if it does not the parity flips at every null:

    A  null counted as a symbol   - phase = absolute index
    B  null deleted               - phase = index among non-null digits
    C  null deleted and phase recomputed per cleartext-delimited run

For each, compare the digit distribution at even against odd offsets, calibrated by shuffling. A real
two-digit code laid on a fixed grid shows a large separation; anything else does not.

If one of these comes out strongly, the text can be cut into units and attacked as a substitution over
roughly a hundred symbols with about three thousand tokens - which is tractable. That is the whole
point of the test.

Usage: python gphase.py
"""
import collections, math, random, re

import escape as E


def chi2(a, b):
    keys = set(a) | set(b)
    na, nb = sum(a.values()), sum(b.values())
    tot = 0.0
    for k in keys:
        e = (a.get(k, 0) + b.get(k, 0))
        ea, eb = e * na / (na + nb), e * nb / (na + nb)
        if ea > 0:
            tot += (a.get(k, 0) - ea) ** 2 / ea
        if eb > 0:
            tot += (b.get(k, 0) - eb) ** 2 / eb
    return tot


def split(seq):
    A = collections.Counter(seq[0::2])
    B = collections.Counter(seq[1::2])
    return A, B


def test(name, seq, trials=3000, seed=4):
    A, B = split(seq)
    obs = chi2(A, B)
    rnd = random.Random(seed)
    pool = list(seq)
    vals = []
    for _ in range(trials):
        rnd.shuffle(pool)
        a, b = split(pool)
        vals.append(chi2(a, b))
    mu = sum(vals) / len(vals)
    sd = (sum((x - mu) ** 2 for x in vals) / len(vals)) ** 0.5
    beat = sum(1 for x in vals if x >= obs)
    print('\n%-44s n=%d' % (name, len(seq)))
    print('   chi2 even vs odd = %7.1f   null mean %5.1f sd %4.1f   z = %+6.2f   p = %.4f'
          % (obs, mu, sd, (obs - mu) / sd if sd else 0, beat / trials))
    pa = {k: v / sum(A.values()) for k, v in A.items()}
    pb = {k: v / sum(B.values()) for k, v in B.items()}
    rows = sorted(set(pa) | set(pb), key=lambda d: -(pa.get(d, 0) / pb[d] if pb.get(d) else 9))
    print('   digit  even    odd     ratio')
    for d in rows:
        r = pa.get(d, 0) / pb[d] if pb.get(d) else float('inf')
        print('     %s    %.4f  %.4f  %.2f' % (d, pa.get(d, 0), pb.get(d, 0), r))
    return obs, (obs - mu) / sd if sd else 0


def main():
    seq = E.load()
    runs = E.runs(seq)
    full = [d for r in runs for d in r]

    print('6549 digits; null 4 occurs %d times' % full.count('4'))

    # A: null occupies a slot, absolute index
    test('A  null counted, absolute index', full)

    # B: null deleted
    nonull = [d for d in full if d != '4']
    test('B  null deleted, global index', nonull)

    # C: null deleted, phase restarts at each cleartext break only
    seqs = []
    for r in runs:
        seqs.append([d for d in r if d != '4'])
    C = []
    for r in seqs:
        C.extend(r)
    test('C  null deleted, per cleartext run', C)

    # D: for comparison, the old test - phase restarts at every null
    D = []
    for r in runs:
        for part in ''.join(r).split('4'):
            D.extend(part)
    # rebuild with per-segment parity by interleaving
    Aa, Bb = collections.Counter(), collections.Counter()
    for r in runs:
        for part in ''.join(r).split('4'):
            for i, d in enumerate(part):
                (Aa if i % 2 == 0 else Bb).update([d])
    print('\n%-44s' % 'D  phase restarts at every null (the old test)')
    print('   chi2 even vs odd = %7.1f' % chi2(Aa, Bb))

    print("""
=== READING
If a global grid existed, one of A, B or C would separate sharply and the others would not. If all
three sit near their shuffle nulls, there is no fixed two-digit grid anywhere in the text, and the
units are genuinely variable-length - which is what Elio's compound symbols predict, and what makes
the cipher unbreakable from ciphertext alone.""")


if __name__ == '__main__':
    main()
