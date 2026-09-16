"""Shared control set: 3 real 1945 Huppenkothen segments + 9 synthetic Wehrmacht-style messages, first N letters."""
import numpy as np, glob
from solver import *
from enigma_core import Enigma
import lm_build

KLPB = 'AM BF CD EK HQ IO LV NT SY WZ'


def pbarr(plugs):
    pb = np.arange(26)
    for pr in plugs.split():
        a, b = A.index(pr[0]), A.index(pr[1]); pb[a], pb[b] = b, a
    return pb


def make_controls(N, nsyn=9, seed=1):
    rng = np.random.default_rng(seed)
    controls = []
    real = {
     'HK1': ('BUQVG DQYEU AUTCD FJFRG LIDWF WBKMH RBWIK OOBRL UBTSL EKDGK GMKDN GCZJV AGRGK TUNAH QDJRT GHYTR YEKSP KGWYQ OMEWN DXCWN XKPGJ', (9, 2, 24, 20)),
     'HK2': ('GDOIH RKODK NYZSJ ILGAO GPCRO ASTKN WIAEZ HDXAH IKZYG SSWXQ SRYCJ EEBGV RCGVK DCPVD WDFJT DBLMB VPJEP TTUEC WNHDD RKNZN QEIOI', (0, 9, 12, 6)),
     'HK3': ('ZRKRF VZQHO JZUVV DLBCG KUBJM ISTVG RLMPX GXGEN KQCJL RKJBA QYMGE ZSTZP BPWAL GMJIM JOQDZ YPOIZ JXVQN XURRE DIERI KQJBL UHVQJ', (4, 24, 11, 7)),
    }
    for k, (txt, (l, m, r, i0)) in real.items():
        controls.append((k, ('I', 'II', 'III'), letters(txt)[:N], l, m, r, i0, pbarr(KLPB)))
    txt = open(sorted(glob.glob('../adfgvx/corpus/de_*.txt'))[4], encoding='utf-8', errors='ignore').read()
    conv = lm_build.convert(txt[200000:400000]).upper()
    for j in range(nsyn):
        order = tuple(rng.choice(WNAMES, 3, replace=False))
        rings = ''.join(rng.choice(list(A), 3)); start = ''.join(rng.choice(list(A), 3))
        lett = list(A); rng.shuffle(lett)
        plugs = ' '.join(''.join(sorted(lett[2 * i:2 * i + 2])) for i in range(10))
        p0 = rng.integers(0, len(conv) - N); pt = conv[p0:p0 + N]
        e = Enigma('B', list(order), rings, plugs)
        ct = letters(e.run(pt, start))
        pos = e.step([A.index(c) for c in start])
        l, m, r = [(pos[i] - e.rings[i]) % 26 for i in range(3)]
        i0 = (e.notch[2] - pos[2]) % 26 + 1
        controls.append(('SYN%d' % j, order, ct, l, m, r, i0, pbarr(plugs)))
    return controls


def nplugs_correct(pb, true):
    n = 0
    for a in range(26):
        if pb[a] > a and true[a] == pb[a]: n += 1
    return n
