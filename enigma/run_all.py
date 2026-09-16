"""Production search: all 60 wheel orders x 26^3 starts x 26 i0 (x optional left step), UKW B (or C).
Per location: 26 E-Stecker climbs (IC -> bigram at 4 plugs -> trigram at 8 plugs), optional SA runs.
Results per order saved to results/<tag>/<order>.npz (top-K scores and keys); resumable.

usage: python run_all.py TAG N [--kleft k] [--ukw C] [--sa n] [--orders I-II-III,...]
"""
import sys, os, time, argparse, numpy as np
from numba import njit, prange
from solver import *
from climb2 import climb2
from sa import anneal

CT97 = ('HITLU TSUNQ RTLIA BFTQR NUWLQ VNITR SETNQ IPKLM AHEEF DCABC UWORU BSWYA '
        'BGGFD TXCBX DVDUC EZGFB KYILX OWNPQ RTUVS WM')


@njit(cache=True)
def ils(S, ct, N, pb, rounds, mono, bi, tri):
    """Iterated local search: remove 2 random plugs, add 1 random pair, trigram-only re-climb; keep if better."""
    sf3 = np.zeros(1, dtype=np.int64); sm3 = np.full(1, 3, dtype=np.int64)
    best = score_tri(S, ct, pb, N, tri)
    trial = np.empty(26, dtype=np.int64)
    plugged = np.empty(26, dtype=np.int64); free = np.empty(26, dtype=np.int64)
    for r in range(rounds):
        for a in range(26):
            trial[a] = pb[a]
        for rep in range(2):
            npg = 0
            for a in range(26):
                if trial[a] > a:
                    plugged[npg] = a; npg += 1
            if npg == 0:
                break
            a = plugged[np.random.randint(0, npg)]; b = trial[a]
            trial[a] = a; trial[b] = b
        nf = 0
        for a in range(26):
            if trial[a] == a:
                free[nf] = a; nf += 1
        if nf >= 2:
            i = np.random.randint(0, nf); j = np.random.randint(0, nf - 1)
            if j >= i:
                j += 1
            a = free[i]; b = free[j]; trial[a] = b; trial[b] = a
        s = climb2(S, ct, N, trial, sf3, sm3, 0, False, mono, bi, tri)
        if s > best:
            best = s
            for a in range(26):
                pb[a] = trial[a]
    return best


@njit(cache=True)
def best_location(S, ct, N, starts, sf, sm, back_from, mono, bi, tri, nsa, pbout):
    """starts: E-Stecker and N-Stecker start plugboards; then nsa rounds of ILS from the best."""
    best = -1e18
    pb = np.empty(26, dtype=np.int64)
    for k in range(starts.shape[0]):
        for a in range(26):
            pb[a] = starts[k, a]
        s = climb2(S, ct, N, pb, sf, sm, back_from, False, mono, bi, tri)
        if s > best:
            best = s
            for a in range(26):
                pbout[a] = pb[a]
    if nsa > 0:
        s = ils(S, ct, N, pbout, nsa, mono, bi, tri)
        if s > best:
            best = s
    return best


@njit(parallel=True, cache=True)
def search(T, ct, N, i0s, kleft, starts, sf, sm, back_from, mono, bi, tri, nsa, K, out_scores, out_keys):
    for lm in prange(676):
        l = lm // 26; m = lm % 26
        S = np.empty((N, 26), dtype=np.int64)
        pbout = np.empty(26, dtype=np.int64)
        for r in range(26):
            for j in range(i0s.shape[0]):
                i0 = i0s[j]
                if kleft >= 0 and i0 + 26 * kleft + 1 >= N:
                    continue
                make_S(T, l, m, r, i0, kleft, N, S)
                s = best_location(S, ct, N, starts, sf, sm, back_from, mono, bi, tri, nsa, pbout)
                if s > out_scores[lm, K - 1]:
                    pos = K - 1
                    while pos > 0 and out_scores[lm, pos - 1] < s:
                        out_scores[lm, pos] = out_scores[lm, pos - 1]
                        for q in range(31):
                            out_keys[lm, pos, q] = out_keys[lm, pos - 1, q]
                        pos -= 1
                    out_scores[lm, pos] = s
                    out_keys[lm, pos, 0] = l; out_keys[lm, pos, 1] = m; out_keys[lm, pos, 2] = r
                    out_keys[lm, pos, 3] = i0; out_keys[lm, pos, 4] = kleft
                    for q in range(26):
                        out_keys[lm, pos, 5 + q] = pbout[q]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('tag'); ap.add_argument('N', type=int)
    ap.add_argument('--kleft', type=int, default=-1); ap.add_argument('--ukw', default='B')
    ap.add_argument('--sa', type=int, default=0); ap.add_argument('--orders', default='')
    ap.add_argument('--K', type=int, default=40); ap.add_argument('--ct', default=CT97)
    ap.add_argument('--skip', type=int, default=0, help='drop this many leading letters')
    ap.add_argument('--nstarts', type=int, default=1, help='add the 25 N-Stecker starts')
    ap.add_argument('--threads', type=int, default=20)
    a = ap.parse_args()
    import numba; numba.set_num_threads(a.threads)
    np.random.seed(12345)
    ct = letters(a.ct)[a.skip:a.skip + a.N]
    N = len(ct)
    mono = np.load('mono_logp.npy'); bi = np.load('bi_logp.npy'); tri = np.load('tri_logp.npy')
    sf = np.array([0, 4, 8]); sm = np.array([0, 2, 3])
    starts = e_stecker_starts()
    if a.nstarts:
        nst = np.tile(np.arange(26), (25, 1)); n_ = A.index('N'); j = 0
        for k in range(26):
            if k != n_:
                nst[j, n_] = k; nst[j, k] = n_; j += 1
        starts = np.vstack([starts, nst.astype(np.int64)])
    i0s = np.arange(1, 27, dtype=np.int64)
    orders = [tuple(o.split('-')) for o in a.orders.split(',')] if a.orders else ORDERS
    outdir = os.path.join('results', a.tag); os.makedirs(outdir, exist_ok=True)
    log = open(os.path.join(outdir, 'log.txt'), 'a')
    print('N=%d ct=%s' % (N, ''.join(A[i] for i in ct)), file=log, flush=True)
    for order in orders:
        fn = os.path.join(outdir, '-'.join(order) + '.npz')
        if os.path.exists(fn): continue
        t = time.time()
        T = build_table(order, a.ukw)
        out_scores = np.full((676, a.K), -np.inf); out_keys = np.zeros((676, a.K, 31), dtype=np.int64)
        search(T, ct, N, i0s, a.kleft, starts, sf, sm, 5, mono, bi, tri, a.sa, a.K, out_scores, out_keys)
        sc_ = out_scores.reshape(-1); ke = out_keys.reshape(-1, 31)
        idx = np.argsort(-sc_)[:a.K]
        np.savez(fn, scores=sc_[idx], keys=ke[idx])
        msg = '%s %s done in %.0fs; top %.1f %s | %s' % (time.strftime('%H:%M:%S'), '-'.join(order), time.time() - t, sc_[idx[0]],
                                                     fmt_key(order, ke[idx[0]]), decrypt_key(order, ct, ke[idx[0]], a.ukw))
        print(msg, file=log, flush=True); print(msg, flush=True)


if __name__ == '__main__':
    main()
