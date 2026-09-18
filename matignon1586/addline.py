"""Add one crib line to the exemplar set, with every safeguard learned the hard way.

    python addline.py <line> "<plaintext with <code> tokens>"

1. choose the segmenter gap whose box count is closest to the token count (lines vary: line 3 was
   split 2:1 at the gap that suited line 2, line 7 under-segmented);
2. force-align boxes to tokens by content;
3. mint only one-box-one-token pairings;
4. ablate: drop the new exemplars one letter at a time and re-score the held-out lines; any letter
   whose removal *raises* the score is harmful and is rejected (similarity audits do not find these);
5. keep the rest, and report the score before and after.
"""
import sys, io, os, json, re, subprocess
import numpy as np
from PIL import Image, ImageOps
from scipy import ndimage
from rlsa import otsu
from shapes import line_boxes
_o = sys.stdout; sys.stdout = io.StringIO()
from forcealign import run, tokens
sys.stdout = _o

SRC, YS = 'hi/f18rflat.png', 'f18r_lines.txt'
MAN = 'exemplars/manifest.json'

def score():
    o = subprocess.run([sys.executable, 'baseline.py'], capture_output=True, text=True).stdout
    return float(re.search(r'non-circular\s+\d+/\d+ = ([\d.]+)', o).group(1))

def best_gap(line, ntok):
    im = ImageOps.autocontrast(Image.open(SRC).convert('L'), 1)
    a = np.array(im); bw = ndimage.median_filter(a < otsu(a), size=3)
    ys = [int(v) for v in open(YS).read().split(',')]
    ink = np.convolve((a < (a.mean()-0.45*a.std())).sum(axis=1).astype(float), np.ones(11)/11, 'same')
    pitch = int(np.median(np.diff(ys))); w = max(10, int(0.38*pitch))
    ys = [int(max(0, y-w) + np.argmax(ink[max(0, y-w):min(len(ink), y+w)])) for y in ys]
    counts = {g: len(line_boxes(bw, ys[line-1], 40, g)) for g in range(6, 24)}
    g = min(counts, key=lambda g: (abs(counts[g] - ntok), -g))
    return g, counts[g]

def add(line, text, tag=None):
    tag = tag or f'f18r_l{line}auto'
    toks = tokens(text)
    gap, nb = best_gap(line, len(toks))
    _o = sys.stdout; sys.stdout = io.StringIO()
    bs, path, a, toks = run(SRC, YS, line, gap, text)
    sys.stdout = _o
    ops = ''.join(p[4] for p in path)
    print(f'line {line}: gap {gap} -> {nb} boxes for {len(toks)} tokens; '
          f'1:{ops.count("1")} digraph:{ops.count("2")} skip:{ops.count("0")} split:{ops.count("s")}')
    man = json.load(open(MAN))
    man = [m for m in man if m['src'] != tag]
    before = score() if True else None
    im = Image.fromarray(a); new = []
    for bi0, bi1, tj0, tj1, op in path:
        if op != '1': continue
        k = bi0 + 1; lab = toks[tj0].strip('<>')
        x0, x1, y0, y1 = bs[bi0]
        fn = f'exemplars/{tag}_{k:02d}_{lab}.png'
        im.crop((x0-4, y0-6, x1+4, y1+6)).save(fn)
        new.append({'file': fn, 'letter': lab, 'src': tag, 'box': [x0, x1, y0, y1],
                    'crib': f'addline {line} gap {gap}'})
    json.dump(man + new, open(MAN, 'w'), indent=1)
    with_all = score()
    harmful = []
    for L in sorted({m['letter'] for m in new}):
        json.dump(man + [m for m in new if m['letter'] != L], open(MAN, 'w'), indent=1)
        if score() - with_all > 1.0: harmful.append(L)
    keep = [m for m in new if m['letter'] not in harmful]
    for m in new:
        if m not in keep and os.path.exists(m['file']):
            os.replace(m['file'], 'exemplars/rejected/' + os.path.basename(m['file']))
    json.dump(man + keep, open(MAN, 'w'), indent=1)
    after = score()
    from collections import Counter
    c = Counter(m['letter'] for m in man + keep if len(m['letter']) == 1)
    print(f'  minted {len(new)}, rejected by ablation {len(new)-len(keep)} {harmful or ""}, kept {len(keep)}')
    print(f'  non-circular {before:.1f} -> {after:.1f} %    letters {len(c)}/22  '
          f'missing {[x for x in "abcdefghilmnopqrstuxyz" if x not in c]}')

if __name__ == '__main__':
    add(int(sys.argv[1]), sys.argv[2])
