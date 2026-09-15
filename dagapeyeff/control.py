"""Positive control for the D'Agapeyeff challenge cipher.

D'Agapeyeff's own book contains a worked Polybius example whose plaintext he gives: 178 letters of
A-E, i.e. 89 cells, enciphering "THE NEW PLAN OF ATTACK ...". That is a known-good Polybius
ciphertext of English, by the same author, in the same book. So we can run the same tests on the
control and on the challenge and see whether the challenge behaves like an encipherment of English.

Two tests, both invariant to the substitution key:
  1. sorted cell frequencies against English letter frequencies (chi-squared)
  2. repeated digrams, against English of the same length and against random shuffles
"""
import collections, math, random, re, sys

from ct import DIGITS

CONTROL = """CDDBC ECBCE BBEBD ABCCB BDBAB CCDCD BCDDE CAECB DDDAA CABCE
AABDE BCEDC BCCDA EBDCB AAEAB ECDDB DCCEC EEABD ADEAD CAADE
ACABD CBDCB AABDC ACEDC BABCD DCDBD DCBEB CDCBE BCAAB DACCD
DBBBC EAACD BDCDD BCEDC AECAC EDC"""

ENG = {'e':12.7,'t':9.06,'a':8.17,'o':7.51,'i':6.97,'n':6.75,'s':6.33,'h':6.09,'r':5.99,
       'd':4.25,'l':4.03,'c':2.78,'u':2.76,'m':2.41,'w':2.36,'f':2.23,'g':2.02,'y':1.97,
       'p':1.93,'b':1.29,'v':0.98,'k':0.77,'j':0.15,'x':0.15,'q':0.10,'z':0.07}


def cells(s, alphabet=None):
    s = ''.join(s.split())
    return [s[i:i + 2] for i in range(0, len(s) - len(s) % 2, 2)]


def freq_chi2_vs_english(counts, ncells=25):
    """Best-case chi-squared: sort observed against sorted English expectations."""
    n = sum(counts)
    obs = sorted(counts, reverse=True)
    obs += [0] * (ncells - len(obs))
    ev = sorted(ENG.values(), reverse=True)[:ncells]
    tot = sum(ev)
    exp = [n * v / tot for v in ev]
    return sum((o - e) ** 2 / e for o, e in zip(obs, exp))


def digram_repeats(seq):
    dg = collections.Counter(zip(seq, seq[1:]))
    return sum(v - 1 for v in dg.values() if v > 1)


def shuffle_null(seq, trials=4000, seed=3):
    rnd = random.Random(seed)
    vals = []
    for _ in range(trials):
        s = seq[:]
        rnd.shuffle(s)
        vals.append(digram_repeats(s))
    m = sum(vals) / len(vals)
    sd = (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5
    return m, sd


def english_null(n, trials=2000, seed=5):
    txt = open('../beale/lmcorpus/pg1342.txt', encoding='utf-8', errors='ignore').read().lower()
    txt = re.sub('[^a-z]', '', txt)
    rnd = random.Random(seed)
    vals = [digram_repeats(list(txt[(i := rnd.randrange(0, len(txt) - n)):i + n])) for _ in range(trials)]
    m = sum(vals) / len(vals)
    sd = (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5
    return m, sd


def report(name, seq, ncells):
    c = collections.Counter(seq)
    n = len(seq)
    ic = sum(v * (v - 1) for v in c.values()) / (n * (n - 1))
    chi = freq_chi2_vs_english(list(c.values()), ncells)
    obs = digram_repeats(seq)
    sm, ssd = shuffle_null(seq)
    em, esd = english_null(n)
    print('\n=== %s' % name)
    print('  %d cells, %d distinct, IC %.4f' % (n, len(c), ic))
    print('  sorted counts: %s' % sorted(c.values(), reverse=True))
    print('  chi2 vs English frequency profile (best case) = %.1f on %d df' % (chi, ncells - 1))
    print('  repeated digrams: observed %d' % obs)
    print('     random shuffle of same symbols: %.1f +/- %.1f  -> z = %+.2f' % (sm, ssd, (obs - sm) / ssd))
    print('     English of same length:         %.1f +/- %.1f  -> z = %+.2f' % (em, esd, (obs - em) / esd))


def main():
    ctrl = cells(CONTROL)
    chal = cells(DIGITS[:392])
    report("CONTROL: D'Agapeyeff's own worked Polybius example (known plaintext)", ctrl, 25)
    report('CHALLENGE: the 1939 challenge cipher, 196 cells', chal, 25)


if __name__ == '__main__':
    main()
