"""Forced alignment of a line's glyph boxes to its known plaintext.

Counting figures cannot place boxes exactly: digraph figures (the doubled-s) swallow a letter, the
segmenter merges or splits unevenly, and the per-line gap is not universal. So instead of counting,
align by content. Each box gets an emission score against each letter from how closely it resembles
that letter's exemplars, and a DP chooses how the boxes and letters pair up, allowing:

    box -> 1 letter        the ordinary case
    box -> 2 letters       a digraph figure, or two figures merged by the segmenter
    box -> nothing         a null, a stray dot, or a fragment of an over-split figure
    2 boxes -> 1 letter    one figure split in two

Only pairings that come out one-box-one-letter with a good margin are used to mint new exemplars,
so the output is a set of labels that the evidence, not the arithmetic, supports.
"""
import json, sys
import numpy as np
from PIL import Image, ImageOps
from scipy import ndimage
from rlsa import otsu
from shapes import line_boxes
from checkex import vec as vec_file
from readleaf import vec_from

def load_exemplars():
    """Letters keyed by themselves; code groups keyed as <word>, e.g. <que>, <plustost>."""
    man = json.load(open('exemplars/manifest.json'))
    by = {}
    for m in man:
        key = m['letter'] if len(m['letter']) == 1 else '<' + m['letter'] + '>'
        by.setdefault(key, []).append(vec_file(m['file']))
    return by

def tokens(text):
    """Plaintext as tokens: single letters, plus <word> for a word written as one code figure."""
    out = []; i = 0
    while i < len(text):
        if text[i] == '<':
            j = text.index('>', i); out.append(text[i:j+1]); i = j + 1
        else:
            out.append(text[i]); i += 1
    return out

def emission(bvec, by, tok):
    ex = by.get(tok)
    if not ex:
        return -0.9 if tok.startswith('<') else -0.6   # an unknown code is less likely than a letter
    return max(float(bvec @ e) for e in ex)

def align(bvecs, text, by, skip=-0.55, split=-0.35, digraph=-0.15):
    n, m = len(bvecs), len(text)
    NEG = -1e9
    D = np.full((n+1, m+1), NEG); D[0, 0] = 0.0
    back = {}
    E = [[emission(b, by, ch) for ch in text] for b in bvecs]
    for i in range(n+1):
        for j in range(m+1):
            if D[i, j] == NEG: continue
            cands = []
            if i < n and j < m:   cands.append((i+1, j+1, E[i][j], '1'))
            if i < n and j+1 < m: cands.append((i+1, j+2, 0.5*(E[i][j]+E[i][j+1]) + digraph, '2'))
            if i < n:             cands.append((i+1, j, skip, '0'))
            if i+1 < n and j < m: cands.append((i+2, j+1, max(E[i][j], E[i+1][j]) + split, 's'))
            for ni, nj, s, op in cands:
                v = D[i, j] + s
                if v > D[ni, nj]:
                    D[ni, nj] = v; back[(ni, nj)] = (i, j, op)
    # walk back from the best end state that has consumed the whole text
    i, j = n, m
    path = []
    while (i, j) != (0, 0) and (i, j) in back:
        pi, pj, op = back[(i, j)]
        path.append((pi, i, pj, j, op)); i, j = pi, pj
    return list(reversed(path)), D[n, m]

def run(src, ysfile, line, gap, text, mint_from=None):
    toks = tokens(text)
    im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
    a = np.array(im); bw = ndimage.median_filter(a < otsu(a), size=3)
    ys = [int(v) for v in open(ysfile).read().split(',')]
    ink = np.convolve((a < (a.mean()-0.45*a.std())).sum(axis=1).astype(float), np.ones(11)/11, 'same')
    pitch = int(np.median(np.diff(ys))); w = max(10, int(0.38*pitch))
    ys = [int(max(0, y-w) + np.argmax(ink[max(0, y-w):min(len(ink), y+w)])) for y in ys]
    bs = line_boxes(bw, ys[line-1], 40, gap)
    bvecs = [vec_from(a[y0:y1, x0:x1]) for (x0, x1, y0, y1) in bs]
    by = load_exemplars()
    path, score = align(bvecs, toks, by)
    ops = ''.join(p[4] for p in path)
    print(f'line {line}: {len(bs)} boxes vs {len(toks)} tokens   score {score:.2f}')
    print(f'  ops  1:{ops.count("1")}  digraph:{ops.count("2")}  skip:{ops.count("0")}  split:{ops.count("s")}')
    shown = []
    for bi0, bi1, tj0, tj1, op in path:
        lab = ''.join(toks[tj0:tj1]) if tj1 > tj0 else '-'
        shown.append(f'{bi0+1}{"-"+str(bi1) if bi1-bi0>1 else ""}:{lab}')
    print('  ' + '  '.join(shown))
    return bs, path, a, toks

if __name__ == '__main__':
    run(sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5])
