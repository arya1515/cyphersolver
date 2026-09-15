"""Is the Vatican Part 5 cipher identifiable *in principle* at this level of polyphony?

The constrained search (vc.py) still does not converge: 24 runs give 24 keys, mean Rand index against
the best 0.861 where chance in the same constrained space is 0.799. Two explanations:

  (a) the model is wrong - the text is not a polyphonic single-digit substitution, so no key fits; or
  (b) the model is right but the problem is not identifiable - 16 consonants sharing 5 digits is about
      3.2 letters per symbol, and at that ambiguity many keys explain the statistics equally well.

These have opposite consequences, so it is worth separating them. Build a synthetic ciphertext with
*exactly* the structure we believe the real one has - same alphabet, same vowel/consonant digit split,
same polyphony, same null rate, same length, real Italian plaintext - and run the identical search on it.

If the synthetic converges and the real text does not, the model is wrong (a).
If the synthetic also fails to converge, then no statistical attack can recover this key (b), and the
cipher needs the key itself.
"""
import collections, itertools, math, random, re, sys

import numpy as np

import vc

AL = vc.AL
VOWELS = vc.VOWELS
VD, CD = vc.VOWEL_DIGITS, vc.CONS_DIGITS


def make_key(rnd):
    """A key with the same shape as the real one is believed to have."""
    key = {}
    vs = list('aeiou')
    rnd.shuffle(vs)
    # 5 vowels over 4 digits: one digit takes two
    for i, c in enumerate(vs[:4]):
        key[c] = VD[i]
    key[vs[4]] = rnd.choice(VD)
    cs = [c for c in AL if c not in VOWELS]
    rnd.shuffle(cs)
    for i, c in enumerate(cs):
        key[c] = CD[i % len(CD)]
    return key


def make_cipher(key, rnd, n_digits=6553, null_rate=0.44):
    txt = open('corpus_it.txt', encoding='utf-8', errors='ignore').read().lower()
    txt = re.sub(r'[^a-z ]+', ' ', txt)
    txt = re.sub('[jkwxy]', '', txt)
    txt = re.sub(' +', ' ', txt)
    start = rnd.randrange(0, len(txt) - n_digits * 2)
    seq = []
    for ch in txt[start:]:
        if len(seq) >= n_digits:
            break
        if ch == ' ':
            if rnd.random() < null_rate:
                seq.append(vc.NULL)
            continue
        if ch in key:
            seq.append(key[ch])
    return seq


def counts_from(seq):
    C = np.zeros((10, 10, 10))
    for a, b, c in zip(seq, seq[1:], seq[2:]):
        C[a, b, c] += 1
    return C


def show(assign):
    g = {d: '' for d in VD + CD}
    for l in sorted(assign, key=lambda x: AL[x]):
        g[assign[l]] += AL[l]
    return ' '.join('%d=%s' % (d, g[d] or '-') for d in VD + CD)


def rand_index(a, b):
    same = tot = 0
    for x, y in itertools.combinations(range(len(AL)), 2):
        tot += 1
        same += (a[x] == a[y]) == (b[x] == b[y])
    return same / tot


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    iters = int(sys.argv[2]) if len(sys.argv) > 2 else 120000
    rnd = random.Random(seed)
    key = make_key(rnd)
    seq = make_cipher(key, rnd)
    truth = {vc.LI[c]: d for c, d in key.items()}
    print('synthetic: %d digits, null rate %.2f' % (len(seq), seq.count(vc.NULL) / len(seq)))
    print('TRUE KEY : %s' % show(truth))

    vc.C = counts_from(seq)
    vc.MASK = vc.C > 0
    print('true key LL: %.1f' % vc.ll(truth))

    results = []
    for trial in range(4):
        r = random.Random(seed * 1000 + trial)
        v, a = vc.sa(r, iters)
        ri = rand_index([a[i] for i in range(len(AL))], [truth[i] for i in range(len(AL))])
        results.append((v, a, ri))
        print('  trial %d: %.1f  rand_vs_truth %.2f  %s' % (trial, v, ri, show(a)), flush=True)
    best = max(results, key=lambda x: x[0])
    inter = [rand_index([best[1][i] for i in range(len(AL))], [a[i] for i in range(len(AL))])
             for _, a, _ in results]
    print('\nrecovery of the true key (best run): %.2f' % best[2])
    print('agreement between runs: %.2f' % (sum(inter) / len(inter)))
    print('real ciphertext, for comparison: agreement 0.86, chance 0.80')


if __name__ == '__main__':
    main()
