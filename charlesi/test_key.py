"""Does the published Biermann/Bosbach/Brown nomenclator open the two unread letters?

The cheap decisive test. Three measurements, each on all four letters, two of which are solved and
act as positive controls:

  1. coverage - what fraction of code groups the key can interpret at all. A nomenclator applied to
     its own traffic should leave almost nothing unexplained.
  2. range    - do the codes respect the key's two-part layout (letters 1-107, words 142-615)? A
     different nomenclator will put codes in the gap or above the top.
  3. language - take the maximal runs of single-letter codes, map them through the key, and score
     them with an English bigram model. Compare against a null in which the 24 letter identities
     are randomly permuted across the homophone classes. That null preserves everything about the
     key's structure (which codes are homophones of which) and destroys only the identity, so it
     isolates exactly the claim being tested.

Usage: python test_key.py
"""
import collections, glob, math, os, random, re, sys

import key as K
import letters as L

CORPUS = os.path.join('..', 'beale', 'lmcorpus')
ALPHA = 'abcdefghiklmnopqrstuwxyz'      # period alphabet: no j, no v


# ---------------------------------------------------------------- language model

def build_bigrams(max_files=25):
    """Bigram counts over the 24-letter period alphabet (j->i, v->u), from the local corpus."""
    cnt = collections.Counter()
    uni = collections.Counter()
    files = sorted(glob.glob(os.path.join(CORPUS, '*.txt')))[:max_files]
    for f in files:
        txt = open(f, encoding='utf-8', errors='ignore').read().lower()
        txt = txt.replace('j', 'i').replace('v', 'u')
        txt = re.sub('[^a-z]', '', txt)
        for a, b in zip(txt, txt[1:]):
            cnt[a + b] += 1
        uni.update(txt)
    return cnt, uni, len(files)


class LM:
    def __init__(self):
        self.big, self.uni, self.nfiles = build_bigrams()
        self.tot = sum(self.uni.values())
        self.rowtot = collections.Counter()
        for k, v in self.big.items():
            self.rowtot[k[0]] += v

    def score(self, s):
        """Mean log-probability per character of a fragment, with add-0.5 smoothing."""
        if len(s) < 2:
            return None
        tot = 0.0
        for a, b in zip(s, s[1:]):
            tot += math.log((self.big[a + b] + 0.5) / (self.rowtot[a] + 0.5 * len(ALPHA)))
        return tot / (len(s) - 1)


# ---------------------------------------------------------------- runs of letter codes

def letter_runs(seq, minlen=3):
    """Maximal runs of codes that the key reads as single letters (nulls pass through).

    Word codes break a run, because the spelled-out fragments on either side of a word are not
    continuous English.
    """
    runs, cur = [], []
    for n in seq:
        if n in K.NULLS:
            continue
        if n in K.LETTERS:
            cur.append(n)
        else:
            if len(cur) >= minlen:
                runs.append(cur)
            cur = []
    if len(cur) >= minlen:
        runs.append(cur)
    return runs


def score_runs(runs, mapping, lm):
    """Length-weighted mean bigram score over all runs under a code->letter mapping."""
    num = den = 0.0
    for r in runs:
        s = ''.join(mapping[n] for n in r)
        v = lm.score(s)
        if v is not None:
            num += v * (len(s) - 1)
            den += len(s) - 1
    return num / den if den else None


def permuted_mapping(rnd):
    """Same homophone structure, randomly relabelled letters."""
    perm = list(ALPHA)
    rnd.shuffle(perm)
    sub = dict(zip(ALPHA, perm))
    return {n: sub[c] for n, c in K.LETTERS.items()}


# ---------------------------------------------------------------- report

def coverage(seq):
    kinds = collections.Counter(K.decode_token(n)[1] for n in seq)
    return kinds


def range_profile(seq):
    lo = [n for n in seq if n <= K.LETTER_MAX]
    gap = [n for n in seq if K.LETTER_MAX < n < K.WORD_MIN]
    hi = [n for n in seq if n >= K.WORD_MIN]
    return lo, gap, hi


