"""Segment cipher lines into token images by column-profile gaps."""
from PIL import Image, ImageOps
import numpy as np, os, sys, json

Image.MAX_IMAGE_PIXELS = None

def segment_line(img, out_prefix, thresh=160, min_gap=14, min_w=8, pad=6):
    g = np.array(img.convert('L'))
    ink = (g < thresh)
    col = ink.sum(axis=0)
    on = col > 0
    toks = []
    i = 0
    n = len(on)
    while i < n:
        if on[i]:
            j = i
            while j < n:
                # extend while gap < min_gap
                k = j
                while k < n and on[k]:
                    k += 1
                # k = first off
                k2 = k
                while k2 < n and not on[k2] and k2 - k < min_gap:
                    k2 += 1
                if k2 < n and on[k2] and k2 - k < min_gap:
                    j = k2
                    continue
                break
            x0, x1 = i, k
            if x1 - x0 >= min_w:
                rows = ink[:, x0:x1].sum(axis=1)
                ys = np.nonzero(rows)[0]
                if len(ys):
                    y0, y1 = ys[0], ys[-1]
                    toks.append((x0, x1, int(y0), int(y1)))
            i = k2 if k2 > k else k + 1
        else:
            i += 1
    outs = []
    for t, (x0, x1, y0, y1) in enumerate(toks):
        c = img.crop((max(0, x0 - pad), max(0, y0 - pad), min(img.width, x1 + pad), min(img.height, y1 + pad)))
        w, h = c.size
        sc = 90 / max(1, h)
        c = c.resize((max(1, int(w * sc)), 90), Image.LANCZOS)
        fn = f'{out_prefix}_{t:02d}.png'
        c.save(fn)
        outs.append(fn)
    return outs

def grid(files, out, cols=12, cell=(110, 100)):
    n = len(files)
    rows = (n + cols - 1) // cols
    im = Image.new('L', (cols * cell[0], rows * (cell[1] + 26)), 255)
    from PIL import ImageDraw, ImageFont
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype('arial.ttf', 18)
    except Exception:
        font = None
    for i, f in enumerate(files):
        t = Image.open(f)
        x = (i % cols) * cell[0]
        y = (i // cols) * (cell[1] + 26)
        t.thumbnail((cell[0] - 6, cell[1] - 4))
        im.paste(t, (x + 3, y + 22))
        d.text((x + 3, y + 2), str(i), fill=0, font=font)
    im.save(out)
    return out

if __name__ == '__main__':
    pass
