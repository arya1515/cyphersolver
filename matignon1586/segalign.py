"""Forced alignment with code groups pinned to boxes read by eye.

On f. 143 the codes are written as two separate digits and the segmenter splits them (13 = a "1" box
and a "3" box), while neighbouring letters are sometimes merged two to a box. Either problem alone the
aligner absorbs; both together make it slip a box. So the numerals, which can be verified by eye, are
made hard boundaries, and only the letter stretches between them are aligned.

    pins: list of (box_from, box_to, token)   e.g. [(3, 4, '<qui>'), (12, 13, '<que>')]
"""
import sys, io, os, json
_o = sys.stdout; sys.stdout = io.StringIO()
from forcealign import align, load_exemplars, tokens
from readleaf import vec_from
sys.stdout = _o
import numpy as np
from PIL import Image, ImageOps
from scipy import ndimage
from rlsa import otsu
from shapes import line_boxes

def boxes_for(src, ysfile, line, gap):
    im = ImageOps.autocontrast(Image.open(src).convert('L'), 1)
    a = np.array(im); bw = ndimage.median_filter(a < otsu(a), size=3)
    ys = [int(v) for v in open(ysfile).read().split(',')]
    return line_boxes(bw, ys[line-1], 40, gap), a

def segalign(src, ysfile, line, gap, text, pins):
    bs, a = boxes_for(src, ysfile, line, gap)
    by = load_exemplars()
    toks = tokens(text)
    # split tokens at the pinned codes, in order
    out = []; ti = 0; bi = 1
    for b0, b1, code in pins + [(len(bs)+1, len(bs)+1, None)]:
        if code is not None:
            j = toks.index(code, ti)
        else:
            j = len(toks)
        seg_toks = toks[ti:j]; seg_boxes = list(range(bi, b0))
        if seg_toks and seg_boxes:
            V = [vec_from(a[bs[k-1][2]:bs[k-1][3], bs[k-1][0]:bs[k-1][1]]) for k in seg_boxes]
            path, _ = align(V, seg_toks, by)
            for p0, p1, t0, t1, op in path:
                out.append((seg_boxes[p0], seg_boxes[p1-1], ''.join(seg_toks[t0:t1]) or '-', op))
        elif seg_toks or seg_boxes:
            out.append((seg_boxes[0] if seg_boxes else bi, seg_boxes[-1] if seg_boxes else bi,
                        ''.join(seg_toks) or '-', 'X'))
        if code is not None:
            out.append((b0, b1, code, 'pin')); ti = j + 1; bi = b1 + 1
    return bs, a, out

if __name__ == '__main__':
    pass
