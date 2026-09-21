"""Treat sign+'#' as one symbol (upper-case the base as a new sign) and re-anneal."""
import sys, re
sys.path.insert(0, 'nino1522'); sys.path.insert(0, '.')
import anneal as A
base = A.CT
MAP = {}
def merge(t):
    out = []; i = 0
    while i < len(t):
        if i + 1 < len(t) and t[i + 1] == 'H' and t[i] != ' ':
            sym = MAP.setdefault(t[i] + 'H', chr(0x100 + len(MAP)))
            out.append(sym); i += 2
        else:
            out.append(t[i]); i += 1
    return ''.join(out)
for strip in ['', 'o']:
    A.CT = ' '.join(''.join(c for c in merge(base) if c not in strip).split())
    A.SIGNS = sorted(set(A.CT) - {' '})
    best = max((A.run({}, iters=40000, T0=2.0) for _ in range(5)), key=lambda r: r[0])
    print(f'strip={strip!r} signs={len(A.SIGNS)} per-char={best[0]/len(A.CT):.2f}')
    print('  ', A.dec(best[1])[:400], flush=True)
