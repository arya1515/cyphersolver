"""Re-anneal the block with candidate null signs removed; prints per-char LM score (real Spanish ~ -1.1)."""
import sys
sys.path.insert(0, 'nino1522'); sys.path.insert(0, '.')
import anneal as A
base = A.CT
for strip in ['', 'H', 'o', 'Ho']:
    A.CT = ' '.join(''.join(c for c in base if c not in strip).split())
    A.SIGNS = sorted(set(A.CT) - {' '})
    best = max((A.run({}, iters=30000, T0=2.0) for _ in range(4)), key=lambda r: r[0])
    n = len(A.CT)
    print(f'strip={strip!r} n={n} per-char={best[0]/n:.2f}')
    print('  ', A.dec(best[1])[:300], flush=True)
