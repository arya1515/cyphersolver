"""Periodic polyalphabetic test: Vigenere, Beaufort and variant Beaufort, periods 1-26, German/English/Dutch.

For each message, period and variant: coordinate ascent on the per-column shifts under a quadgram model, with
restarts. Calibrated two ways: the score of real language of the same length (the target), and the best score
the same search reaches on a shuffle of the ciphertext (the noise floor at that period).
"""
import random, sys
from msgs import CT
from lm import Q

A = 'abcdefghijklmnopqrstuvwxyz'


def dec(ct, key, variant):
    out = []
    for i, c in enumerate(ct):
        k = key[i % len(key)]; x = ord(c) - 97
        if variant == 'vig': p = (x - k) % 26
        elif variant == 'beau': p = (k - x) % 26
        else: p = (x + k) % 26
        out.append(chr(p + 97))
    return ''.join(out)


def solve(ct, period, variant, q, rnd, restarts=6):
    best = (-1e9, None)
    for r in range(restarts):
        key = [rnd.randrange(26) for _ in range(period)]
        cur = q.score(dec(ct, key, variant))
        improved = True
        while improved:
            improved = False
            for j in range(period):
                for s in range(26):
                    if s == key[j]: continue
                    old = key[j]; key[j] = s
                    v = q.score(dec(ct, key, variant))
                    if v > cur: cur, improved = v, True
                    else: key[j] = old
        if cur > best[0]: best = (cur, list(key))
    return best


def main():
    langs = sys.argv[1:] or ['de', 'en', 'nl']
    rnd = random.Random(0)
    for lang in langs:
        q = Q(lang)
        for mid, ct in CT.items():
            target = q.score(q.sample(lang, len(ct)))
            sh = list(ct); random.Random(9).shuffle(sh); sh = ''.join(sh)
            rows = []
            for variant in ('vig', 'beau', 'var'):
                for p in range(1, 27):
                    sc, key = solve(ct, p, variant, q, rnd, restarts=3)
                    rows.append((sc, p, variant, key))
            rows.sort(reverse=True)
            sc, p, variant, key = rows[0]
            noise = solve(sh, p, variant, q, rnd, restarts=3)[0]
            print('%s msg %d: language %.0f | best %s p=%d %.0f (shuffled ct at same setting %.0f) %s'
                  % (lang, mid, target, variant, p, sc, noise, dec(ct, key, variant)[:50]), flush=True)


if __name__ == '__main__':
    main()
