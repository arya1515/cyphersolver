"""Isomorph search: is the monographe verse a syllable-for-glyph encoding of some 20 lines of French verse?

For each candidate window (20 consecutive verse lines, prefiltered for rhyming couplets), align glyphs to
syllables LINE BY LINE (the line division is known), iterating: align with a monotone DP that rewards pairs
already seen elsewhere, recount, realign. Score = mapping consistency (see isomorph.py). A positive control
- a real French window encoded with a random syllabary, 15% glyph noise and per-line insertions/deletions -
is planted in the corpus to check that the search can find what it is looking for.

Usage: python versesearch.py [max_windows]
"""
import collections, glob, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from verse_transcription import lines as verse_glyph_lines
from isomorph import auto_syllables, score
import shape


def syl_lines(W):
    return [auto_syllables([l]) for l in W]


def dp_align(G, S, w, gap=0.6):
    n, m = len(G), len(S)
    NEG = -1e9
    D = [[NEG] * (m + 1) for _ in range(n + 1)]; B = [[None] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            if D[i][j] == NEG: continue
            if i < n and j < m:
                v = D[i][j] + w(G[i], S[j])
                if v > D[i + 1][j + 1]: D[i + 1][j + 1] = v; B[i + 1][j + 1] = (i, j, True)
            if i < n and D[i][j] - gap > D[i + 1][j]: D[i + 1][j] = D[i][j] - gap; B[i + 1][j] = (i, j, False)
            if j < m and D[i][j] - gap > D[i][j + 1]: D[i][j + 1] = D[i][j] - gap; B[i][j + 1] = (i, j, False)
    pairs, i, j = [], n, m
    while (i, j) != (0, 0):
        pi, pj, match = B[i][j]
        if match: pairs.append((G[pi], S[pj]))
        i, j = pi, pj
    return pairs[::-1]


def em_score(GL, SL, iters=4):
    # start: proportional (diagonal) pairing within each line
    pairs = []
    for G, S in zip(GL, SL):
        for k, g in enumerate(G):
            pairs.append((g, S[min(len(S) - 1, int(k * len(S) / len(G)))]))
    for _ in range(iters):
        cnt = collections.Counter(pairs)
        gtot = collections.Counter(g for g, _ in pairs); stot = collections.Counter(s for _, s in pairs)
        w = lambda g, s: (2.0 * cnt[(g, s)] / (gtot[g] + stot[s])) if cnt[(g, s)] else 0.0
        pairs = [p for G, S in zip(GL, SL) for p in dp_align(G, S, w)]
    return score(pairs)


def windows(files):
    for f in files:
        for W in shape.windows(f):
            yield os.path.basename(f), W


def rhymes_ok(W):
    rk = [shape.rhyme_key(l, 'fr') for l in W]
    c = sum(1 for k in range(0, 20, 2) if rk[k] and rk[k] == rk[k + 1])
    a = sum(1 for k in range(1, 19, 2) if rk[k] and rk[k] == rk[k + 1])
    return c >= 6 and a <= 3


def plant(W, rnd):
    SL = syl_lines(W)
    key = {}
    GL = []
    for S in SL:
        G = []
        for s in S:
            key.setdefault(s, 'k%d' % len(key))
            G.append(key[s] if rnd.random() > 0.15 else 'n%d' % rnd.randrange(10 ** 6))
        if rnd.random() < 0.5: G.insert(rnd.randrange(len(G) + 1), 'i%d' % rnd.randrange(10 ** 6))
        if rnd.random() < 0.5 and len(G) > 3: del G[rnd.randrange(len(G))]
        GL.append(G)
    return GL


def main():
    maxw = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 9
    files = sorted(glob.glob(os.path.join(HERE, 'corpus', 'fr*.txt')))
    real_GL = verse_glyph_lines()
    rnd = random.Random(5)
    cands = [(f, W) for f, W in windows(files) if rhymes_ok(W)]
    rnd.shuffle(cands)
    cands = cands[:maxw]
    print('%d rhyming-couplet windows' % len(cands), flush=True)
    planted_f, planted_W = cands[len(cands) // 2]
    planted_GL = plant(planted_W, random.Random(9))
    res_real, res_plant = [], []
    for k, (f, W) in enumerate(cands):
        SL = syl_lines(W)
        if any(len(S) == 0 for S in SL): continue
        res_real.append((em_score(real_GL, SL), f, W[0][:50]))
        res_plant.append((em_score(planted_GL, SL), f, W[0][:50], W is planted_W))
        if k % 500 == 0: print('  %d' % k, flush=True)
    res_real.sort(reverse=True); res_plant.sort(reverse=True)
    print('\npositive control (planted encoding of %s | %s):' % (planted_f, planted_W[0][:50]))
    rank = [i for i, r in enumerate(res_plant) if r[3]][0]
    print('   true window ranks %d of %d, score %d; next best %d; median %d'
          % (rank + 1, len(res_plant), res_plant[rank][0], res_plant[1 if rank == 0 else 0][0], res_plant[len(res_plant) // 2][0]))
    print('\nmonographe verse, top windows (median %d):' % res_real[len(res_real) // 2][0])
    for s, f, first in res_real[:12]:
        print('   %d  %s | %s' % (s, f, first))


if __name__ == '__main__':
    main()
