"""Which E-Stecker starts find the solution at the true location? Three real 1945 controls (Huppenkothen
parts 1-3, first 97 letters, same daily key, different message keys)."""
import sys, time, numpy as np
from solver import *

logp = np.load('tri_logp.npy')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 97
parts = {
 1: ('BUQVG DQYEU AUTCD FJFRG LIDWF WBKMH RBWIK OOBRL UBTSL EKDGK GMKDN GCZJV AGRGK TUNAH QDJRT GHYTR YEKSP KGWYQ OMEWN DXCWN XKPGJ', (9, 2, 24, 20)),
 2: ('GDOIH RKODK NYZSJ ILGAO GPCRO ASTKN WIAEZ HDXAH IKZYG SSWXQ SRYCJ EEBGV RCGVK DCPVD WDFJT DBLMB VPJEP TTUEC WNHDD RKNZN QEIOI', (0, 9, 12, 6)),
 3: ('ZRKRF VZQHO JZUVV DLBCG KUBJM ISTVG RLMPX GXGEN KQCJL RKJBA QYMGE ZSTZP BPWAL GMJIM JOQDZ YPOIZ JXVQN XURRE DIERI KQJBL UHVQJ', (4, 24, 11, 7)),
}
order = ('I', 'II', 'III')
pb = np.arange(26)
for pr in 'AM BF CD EK HQ IO LV NT SY WZ'.split():
    a, b = A.index(pr[0]), A.index(pr[1]); pb[a], pb[b] = b, a
T = build_table(order)
starts = e_stecker_starts()
for p, (txt, (l, m, r, i0)) in parts.items():
    ct = letters(txt)[:N]
    S = np.empty((N, 26), dtype=np.int64); make_S(T, l, m, r, i0, -1, N, S)
    out = np.empty(N, dtype=np.int64); decrypt(S, ct, pb, N, out)
    true_s = score_tri(S, ct, pb, N, logp)
    print('part %d true: %.1f %s' % (p, true_s, ''.join(A[i] for i in out)[:60]))
    ok = []
    t = time.time()
    for k in range(26):
        pbk = starts[k].copy()
        s = climb(S, ct, N, pbk, logp, 7, 5)
        if s >= true_s - 1e-6: ok.append(k)
        if k == 0: t0 = time.time() - t
    dt = time.time() - t
    print('   26 starts: %.3fs (%.1f ms/start); successful starts: %s' % (dt, 1000 * dt / 26, ok))
    # empty-start only, tri_from variants
    for tf, bf in ((7, 5), (5, 3), (4, 4), (10, 5), (0, 0)):
        pbk = np.arange(26); s = climb(S, ct, N, pbk, logp, tf, bf)
        print('   empty start tri_from=%d back_from=%d: %.1f' % (tf, bf, s))
