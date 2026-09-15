"""Vatican Challenge Part 5 - constrained polyphonic search.

Earlier free searches over all assignments of 21 letters to 9 digits never converged: 24 runs gave 24
different keys within 500 nats of each other (Rand index vs best about 0.85, i.e. chance). The model
class was too loose.

Two structural facts constrain it hard, and both come from the data rather than from a guessed key.

  * digit 4 is a null / word separator. Conditioning on 4 in the middle drops the mutual information
    between its neighbours to 0.030, matching Italian across a word boundary (0.028), where every other
    digit sits at 0.08-0.17.
  * Italian words end in a vowel about 97% of the time. Word-final enrichment (final rate / overall rate)
    splits the nine remaining digits cleanly:

        1: 1.79   7: 1.76   3: 1.52   0: 1.49  |  6: 1.01  |  9: 0.64  2: 0.58  5: 0.25  8: 0.08

    and the frequency masses agree with Italian to three decimals:
        vowel digits {7,0,3,1} = 0.476   against  a+e+i+o+u = 0.479
        consonant digits {8,5,2,6,9} = 0.524  against  all consonants = 0.521

So: vowels may only be assigned to {7,0,3,1} and consonants only to {8,5,2,6,9}. That cuts the space from
9^21 to 4^5 x 5^16 and, more importantly, removes the vowel/consonant confusions that let wrong keys score
as well as right ones.

Objective: exact multinomial log-likelihood of the observed digit trigram counts under the grouped Italian
letter-trigram distribution, with 4 as the boundary symbol. Identical to trigramfit.py apart from the
constraint, so the two are directly comparable.

Usage:  python vc.py [seed] [iters]
"""
import collections, json, math, random, sys

import numpy as np

from parse5 import load, digit_stream

AL = 'abcdefghilmnopqrstuvz'          # 21-letter Italian alphabet
VOWELS = set('aeiou')
LI = {c: i for i, c in enumerate(AL)}
B = len(AL)                           # boundary index
N = B + 1

VOWEL_DIGITS = [7, 0, 3, 1]
CONS_DIGITS = [8, 5, 2, 6, 9]
DIGITS = VOWEL_DIGITS + CONS_DIGITS
NULL = 4


def build_lm():
    ng = json.load(open('it_ngrams.json', encoding='utf-8'))
    P3 = np.full((N, N, N), 1e-9)
    for k, v in ng['3'].items():
        idx = [LI.get(ch, B if ch == ' ' else None) for ch in k]
        if None in idx:
            continue
        P3[idx[0], idx[1], idx[2]] += v
    return P3 / P3.sum()


def build_counts():
    runs = digit_stream(load())
    seq = []
    for r in runs:
        for i, t in enumerate(r):
            d = t[0]
            bad = ('^' in t or '_' in t or '?' in t) or (i > 0 and ('^' in r[i - 1] or '_' in r[i - 1]))
            seq.append(None if bad else int(d))
        seq.append(NULL)
    C = np.zeros((10, 10, 10))
    for a, b, c in zip(seq, seq[1:], seq[2:]):
        if None in (a, b, c):
            continue
        C[a, b, c] += 1
    return C


P3 = build_lm()
C = build_counts()
MASK = C > 0


def ll(assign):
    G = np.zeros((10, N))
    G[NULL, B] = 1.0
    for l, d in assign.items():
        G[d, l] = 1.0
    Q = np.tensordot(P3, G.T, axes=([2], [0]))
    Q = np.tensordot(Q, G.T, axes=([1], [0]))
    Q = np.tensordot(G, Q, axes=([1], [0]))
    Q = np.transpose(Q, (0, 2, 1))
    Q = Q / Q.sum()
    return float((C[MASK] * np.log(Q[MASK] + 1e-12)).sum())


def show(assign):
    g = {d: '' for d in DIGITS}
    for l in sorted(assign, key=lambda x: AL[x]):
        g[assign[l]] += AL[l]
    return ' '.join('%d=%s' % (d, g[d] or '-') for d in DIGITS)


def sa(rnd, iters):
    assign = {}
    for i, c in enumerate(AL):
        assign[i] = rnd.choice(VOWEL_DIGITS if c in VOWELS else CONS_DIGITS)
    cur = ll(assign)
    best = (cur, dict(assign))
    T = 25.0
    for it in range(iters):
        l = rnd.randrange(B)
        pool = VOWEL_DIGITS if AL[l] in VOWELS else CONS_DIGITS
        old = assign[l]
        new = rnd.choice(pool)
        if new == old:
            continue
        assign[l] = new
        if not any(v == old for v in assign.values()):
            assign[l] = old
            continue
        v = ll(assign)
        if v > cur or rnd.random() < math.exp((v - cur) / max(T, 1e-9)):
            cur = v
        else:
            assign[l] = old
        if cur > best[0]:
            best = (cur, dict(assign))
        T = max(0.2, T * 0.99994)
    return best


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    iters = int(sys.argv[2]) if len(sys.argv) > 2 else 120000
    for trial in range(4):
        rnd = random.Random(seed * 100 + trial)
        v, a = sa(rnd, iters)
        print('seed %d trial %d: %.1f  %s' % (seed, trial, v, show(a)), flush=True)


if __name__ == '__main__':
    main()
