# Local alignment (Smith-Waterman style) of each cipher line's class-probability sequence against a known plaintext.
# usage: crib_search.py probs.json boxes_g2.json plaintext.txt [minlen]
import sys, json, re, numpy as np, random
from boot2 import plain_classes, CLASSES
NULL = CLASSES.index('null')
def local_align(lpr, areas, P, gap=-3.0, skip=-2.5):
    n, m = len(lpr), len(P)
    H = np.zeros((n + 1, m + 1)); B = np.zeros((n + 1, m + 1), np.int8)
    best = (0, 0, 0)
    for t in range(1, n + 1):
        sk = -0.3 if areas[t - 1] < 130 else skip
        for p in range(1, m + 1):
            v = lpr[t - 1, P[p - 1]]
            cands = (H[t - 1, p - 1] + v, H[t - 1, p] + sk, H[t, p - 1] + gap, 0.0)
            b = int(np.argmax(cands)); H[t, p] = cands[b]; B[t, p] = b
            if H[t, p] > best[0]: best = (H[t, p], t, p)
    s, t, p = best
    # traceback for span
    t0, p0 = t, p; L = 0
    while t0 > 0 and p0 > 0 and H[t0, p0] > 0:
        b = B[t0, p0]
        if b == 0: t0 -= 1; p0 -= 1; L += 1
        elif b == 1: t0 -= 1
        else: p0 -= 1
    return s, (t0, t), (p0, p), L
if __name__ == '__main__':
    probs = json.load(open(sys.argv[1])); boxes = json.load(open(sys.argv[2]))
    text = open(sys.argv[3], encoding='utf-8').read()
    P = plain_classes(text)
    words = re.findall(r'[a-z#]+', text.lower())
    rnd = random.Random(1); shuf = words[:]; rnd.shuffle(shuf)
    Pshuf = plain_classes(' '.join(shuf))
    letters = re.sub(r'[^a-z# ]', '', text.lower()); letters = re.sub(r'\s+', ' ', letters)
    for k in sorted(probs, key=int):
        pr = np.array(probs[k]); pr = 0.9 * pr + 0.1 / pr.shape[1]
        # score relative to uniform-over-11 baseline so matches are positive
        lpr = np.log(pr) - np.log(1 / 11)
        ar = [b[4] for b in boxes[k]]
        s, (t0, t1), (p0, p1), L = local_align(lpr, ar, P)
        s2, _, _, L2 = local_align(lpr, ar, Pshuf)
        # map p0..p1 back to text approx: count letters
        flag = '  <==' if s > 1.6 * s2 and L >= 12 else ''
        print(f'L{k}: real {s:.1f} (len {L}, boxes {t0}-{t1}) shuffled {s2:.1f} (len {L2}){flag}', flush=True)
