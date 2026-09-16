"""Collect candidates from results/<tag>/*.npz, rank, decrypt, and apply the indicator check.

Indicator check: header `hiq rst` = Grundstellung HIQ (window), enciphered message key RST. A candidate gives the
core positions (l, m, r) at the first letter and i0 (first middle step), hence the right ring: the right window at
letter 0 is w_r = r + ring_r, and the middle steps when the right window passes the notch letter: i0 = (notch - w_r) mod 26
(+26 if 0) -> ring_r = notch - i0 - r (mod 26). The message start window P (before the first step) is core - 1 for the
right wheel: P_r = w_r - 1; P_m = m + ring_m, P_l = l + ring_l (676 unknowns). Requirement: Enigma at window HIQ (rings as
above) enciphers P to RST (indicator encipherment), i.e. decrypting RST at HIQ gives P. Random match probability 1/26.
"""
import sys, glob, os, numpy as np
from solver import *
from enigma_core import Enigma, WHEELS

CT97 = ('HITLU TSUNQ RTLIA BFTQR NUWLQ VNITR SETNQ IPKLM AHEEF DCABC UWORU BSWYA '
        'BGGFD TXCBX DVDUC EZGFB KYILX OWNPQ RTUVS WM')


def plugs_str(pb):
    return ' '.join(A[a] + A[pb[a]] for a in range(26) if pb[a] > a)


def indicator_check(order, key, ukw='B', grund='HIQ', ind='RST'):
    l, m, r, i0, kl = [int(x) for x in key[:5]]
    pb = key[5:]
    notch = A.index(WHEELS[order[2]][1])
    ring_r = (notch - i0 + 1 - r) % 26   # window before keypress i0 shows the notch letter
    wr = (r + ring_r) % 26          # right window at letter 0 (after the first step)
    Pr = (wr - 1) % 26              # message key as set before typing
    hits = []
    for ring_l in range(26):
        for ring_m in range(26):
            e = Enigma(ukw, list(order), A[ring_l] + A[ring_m] + A[ring_r], plugs_str(pb))
            P = e.run(ind, grund)
            if P[2] == A[Pr] and A.index(P[1]) == (m + ring_m) % 26 and A.index(P[0]) == (l + ring_l) % 26:
                hits.append((A[ring_l] + A[ring_m] + A[ring_r], P))
    return hits


def main(tag, ukw='B', top=30):
    ct = letters(CT97)
    rows = []
    for fn in sorted(glob.glob(os.path.join('results', tag, '*.npz'))):
        order = tuple(os.path.basename(fn)[:-4].split('-'))
        d = np.load(fn)
        for s, k in zip(d['scores'], d['keys']):
            rows.append((s, order, k))
    rows.sort(key=lambda x: -x[0])
    N = len(ct)
    print('%d candidates from %d orders; top %d:' % (len(rows), len(set(r[1] for r in rows)), top))
    for s, order, k in rows[:top]:
        pt = decrypt_key(order, ct[:N], k, ukw)
        hits = indicator_check(order, k, ukw)
        print('%8.1f %s %s %s' % (s, fmt_key(order, k), 'IND:' + (','.join(h[0] for h in hits) if hits else '-'), pt))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'B')
