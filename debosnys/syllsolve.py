"""Can a glyph -> French-syllable key be recovered from ~1,000 glyphs? Positive control first, then the real text.

LM: syllable bigrams (orthographic syllables, isomorph.auto_syllables) from the French corpus, one volume held
out. Solver: simulated annealing over the key (each glyph type -> one syllable from the top-N list), scoring
the whole sequence under the bigram model, with incremental rescoring of only the positions of the changed glyph.

Control: N syllables of held-out French encoded one-to-one (each syllable type its own glyph). Accuracy =
share of tokens whose recovered syllable is right. If the control fails at the cipher's length, no key-only
solve of the Debosnys corpus is possible, whatever the real plaintext is.

Usage: python syllsolve.py control N   |   python syllsolve.py real
"""
import collections, glob, math, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from isomorph import auto_syllables
from unitstats import verse_lines

TOPN = 600
HOLDOUT = os.environ.get('HOLDOUT', 'fr17899.txt')


def corpus_syllables(files):
    out = []
    for f in files:
        for l in verse_lines([f]):
            out.extend(auto_syllables([l]) + ['#'])
    return out


class LM:
    def __init__(self, sylls):
        c = collections.Counter(sylls)
        self.vocab = [s for s, _ in c.most_common(TOPN) if s != '#']
        V = set(self.vocab) | {'#', '<u>'}
        norm = [s if s in V else '<u>' for s in sylls]
        self.uni = collections.Counter(norm)
        self.bi = collections.Counter(zip(norm, norm[1:]))
        self.N = len(norm); self.V = len(V)
        self.freq = [self.uni[s] for s in self.vocab]

    def lp(self, a, b):
        return math.log((self.bi[(a, b)] + 0.1) / (self.uni[a] + 0.1 * self.V))


def anneal(seq, lm, rnd, iters=200000):
    types = sorted(set(seq))
    pos = collections.defaultdict(list)
    for i, g in enumerate(seq): pos[g].append(i)
    key = {g: lm.vocab[min(len(lm.vocab) - 1, int(rnd.expovariate(1 / 40)))] for g in types}
    dec = [key[g] for g in seq]

    def local(i):
        s = 0.0
        if i > 0: s += lm.lp(dec[i - 1], dec[i])
        if i + 1 < len(dec): s += lm.lp(dec[i], dec[i + 1])
        return s

    total = sum(lm.lp(dec[i], dec[i + 1]) for i in range(len(dec) - 1))
    T0 = 3.0
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.02
        g = rnd.choice(seq)                                  # frequent glyphs chosen more often
        new = rnd.choices(lm.vocab, weights=lm.freq)[0] if rnd.random() < 0.7 else rnd.choice(lm.vocab)
        old = key[g]
        if new == old: continue
        idx = set()
        for i in pos[g]: idx.update((i - 1, i))
        idx = {i for i in idx if 0 <= i < len(dec) - 1}
        before = sum(lm.lp(dec[i], dec[i + 1]) for i in idx)
        for i in pos[g]: dec[i] = new
        after = sum(lm.lp(dec[i], dec[i + 1]) for i in idx)
        d = after - before
        if d >= 0 or rnd.random() < math.exp(d / T):
            key[g] = new; total += d
        else:
            for i in pos[g]: dec[i] = old
    return total, key, dec


def main():
    files = sorted(glob.glob(os.path.join(HERE, 'corpus', 'fr*.txt')))
    train = [f for f in files if not f.endswith(HOLDOUT)]
    lm = LM(corpus_syllables(train))
    mode = sys.argv[1]
    if mode == 'control':
        n = int(sys.argv[2])
        held = [s for s in corpus_syllables([f for f in files if f.endswith(HOLDOUT)]) if s != '#']
        start = random.Random(1).randrange(len(held) - n)
        plain = held[start:start + n]
        types = {s: 'g%d' % k for k, s in enumerate(dict.fromkeys(plain))}
        seq = [types[s] for s in plain]
        best = None
        for r in range(3):
            res = anneal(seq, lm, random.Random(r))
            if best is None or res[0] > best[0]: best = res
        acc = sum(1 for a, b in zip(best[2], plain) if a == b) / n
        base = sum(1 for s in plain if s == lm.vocab[0]) / n
        print('control n=%d, %d glyph types: token accuracy %.1f%% (always-most-frequent baseline %.1f%%)'
              % (n, len(types), 100 * acc, 100 * base))
        print('   plain :', ' '.join(plain[:40]))
        print('   solved:', ' '.join(best[2][:40]))
    else:
        from verse_transcription import lines
        from n9_transcription import tokens as t9
        from n10_transcription import tokens as t10
        seq = [g for l in lines() for g in l] + t10(True) + t9()
        real = max((anneal(seq, lm, random.Random(r)) for r in range(3)), key=lambda x: x[0])
        sh = list(seq); random.Random(5).shuffle(sh)
        ctrl = max((anneal(sh, lm, random.Random(r)) for r in range(3)), key=lambda x: x[0])
        print('real order %.0f  vs shuffled %.0f  (%d glyphs)' % (real[0], ctrl[0], len(seq)))
        print('   verse line 1 as solved:', ' '.join(real[2][:12]))


if __name__ == '__main__':
    main()