def main():
    lm = LM()
    print('bigram model: %d books, %s characters\n' % (lm.nfiles, format(lm.tot, ',')))

    trials = 4000
    rows = []
    for let in L.ALL:
        seq = L.codes(let)
        kinds = coverage(seq)
        lo, gap, hi = range_profile(seq)
        runs = letter_runs(seq)
        nrun = sum(len(r) for r in runs)
        real = score_runs(runs, K.LETTERS, lm)

        rnd = random.Random(12345)
        null = []
        for _ in range(trials):
            v = score_runs(runs, permuted_mapping(rnd), lm)
            if v is not None:
                null.append(v)
        if real is not None and null:
            mu = sum(null) / len(null)
            sd = (sum((x - mu) ** 2 for x in null) / len(null)) ** 0.5
            z = (real - mu) / sd if sd else 0.0
            better = sum(1 for x in null if x >= real)
            pct = 100.0 * better / len(null)
        else:
            mu = sd = z = pct = float('nan')

        rows.append((let, seq, kinds, lo, gap, hi, runs, nrun, real, mu, sd, z, pct))

    print('=' * 100)
    print('1. COVERAGE  (what fraction of code groups the published key can interpret)')
    print('=' * 100)
    print('%-34s %6s %8s %7s %7s %9s' % ('letter', 'codes', 'letters', 'words', 'nulls', 'UNKNOWN'))
    for let, seq, kinds, *_ in rows:
        unk = kinds['unknown']
        print('%-34s %6d %8d %7d %7d %6d %3.0f%%  %s'
              % (L.name(let)[:34], len(seq), kinds['letter'], kinds['word'], kinds['null'],
                 unk, 100.0 * unk / len(seq), let['status'][:20]))

    print()
    print('=' * 100)
    print('2. RANGE  (the key is letters 1-107, a dead gap 108-141, words 142-615)')
    print('=' * 100)
    print('%-34s %10s %10s %10s %7s' % ('letter', '1-107', 'GAP 108-141', '142-615', 'max'))
    for let, seq, kinds, lo, gap, hi, *_ in rows:
        over = [n for n in hi if n > 615]
        print('%-34s %10d %10d %10d %7d %s'
              % (L.name(let)[:34], len(lo), len(gap), len(hi) - len(over), max(seq),
                 ('  %d above 615: %s' % (len(over), sorted(set(over)))) if over else ''))
    ingap = {}
    for let, seq, kinds, lo, gap, hi, *_ in rows:
        if gap:
            ingap[L.name(let)] = sorted(set(gap))
    for n, g in ingap.items():
        print('   codes in the dead gap, %s: %s' % (n, g))

    print()
    print('=' * 100)
    print('3. LANGUAGE  (runs of single-letter codes, scored as English; null = letters relabelled)')
    print('=' * 100)
    print('%-34s %5s %6s %8s %8s %7s %8s' %
          ('letter', 'runs', 'chars', 'score', 'null mu', 'z', 'p'))
    for let, seq, kinds, lo, gap, hi, runs, nrun, real, mu, sd, z, pct in rows:
        if real is None:
            print('%-34s %5d %6d   (too little letter text to score)' % (L.name(let)[:34], len(runs), nrun))
            continue
        print('%-34s %5d %6d %8.3f %8.3f %+7.2f %7.3f' %
              (L.name(let)[:34], len(runs), nrun, real, mu, z, pct / 100.0))

    print()
    print('=' * 100)
    print('DECODES')
    print('=' * 100)
    for let in L.ALL:
        print('\n--- %s   [%s]' % (L.name(let), let['status']))
        for clear, cs in let['chunks']:
            if clear:
                print('   %s' % re.sub(r'\s+', ' ', clear).strip())
            if cs:
                txt, _ = K.decode(cs)
                print('   >>> %s' % txt)


if __name__ == '__main__':
    main()
