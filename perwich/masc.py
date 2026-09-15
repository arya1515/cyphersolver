"""Perwich 1670 is a substitution, not a transposition - and this solves it.

Everyone who has looked at this has called it a transposition. The National Archives blog that
published it in August 2025 presents it that way, Tomokiyo's own post is titled "an undeciphered
transposition cipher", and this project's tracker repeated the guess.

The frequency test says otherwise, and it is not a close call:

    index of coincidence        0.0629     English 0.0667, random 0.0385
    chi-squared IN PLACE        154.7      English samples of this length give about 25
    chi-squared SORTED          8.7        English samples give about 12

A transposition moves letters around but leaves each one as itself, so the in-place chi-squared would
be ordinary. It is six times too large. Meanwhile the sorted profile - the frequency shape with the
identities thrown away - fits English better than a typical English sample of the same length. That is
a substitution: identities scrambled, shape preserved.

Which also explains why three separate transposition attacks failed here: reading down the transcribed
columns, hill-climbing every columnar period from 4 to 26, and ten reading routes over the grid and
over each page.

So: hill-climb a monoalphabetic key against English quadgrams. Restarts must agree, or it is not
solved.

Usage: python masc.py [restarts] [iters]
"""
import collections, glob, math, os, random, re, sys

import grid

CORPUS = os.path.join('..', 'beale', 'lmcorpus')
AL = 'abcdefghijklmnopqrstuvwxyz'


def ciphertext(u_as_ll=True):
    """Every alphabetic character of the grid, in reading order."""
    rows = grid.load()
    out = []
    for r in rows:
        for c in r:
            c = grid.norm(c)
            if not c or c.isdigit():
                continue
            if c == 'U' and u_as_ll:
                out.append('ll')
            else:
                out.append(re.sub(r'[^A-Za-z]', '', c))
    return ''.join(out).lower()


def quadgrams(max_files=20):
    cnt = collections.Counter()
    for f in sorted(glob.glob(os.path.join(CORPUS, '*.txt')))[:max_files]:
        t = re.sub('[^a-z]', '', open(f, encoding='utf-8', errors='ignore').read().lower())
        for i in range(len(t) - 3):
            cnt[t[i:i + 4]] += 1
    tot = sum(cnt.values())
    floor = math.log10(0.01 / tot)
    return {k: math.log10(v / tot) for k, v in cnt.items()}, floor


class Q:
    def __init__(self):
        self.d, self.floor = quadgrams()

    def score(self, s):
        return sum(self.d.get(s[i:i + 4], self.floor) for i in range(len(s) - 3))


def apply_key(ct, key):
    return ct.translate(str.maketrans(AL, key))


def climb(ct, q, rnd, iters=6000):
    key = list(AL)
    rnd.shuffle(key)
    key = ''.join(key)
    best = q.score(apply_key(ct, key))
    improved = True
    while improved:
        improved = False
        for a in range(26):
            for b in range(a + 1, 26):
                k = list(key)
                k[a], k[b] = k[b], k[a]
                k = ''.join(k)
                v = q.score(apply_key(ct, k))
                if v > best:
                    best, key, improved = v, k, True
    return best, key


def main():
    restarts = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    q = Q()
    ct = ciphertext()
    print('ciphertext %d letters' % len(ct))
    print('%s ...' % ct[:80])
    eng = re.sub('[^a-z]', '', open(os.path.join(CORPUS, 'pg1342.txt'), encoding='utf-8',
                                    errors='ignore').read().lower())[:len(ct)]
    print('\ncalibration: real English scores %.0f, the raw ciphertext %.0f'
          % (q.score(eng), q.score(ct)))

    res = []
    for r in range(restarts):
        rnd = random.Random(r)
        sc, key = climb(ct, q, rnd)
        res.append((sc, key))
        if r < 3 or sc >= max(x[0] for x in res):
            print('   run %2d  %.0f  %s' % (r + 1, sc, apply_key(ct, key)[:70]), flush=True)
    res.sort(reverse=True)
    print('\nbest %.0f' % res[0][0])
    pt = apply_key(ct, res[0][1])
    for i in range(0, min(len(pt), 560), 70):
        print('   %s' % pt[i:i + 70])
    agree = sum(1 for a, b in zip(res[0][1], res[1][1]) if a == b) if len(res) > 1 else 0
    print('\ntop two keys agree on %d of 26 positions' % agree)
    print('key: plain %s' % AL)
    print('     ciph. %s' % res[0][1])


if __name__ == '__main__':
    main()
