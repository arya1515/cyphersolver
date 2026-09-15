"""Unroll the segmented tram bands of the censorship-manual map (Illustration No. 14) into straight strips.

The manual says: "Morse can be introduced into the heavy lining in the print such as tram lines". Each band is
two thin outlines with an interior alternately inked and blank. Given rough waypoints along a band, resample
the path every half pixel, re-centre each point between the band's two outlines, and sample the perpendicular
profile. The result is a straight strip image (for reading by eye) and an interior intensity profile (for
run-length decoding).

Usage: python bands.py NAME   (writes strip_NAME.png and profile_NAME.json)
"""
import json, math, sys
import numpy as np
from PIL import Image

IMG = 'Censor-Manual-map.png'

# rough waypoints (x, y) in full-resolution map pixels, in reading order
BANDS = {
    'rokin_inner': [(1178, 150), (1160, 260), (1140, 400), (1150, 520), (1170, 640), (1195, 780), (1210, 900), (1225, 980), (1270, 1060), (1340, 1110)],
    'rokin_outer': [(1272, 150), (1250, 260), (1218, 400), (1240, 520), (1262, 640), (1288, 780), (1306, 900), (1330, 990), (1400, 1060), (1500, 1100)],
    'kalver': [(1005, 130), (975, 240), (930, 350), (905, 450), (925, 560), (960, 680), (985, 800), (1000, 920), (1000, 1050), (1010, 1130)],
}


def resample(pts, step=0.5):
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d = math.hypot(x1 - x0, y1 - y0); n = max(1, int(d / step))
        for k in range(n):
            t = k / n; out.append((x0 + t * (x1 - x0), y0 + t * (y1 - y0)))
    out.append(pts[-1])
    return np.array(out)


def bilinear(a, x, y):
    x0 = np.clip(np.floor(x).astype(int), 0, a.shape[1] - 2); y0 = np.clip(np.floor(y).astype(int), 0, a.shape[0] - 2)
    fx = x - x0; fy = y - y0
    return (a[y0, x0] * (1 - fx) * (1 - fy) + a[y0, x0 + 1] * fx * (1 - fy) + a[y0 + 1, x0] * (1 - fx) * fy + a[y0 + 1, x0 + 1] * fx * fy)


def normals(P):
    d = np.gradient(P, axis=0)
    d = np.array([np.convolve(d[:, k], np.ones(15) / 15, mode='same') for k in range(2)]).T
    n = np.stack([-d[:, 1], d[:, 0]], axis=1)
    return n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-9)


def recenter(a, P, half=14):
    N = normals(P); offs = np.arange(-half, half + 1)
    prof = np.stack([bilinear(a, P[:, 0] + o * N[:, 0], P[:, 1] + o * N[:, 1]) for o in offs], axis=1)
    # smooth along the band so segment ink does not pull the centre
    k = 41
    sm = np.array([np.convolve(prof[:, j], np.ones(k) / k, mode='same') for j in range(prof.shape[1])]).T
    centers = []
    for row in sm:
        best, bc = None, 0
        for i in range(len(offs)):
            for j in range(i + 6, min(len(offs), i + 22)):
                v = row[i] + row[j] - 0.5 * row[(i + j) // 2]   # two dark outlines, lighter middle on average
                if best is None or v < best: best, bc = v, (offs[i] + offs[j]) / 2
        centers.append(bc)
    c = np.convolve(np.array(centers, float), np.ones(61) / 61, mode='same')
    return P + c[:, None] * N


def unroll(name, half=10):
    a = np.array(Image.open(IMG).convert('L')).astype(float)
    P = resample(BANDS[name])
    for _ in range(2):
        P = recenter(a, P)
    N = normals(P); offs = np.arange(-half, half + 1, 0.5)
    strip = np.stack([bilinear(a, P[:, 0] + o * N[:, 0], P[:, 1] + o * N[:, 1]) for o in offs], axis=0)
    img = Image.fromarray(np.clip(strip, 0, 255).astype(np.uint8))
    # break long strips into rows for viewing
    W = img.width; rowlen = 1400; rows = [img.crop((s, 0, min(W, s + rowlen), img.height)) for s in range(0, W, rowlen)]
    sheet = Image.new('L', (rowlen, (img.height * 3 + 12) * len(rows)), 255)
    for k, r in enumerate(rows):
        sheet.paste(r.resize((r.width, r.height * 3)), (0, k * (img.height * 3 + 12)))
    sheet.save('strip_%s.png' % name)
    mid = strip[len(offs) // 2 - 3: len(offs) // 2 + 4].mean(axis=0)
    json.dump({'path': P.tolist(), 'interior': mid.tolist()}, open('profile_%s.json' % name, 'w'))
    print(name, 'length %.0f px, strip %s' % (len(P) * 0.5, img.size))


if __name__ == '__main__':
    for n in (sys.argv[1:] or BANDS):
        unroll(n)
