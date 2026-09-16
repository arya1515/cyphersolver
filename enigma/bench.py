"""Benchmark climb configurations on real and synthetic 97-letter controls at the true scrambler location.
Metric: number of E-Stecker starts (of 26) that reach the true plugboard score, and time per start."""
import sys, time, numpy as np
from solver import *
from climb2 import climb2
from enigma_core import Enigma

mono = np.load('mono_logp.npy'); bi = np.load('bi_logp.npy'); tri = np.load('tri_logp.npy')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 97
rng = np.random.default_rng(1)

controls = []  # (name, order, ct, l, m, r, i0, pb)
KLPB = 'AM BF CD EK HQ IO LV NT SY WZ'
def pbarr(plugs):
    pb = np.arange(26)
    for pr in plugs.split():
        a, b = A.index(pr[0]), A.index(pr[1]); pb[a], pb[b] = b, a
    return pb
real = {
 'HK1': ('BUQVG DQYEU AUTCD FJFRG LIDWF WBKMH RBWIK OOBRL UBTSL EKDGK GMKDN GCZJV AGRGK TUNAH QDJRT GHYTR YEKSP KGWYQ OMEWN DXCWN XKPGJ', (9, 2, 24, 20)),
 'HK2': ('GDOIH RKODK NYZSJ ILGAO GPCRO ASTKN WIAEZ HDXAH IKZYG SSWXQ SRYCJ EEBGV RCGVK DCPVD WDFJT DBLMB VPJEP TTUEC WNHDD RKNZN QEIOI', (0, 9, 12, 6)),
 'HK3': ('ZRKRF VZQHO JZUVV DLBCG KUBJM ISTVG RLMPX GXGEN KQCJL RKJBA QYMGE ZSTZP BPWAL GMJIM JOQDZ YPOIZ JXVQN XURRE DIERI KQJBL UHVQJ', (4, 24, 11, 7)),
}
for k, (txt, (l, m, r, i0)) in real.items():
    controls.append((k, ('I', 'II', 'III'), letters(txt)[:N], l, m, r, i0, pbarr(KLPB)))

# synthetic: Wehrmacht-style German (converted Gutenberg + KL-like formulas), random keys
import lm_build, glob, os
txt = open(sorted(glob.glob('../adfgvx/corpus/de_*.txt'))[4], encoding='utf-8', errors='ignore').read()
conv = lm_build.convert(txt[200000:400000]).upper()
for j in range(9):
    order = tuple(rng.choice(WNAMES, 3, replace=False))
    rings = ''.join(rng.choice(list(A), 3)); start = ''.join(rng.choice(list(A), 3))
    lett = list(A); rng.shuffle(lett)
    plugs = ' '.join(''.join(sorted(lett[2 * i:2 * i + 2])) for i in range(10))
    p0 = rng.integers(0, len(conv) - N); pt = conv[p0:p0 + N]
    e = Enigma('B', list(order), rings, plugs)
    ct = letters(e.run(pt, start))
    # core positions of the first letter and i0
    pos = e.step([A.index(c) for c in start])
    l, m, r = [(pos[i] - e.rings[i]) % 26 for i in range(3)]
    notch = e.notch[2]
    i0 = (notch - pos[2]) % 26 + 1   # letters until the right window shows the notch letter, then step
    if i0 == 0: i0 = 26
    # left-wheel step inside the message? check: middle notch reached
    controls.append(('SYN%d' % j, order, ct, l, m, r, i0, pbarr(plugs)))

configs = {
 'ic7-tri/first':   (np.array([0, 7]), np.array([0, 3]), 5, False),
 'ic7-tri/steep':   (np.array([0, 7]), np.array([0, 3]), 5, True),
 'ic4-bi-tri8':     (np.array([0, 4, 8]), np.array([0, 2, 3]), 5, False),
 'ic3-bi6-tri9':    (np.array([0, 3, 6, 9]), np.array([0, 0, 2, 3]), 4, False),
 'mono-tri6':       (np.array([0, 6]), np.array([1, 3]), 4, False),
 'bi-tri7':         (np.array([0, 7]), np.array([2, 3]), 5, False),
 'tri-only':        (np.array([0]), np.array([3]), 5, False),
 'ic7-tri/back0':   (np.array([0, 7]), np.array([0, 3]), 0, False),
 'ic5-tri/steep':   (np.array([0, 5]), np.array([0, 3]), 3, True),
}
starts = e_stecker_starts()
tables = {}
for name, order, ct, l, m, r, i0, pb in controls:
    if order not in tables: tables[order] = build_table(order)
    S = np.empty((N, 26), dtype=np.int64); make_S(tables[order], l, m, r, i0, -1, N, S)
    out = np.empty(N, dtype=np.int64); decrypt(S, ct, pb, N, out)
    ts = score_tri(S, ct, pb, N, tri)
    print('%s %s true %.1f %s' % (name, '-'.join(order), ts, ''.join(A[i] for i in out)[:40]))
res = {c: [] for c in configs}; tm = {c: 0.0 for c in configs}
for name, order, ct, l, m, r, i0, pb in controls:
    S = np.empty((N, 26), dtype=np.int64); make_S(tables[order], l, m, r, i0, -1, N, S)
    ts = score_tri(S, ct, pb, N, tri)
    for c, (sf, sm, bf, st) in configs.items():
        ok = 0; t = time.time()
        for k in range(26):
            pbk = starts[k].copy()
            s = climb2(S, ct, N, pbk, sf, sm, bf, st, mono, bi, tri)
            if s >= ts - 1e-6: ok += 1
        tm[c] += time.time() - t
        res[c].append(ok)
        print(name, c, ok, '%.1fs' % (time.time()-t), flush=True)
print('\nconfig            ' + ' '.join('%4s' % n[:4] for n, *_ in controls) + '  solved  ms/start')
for c in configs:
    print('%-18s' % c + ' '.join('%4d' % v for v in res[c]) + '  %2d/%d   %.2f' % (sum(v > 0 for v in res[c]), len(controls), 1000 * tm[c] / (26 * len(controls))))
