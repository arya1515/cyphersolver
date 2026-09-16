"""Calibration on the real 1945 Huppenkothen message (first 97 letters, known key)."""
import sys, time, numpy as np
from solver import *

HK = ('BUQVG DQYEU AUTCD FJFRG LIDWF WBKMH RBWIK OOBRL UBTSL EKDGK GMKDN GCZJV '
      'AGRGK TUNAH QDJRT GHYTR YEKSP KGWYQ OMEWN DXCWN XKPGJ GNGSG TQEZW WXUKI DPVCU')
logp = np.load('tri_logp.npy')
N = int(sys.argv[1]) if len(sys.argv) > 1 else 97
ct = letters(HK)[:N]
order = ('I', 'II', 'III')
# window start GLB, rings XJE -> first letter at core J C Y; middle steps at letter 20
pb = np.arange(26)
for pr in 'AM BF CD EK HQ IO LV NT SY WZ'.split():
    a, b = A.index(pr[0]), A.index(pr[1]); pb[a], pb[b] = b, a
key = np.array([9, 2, 24, 20, -1] + list(pb))
print('true key decrypt:', decrypt_key(order, ct, key))
T = build_table(order)
S = np.empty((N, 26), dtype=np.int64)
make_S(T, 9, 2, 24, 20, -1, N, S)
print('true-key trigram score', score_tri(S, ct, pb, N, logp), 'ic', score_ic(S, ct, pb, N))
starts = e_stecker_starts()
pbout = np.empty(26, dtype=np.int64)
t = time.time()
s = best_climb(S, ct, N, starts, logp, 7, 5, pbout)
print('climb at true location: score %.2f  %.3fs' % (s, time.time() - t))
print(fmt_key(order, np.concatenate([[9, 2, 24, 20, -1], pbout])))
out = np.empty(N, dtype=np.int64); decrypt(S, ct, pbout, N, out); print(''.join(A[i] for i in out))
for i0 in (13, 26, 6):
    make_S(T, 9, 2, 24, i0, -1, N, S)
    s = best_climb(S, ct, N, starts, logp, 7, 5, pbout)
    decrypt(S, ct, pbout, N, out)
    print('i0=%d: %.2f %s' % (i0, s, ''.join(A[i] for i in out)))
# timing + ranking over the full order with the right i0
for i0s in ([20], [13, 26]):
    t = time.time()
    scs, keys = run_order(order, ct, i0s, K=20, logp=logp)
    dt = time.time() - t
    print('order run i0s=%s: %.1fs for %d locations (%.2f ms/location)' % (i0s, dt, 17576 * len(i0s), 1000 * dt / (17576 * len(i0s))))
    for j in range(8):
        print('  %.2f %s %s' % (scs[j], fmt_key(order, keys[j]), decrypt_key(order, ct, keys[j])[:50]))
