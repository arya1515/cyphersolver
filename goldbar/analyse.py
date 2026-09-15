"""Chinese gold bar cryptograms (IACR 1996): test whether they can be enciphered text.

Result: the 263 letters contain almost exactly ten of every letter of the alphabet. The
chi-squared statistic against a uniform distribution is 1.25 on 25 degrees of freedom, where
random sampling predicts 25. That is about a one-in-a-trillion level of over-uniformity, and it
excludes every encryption of natural language: substitution and transposition keep the plaintext
skew, a short-key Vigenere only partly flattens it, and even a one-time pad lands at chi-squared
near 25 because it is still random sampling. The strings were constructed, not enciphered.
"""
import collections, random
from corpus import CRYPTOGRAMS, ALL
AL = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def main():
    n = len(ALL)
    c = collections.Counter(ALL)
    counts = [c[ch] for ch in AL]
    exp = n / 26
    chi = sum((v - exp) ** 2 / exp for v in counts)
    ic = sum(v * (v - 1) for v in counts) / (n * (n - 1))
    print('%d cryptograms, %d letters' % (len(CRYPTOGRAMS), n))
    print('counts:', ' '.join('%s%d' % (ch, v) for ch, v in zip(AL, counts)))
    print('exactly ten: %d of 26; deviations %s'
          % (sum(1 for v in counts if v == 10),
             {ch: v - 10 for ch, v in zip(AL, counts) if v != 10}))
    print('IC = %.4f   chi2 vs uniform = %.3f on 25 df' % (ic, chi))
    try:
        from scipy import stats
        print('P(chi2_25 <= %.3f) = %.3e' % (chi, stats.chi2.cdf(chi, 25)))
    except ImportError:
        pass
    rnd = random.Random(12345)
    M, hits = 200000, 0
    for _ in range(M):
        cc = collections.Counter(rnd.choices(AL, k=n))
        if sum((cc[ch] - exp) ** 2 / exp for ch in AL) <= chi:
            hits += 1
    print('random 263-letter strings at least this uniform: %d of %d' % (hits, M))

if __name__ == '__main__':
    main()
