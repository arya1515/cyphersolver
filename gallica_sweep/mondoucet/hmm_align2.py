# Soft-EM alignment for a homophonic substitution WITH word-signs and nulls: a token may consume 0 letters (null,
# one global rate), 1 letter (emission learned by EM) or k=2..MAXK letters (a word-sign; flat emission, per-token
# code weight learned). Start anywhere in the first START letters; end anywhere. Banded positional initialisation
# and sharpening. This is the version validated on the control (56/58 letter symbols, 7/10 word-codes); a variant
# with a learned per-symbol null rate collapsed to all-null on the same control and was discarded (17 Sept 2026).
import sys, re, unicodedata, collections, json
import numpy as np
from hmm_align import load_tokens, load_pt


def run(T, P, iters=20, START=80, p_null=0.07, p_code=0.012, MAXK=10, verbose=True, band=25, sharpen=2.0, code_em=None):
    types = sorted(set(T)); tix = {t: i for i, t in enumerate(types)}
    letters = sorted(set(P)); lix = {c: i for i, c in enumerate(letters)}
    n, m, K, L = len(T), len(P), len(types), len(letters)
    Tn = np.array([tix[t] for t in T]); Pn = np.array([lix[c] for c in P])
    E = np.full((K, L), 0.5); ratio = m / n
    for i in range(n):
        c = i * ratio; lo, hi = int(max(0, c - band)), int(min(m, c + band + 1))
        w = np.exp(-((np.arange(lo, hi) - c) / (band / 2.0)) ** 2); np.add.at(E[Tn[i]], Pn[lo:hi], w)
    E = E / E.sum(axis=1, keepdims=True)
    p1 = 1 - p_null - p_code * (MAXK - 1)
    if code_em is None:
        code_em = 1.0 / L
    codew = np.full(K, 0.5)
    for it in range(iters):
        alpha = np.zeros((n, m + 1)); scale = np.zeros(n)
        init = np.zeros(m + 1); init[0:START + 1] = 1.0 / (START + 1)

        def step(prev, i):
            em = E[Tn[i]][Pn]; cw = codew[Tn[i]]
            a = np.zeros(m + 1)
            a[1:] += prev[:-1] * p1 * em * (1 - cw + 1e-9) * 2
            for k in range(2, MAXK + 1):
                a[k:] += prev[:-k] * p_code * code_em * cw * 2
            a += prev * p_null
            return a
        a = step(init, 0); scale[0] = a.sum(); alpha[0] = a / scale[0]
        for i in range(1, n):
            a = step(alpha[i - 1], i); scale[i] = a.sum() + 1e-300; alpha[i] = a / scale[i]
        beta = np.zeros((n, m + 1)); beta[n - 1] = 1.0
        for i in range(n - 2, -1, -1):
            nxt = beta[i + 1]; em = E[Tn[i + 1]][Pn]; cw = codew[Tn[i + 1]]
            b = np.zeros(m + 1)
            b[:-1] += nxt[1:] * p1 * em * (1 - cw + 1e-9) * 2
            for k in range(2, MAXK + 1):
                b[:-k] += nxt[k:] * p_code * code_em * cw * 2
            b += nxt * p_null
            beta[i] = b / (b.sum() + 1e-300)
        C = np.zeros((K, L)); codemass = np.zeros(K); lettermass = np.zeros(K); nullmass = 0.0
        for i in range(n):
            prev = init if i == 0 else alpha[i - 1]
            em = E[Tn[i]][Pn]; cw = codew[Tn[i]]
            pm = prev[:-1] * p1 * em * (1 - cw + 1e-9) * 2 * beta[i][1:]
            pc = 0.0
            for k in range(2, MAXK + 1):
                pc += (prev[:-k] * p_code * code_em * cw * 2 * beta[i][k:]).sum()
            pn = (prev * p_null * beta[i]).sum()
            z = pm.sum() + pc + pn + 1e-300
            np.add.at(C[Tn[i]], Pn, pm / z); lettermass[Tn[i]] += pm.sum() / z; codemass[Tn[i]] += pc / z; nullmass += pn / z
        E = (C + 0.02) / (C + 0.02).sum(axis=1, keepdims=True)
        if it < iters - 3:
            E = E ** sharpen; E = E / E.sum(axis=1, keepdims=True)
        codew = (codemass + 0.2) / (codemass + lettermass + 0.4)
        if verbose:
            print('iter %d loglik %.1f letters %.0f codes %.0f nulls %.0f' % (it, np.log(scale).sum(), lettermass.sum(), codemass.sum(), nullmass), flush=True)
    key = {}
    for t in types:
        row = C[tix[t]]; tot = row.sum()
        if tot + codemass[tix[t]] > 0.5:
            b = np.argsort(-row)[:3]
            key[t] = {'letter': letters[b[0]], 'share': float(row[b[0]] / max(tot, 1e-9)), 'n_letter': float(tot), 'n_code': float(codemass[tix[t]]),
                      'alt': [(letters[x], round(float(row[x] / max(tot, 1e-9)), 2)) for x in b[1:]]}
    return key, E, C, lettermass, codemass


if __name__ == '__main__':
    T = load_tokens(sys.argv[1]); P = load_pt(sys.argv[2])
    iters = int(sys.argv[3]) if len(sys.argv) > 3 else 20; START = int(sys.argv[4]) if len(sys.argv) > 4 else 80
    print('tokens', len(T), 'types', len(set(T)), 'letters', len(P))
    key, E, C, lm, cm = run(T, P, iters, START)
    inv = collections.defaultdict(list)
    for t, k in sorted(key.items(), key=lambda kv: -(kv[1]['n_letter'] + kv[1]['n_code'])):
        print('%-5s %7.1f %6.1f  %s %.2f %s' % (t, k['n_letter'], k['n_code'], k['letter'], k['share'], k['alt']))
        if k['n_letter'] > k['n_code']:
            inv[k['letter']].append((t, int(k['n_letter'])))
    for c in sorted(inv):
        print(c, ' '.join('%s(%d)' % x for x in sorted(inv[c], key=lambda x: -x[1])))
    json.dump(key, open('key_hmm2.json', 'w'))
