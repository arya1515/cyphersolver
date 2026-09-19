"""Homophonic solver for the Kurz cipher: each symbol -> a letter, a consonant+vowel bigram, or null.

    python solve.py [--records R3811,R3813] [--fix key.json] [--iters 200000] [--restarts 4] [--out key_sa.json]

Scores the deciphered text (runs joined, no spaces) with a 5-gram German model in early spelling (u/v, i/j merged).
Symbols in --fix keep their value. Writes the best key and prints the decipherment of the first runs.
"""
import argparse, collections, json, math, os, random, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'cypher-lang'))
from lang import lm
from parse import load

LETTERS = 'abcdefghiklmnopqrstuwxyz'
VOW = 'aeiou'
CONS = 'bcdfghklmnpqrstwxz'
BIGR = [c + v for c in CONS for v in VOW]
CACHE = os.path.join(HERE, 'de_early5.npy')


def model():
    alpha = lm.alphabet('early', False)
    if os.path.exists(CACHE):
        return lm.DenseLM(np.load(CACHE), 5, alpha)
    sys.path.insert(0, os.path.join(HERE, '..', '..', 'cypher-lang'))
    from lang import corpora
    text = lm.norm(corpora.text(['de-gutenberg']), 'early', False)
    extra = os.path.join(HERE, 'corpus_de17.txt')
    if os.path.exists(extra):
        t2 = lm.norm(open(extra, encoding='utf-8').read(), 'early', False)
        text = t2 * 3 + text
    m = lm.DenseLM.build(text, 5, alpha)
    np.save(CACHE, m.lp)
    return m


def decode(runs, key):
    return [''.join(key.get(t, '?') for t in r) for _, r in runs]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--records')
    ap.add_argument('--fix')
    ap.add_argument('--iters', type=int, default=200000)
    ap.add_argument('--restarts', type=int, default=3)
    ap.add_argument('--out', default='key_sa.json')
    ap.add_argument('--nobigram', action='store_true')
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--kl', type=float, default=3.0)
    a = ap.parse_args()
    random.seed(a.seed)
    runs, _ = load(a.records.split(',') if a.records else None)
    runs = [(f, [t for t in r if '?' not in t]) for f, r in runs]
    runs = [x for x in runs if len(x[1]) >= 3]
    m = model()
    cnt = collections.Counter(t for _, r in runs for t in r)
    syms = sorted(cnt)
    fixed = json.load(open(a.fix, encoding='utf-8')) if a.fix else {}
    free = [s for s in syms if s not in fixed]
    vals = list(LETTERS) + ([] if a.nobigram else BIGR) + ['']
    # prior weight on values: letters common, bigrams and nulls rarer
    idx = {s: i for i, s in enumerate(syms)}
    seqs = [np.array([idx[t] for t in r]) for _, r in runs]
    enc = {c: i for i, c in enumerate(m.alpha if hasattr(m, 'alpha') else lm.alphabet('early', False))}

    def score(key):
        text = ''.join(''.join(key[s] for s in (syms[i] for i in q)) + '' for q in seqs)
        if len(text) < 10:
            return -1e9
        x = np.array([enc[c] for c in text], dtype=np.int64)
        return m.score_idx(x)

    ref = collections.Counter(lm.norm(open(os.path.join(HERE, 'corpus_de17.txt'), encoding='utf-8').read()[:400000], 'early', False))
    rt = sum(ref.values()); refp = {c: ref[c] / rt for c in LETTERS}

    def klpen(key):
        c = collections.Counter()
        for k, v in key.items():
            for ch in v:
                c[ch] += cnt[k]
        n = sum(c.values()) or 1
        return n * sum((c[ch] / n) * math.log((c[ch] / n) / max(refp[ch], 1e-4)) for ch in c if c[ch])

    def total(key):
        s = score(key) - a.kl * klpen(key)
        pen = sum(4 for v in key.values() if len(v) == 2) + sum(3.0 * cnt[k] for k, v in key.items() if v == '')
        return s - pen

    best_all = None
    for r in range(a.restarts):
        key = dict(fixed)
        freq = 'enirstadhulgcmobwfkzp'
        for i, s in enumerate(sorted(free, key=lambda s: -cnt[s])):
            key[s] = freq[i % len(freq)]
        cur = total(key)
        best = (cur, dict(key))
        T0 = 3.0
        for it in range(a.iters):
            T = T0 * (1 - it / a.iters) + 0.02
            s = random.choice(free)
            old = key[s]
            if random.random() < 0.8:
                key[s] = random.choice(LETTERS)
            else:
                key[s] = random.choice(vals)
            if key[s] == old:
                continue
            new = total(key)
            if new >= cur or random.random() < math.exp((new - cur) / T):
                cur = new
                if cur > best[0]:
                    best = (cur, dict(key))
            else:
                key[s] = old
        print(f'restart {r}: {best[0]:.2f}', flush=True)
        if best_all is None or best[0] > best_all[0]:
            best_all = best
    key = best_all[1]
    json.dump(key, open(os.path.join(HERE, a.out), 'w'), indent=0, sort_keys=True)
    for (f, r), d in list(zip(runs, decode(runs, key)))[:30]:
        print(f, d)


if __name__ == '__main__':
    main()
