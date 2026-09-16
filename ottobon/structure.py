"""Structural tests to run on ct.txt before any solving (Ottobon to Mocenigo, 1589).

1. Frequency profile per base letter and per figure; IC of the token stream.
2. Vowel-slot test: in the Zifra Granda (ASVe b.4 r.16, 1578-87) syllables ending -a -e -i -o -u carry figures
   ending 1 2 3 4 5 (Bonavoglia 2019 Fig. 2). If the letter uses that table or one built on the same plan,
   the last digit of the figures is confined to 1-5 for the syllable part and the digit histogram mod 5 (or
   mod 10) is far from flat. Same test as segur/ (memory: syllabary mod-5 test), applied per base letter.
3. Key-reuse test: read the text through refs/zifra_granda_syllabary.json and score the fraction of tokens
   that hit a syllable, then the 5-gram Italian score of the syllable string (lucca/it5.npy) against the
   same string under a random relabelling of the figures. A hit rate near 1 with a score well above the
   shuffles means the table is the key or is close to it.
4. Repeats: repeated 3- and 4-token sequences against a shuffle, as in vatican5/ (a nomenclator-heavy text
   repeats long formulae; a letter-by-letter text does not).

Usage: python structure.py ct.txt
"""
import sys, json, collections, random, os, math
import numpy as np
from parse import parse, cipher_only

HERE = os.path.dirname(os.path.abspath(__file__))

def ic(seq):
    c = collections.Counter(seq); n = len(seq)
    return sum(v * (v - 1) for v in c.values()) / (n * (n - 1)) if n > 1 else 0.0

def load_lm():
    p = os.path.join(HERE, '..', 'lucca', 'it5.npy')
    return np.load(p) if os.path.exists(p) else None

def score5(lp, s):
    A = 'abcdefghijklmnopqrstuvwxyz'
    idx = [A.index(ch) for ch in s if ch in A]
    if len(idx) < 5 or lp is None:
        return float('nan')
    p = np.array(idx)
    q = p[:-4] * 456976 + p[1:-3] * 17576 + p[2:-2] * 676 + p[3:-1] * 26 + p[4:]
    return float(lp[q].sum()) / len(q)

def main(fn):
    toks = cipher_only(parse(open(fn, encoding='utf-8').read()))
    raws = [t[2] for t in toks]
    print('tokens %d, distinct %d, IC %.4f' % (len(raws), len(set(raws)), ic(raws)))

    # 1. profiles
    by_base = collections.defaultdict(collections.Counter)
    for b, f, r in toks:
        by_base[b][f] += 1
    for b in sorted(by_base, key=lambda x: -sum(by_base[x].values())):
        c = by_base[b]
        figs = sorted(k for k in c if k is not None)
        print('base %-2s n=%4d distinct=%3d range=%s' % (b or '-', sum(c.values()), len(c),
              ('%d-%d' % (figs[0], figs[-1])) if figs else '-'))

    # 2. vowel-slot test, per base letter and overall
    print('\nlast-digit histogram (mod 10) and mod 5, overall and per base letter')
    def hist(fs, m):
        h = [0] * m
        for f in fs:
            h[f % m] += 1
        return h
    def chi(h):
        n = sum(h); e = n / len(h)
        return sum((x - e) ** 2 / e for x in h) if e > 0 else 0.0
    allf = [f for b, f, r in toks if f is not None]
    print('all    mod10 %s chi2=%.1f | mod5 %s chi2=%.1f' % (hist(allf, 10), chi(hist(allf, 10)), hist(allf, 5), chi(hist(allf, 5))))
    for b in sorted(by_base):
        fs = [f for f in by_base[b].elements() if f is not None]
        if len(fs) >= 20:
            print('%-6s mod10 %s chi2=%.1f | mod5 %s chi2=%.1f' % (b or '-', hist(fs, 10), chi(hist(fs, 10)), hist(fs, 5), chi(hist(fs, 5))))
    print('(mod-5 chi2 with 4 d.f.: 9.5 is p=0.05, 18.5 is p=0.001; a syllabary on the Zifra Granda plan gives hundreds)')

    # 3. key-reuse test against the Zifra Granda syllabary
    tab = json.load(open(os.path.join(HERE, 'refs', 'zifra_granda_syllabary.json'), encoding='utf-8'))['syllables']
    def norm(r):
        return r.replace('_', '')
    hits = [tab.get(norm(r)) for r in raws]
    nh = sum(1 for h in hits if h)
    print('\nZifra Granda syllabary: %d of %d tokens are table entries (%.1f%%)' % (nh, len(raws), 100.0 * nh / max(1, len(raws))))
    lp = load_lm()
    s = ''.join(h for h in hits if h)
    if lp is not None and len(s) > 20:
        real = score5(lp, s)
        keys = list(tab.keys()); vals = list(tab.values())
        rnd = random.Random(1); ctrl = []
        for _ in range(20):
            rnd.shuffle(vals)
            t2 = dict(zip(keys, vals))
            s2 = ''.join(t2[norm(r)] for r in raws if norm(r) in t2)
            ctrl.append(score5(lp, s2))
        print('5-gram per position: table as printed %.3f; figures relabelled at random %.3f +- %.3f' % (real, np.mean(ctrl), np.std(ctrl)))
        print('syllable string head:', s[:200])

    # 4. repeats
    def rep(seq, k):
        c = collections.Counter(tuple(seq[i:i + k]) for i in range(len(seq) - k + 1))
        return sum(v - 1 for v in c.values() if v > 1)
    rnd = random.Random(2); sh = raws[:]; rnd.shuffle(sh)
    print('\nrepeated 3-grams %d (shuffle %d), 4-grams %d (shuffle %d)' % (rep(raws, 3), rep(sh, 3), rep(raws, 4), rep(sh, 4)))

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else 'ct.txt')
