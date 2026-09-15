"""Read the pen marks hanging under the Raadhuisstraat tram band (Illustration No. 14) as Morse.

Along the street, straighten a narrow strip around the band's lower outline. For each position along the
street measure how much ink hangs below that outline (a thin stroke = dot, a small filled block = dash, per the
2016 reading on Schmeh's blog). Runs of hanging ink are classified by width; gaps between runs give symbol and
letter boundaries. The decoded Morse letters are then shifted +11, as the manual prescribes.
"""
import math, sys
import numpy as np
from PIL import Image, ImageOps

import bands

MORSE = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g', '....': 'h', '..': 'i',
         '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n', '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r',
         '...': 's', '-': 't', '..-': 'u', '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y', '--..': 'z',
         '.-.-': 'ä', '---.': 'ö', '..--': 'ü', '----': 'ch'}
REV = {v: k for k, v in MORSE.items()}

PTS = [(250, 722), (350, 672), (450, 641), (550, 626), (650, 616), (750, 602), (850, 577), (920, 560)]


def shift(s, k):
    return ''.join(chr((ord(c) - 97 + k) % 26 + 97) if 'a' <= c <= 'z' else c for c in s)


def strip():
    a = np.array(Image.open(bands.IMG).convert('L')).astype(float)
    P = bands.resample(PTS, step=0.5)
    N = bands.normals(P)
    if N[len(N) // 2][1] < 0: N = -N
    offs = np.arange(-16, 20, 0.5)
    S = np.stack([bands.bilinear(a, P[:, 0] + o * N[:, 0], P[:, 1] + o * N[:, 1]) for o in offs], axis=0)
    return S, offs, P


def hanging(S, offs, thr=120):
    ink = S < thr
    H, W = ink.shape
    # the band's lower outline: per column, the lowest row of the contiguous dark mass that contains the
    # darkest row near offset 0; smoothed strongly so marks do not move it
    edge = np.zeros(W)
    for x in range(W):
        col = ink[:, x]
        rows = np.where(col[(offs > -12) & (offs < 4)])[0]
        edge[x] = rows.max() + np.argmax(offs > -12) if len(rows) else np.nan
    e = np.array(edge); good = ~np.isnan(e)
    e[~good] = np.interp(np.where(~good)[0], np.where(good)[0], e[good])
    k = 121
    base = np.array([np.median(e[max(0, i - k // 2): i + k // 2]) for i in range(W)])
    depth = np.zeros(W)
    for x in range(W):
        r0 = int(base[x]) + 2
        col = ink[r0:, x]
        d = 0
        while d < len(col) and col[d]: d += 1
        depth[x] = d
    return depth, base


def runs(depth, min_depth=3):
    on = depth >= min_depth
    out, s = [], None
    for i, b in enumerate(on):
        if b and s is None: s = i
        if not b and s is not None: out.append((s, i)); s = None
    if s is not None: out.append((s, len(on)))
    return out


def main():
    S, offs, P = strip()
    depth, base = hanging(S, offs)
    R = runs(depth)
    widths = [(e - s) * 0.5 for s, e in R]          # in map pixels
    print('%d hanging marks; widths (px): %s' % (len(R), ' '.join('%.1f' % w for w in widths)))
    xs = [P[(s + e) // 2][0] for s, e in R]
    for (s, e), w, x in zip(R, widths, xs):
        print('   at x=%4.0f  width %4.1f  max depth %4.1f' % (x, w, depth[s:e].max() * 0.5))
    img = Image.fromarray(np.clip(S, 0, 255).astype(np.uint8))
    img = ImageOps.autocontrast(img, cutoff=1).convert('RGB')
    from PIL import ImageDraw
    d = ImageDraw.Draw(img)
    for s, e in R:
        d.line([(s, img.height - 3), (e, img.height - 3)], fill=(255, 0, 0), width=3)
    for k, s0 in enumerate(range(0, img.width, 420)):
        c = img.crop((s0, 0, min(img.width, s0 + 440), img.height))
        c.resize((c.width * 2, c.height * 4), Image.LANCZOS).save('mr_%d.png' % k)


if __name__ == '__main__':
    main()
