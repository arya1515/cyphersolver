# Soft-EM (forward-backward) alignment of a cipher token sequence to a known plaintext for a homophonic
# substitution with nulls and occasional skipped letters. Hidden state = plaintext position after emitting token i.
# Transitions: advance 1 (match), stay (null token), advance 2 (letter skipped / word-sign). Start anywhere in the
# first START positions. Emissions P(token | letter) learned by EM from a flat start; the monotone structure plus
# the plaintext itself carries the signal, so no hard collapse.
# usage: python hmm_align.py tokens.txt plaintext.txt [iters] [START]
import sys, re, math, unicodedata, collections, json
import numpy as np


def load_tokens(f):
    toks = []
    for l in open(f, encoding='utf-8'):
        if l.startswith('#') or not l.strip():
            continue
        l = re.sub(r'^\S+ \d+: ', '', l.strip()); l = re.sub(r'^\d+[ab]?:\s*', '', l)
        toks += [t for t in l.split() if t != '?']
    return toks


def load_pt(f):
    s = ''.join(l for l in open(f, encoding='utf-8') if not l.startswith('#'))
    s = unicodedata.normalize('NFD', s.lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z]', '', s)


def run(T, P, iters=15, START=80, p_null=0.06, p_skip=0.03, verbose=True, band=25, sharpen=2.0):
    types = sorted(set(T)); tix = {t: i for i, t in enumerate(types)}
    letters = sorted(set(P)); lix = {c: i for i, c in enumerate(letters)}
    n, m, K, L = len(T), len(P), len(types), len(letters)
    Tn = np.array([tix[t] for t in T]); Pn = np.array([lix[c] for c in P])
    # banded positional initialisation: token i co-occurs with letters near i*m/n, gaussian window
    E = np.full((K, L), 0.5)
    ratio = m / n
    for i in range(n):
        c = i * ratio
        lo, hi = int(max(0, c - band)), int(min(m, c + band + 1))
        w = np.exp(-((np.arange(lo, hi) - c) / (band / 2.0)) ** 2)
        np.add.at(E[Tn[i]], Pn[lo:hi], w)
    E = E / E.sum(axis=1, keepdims=True)
    p_match = 1 - p_null - p_skip
    for it in range(iters):
        # emission matrix for each (i, j): token i emitted at letter j -> E[Tn[i], Pn[j]]
        # forward: alpha[i][j] = prob of tokens 0..i with state j after token i (j = letters consumed, 1..m)
        alpha = np.zeros((n, m + 1)); scale = np.zeros(n)
        em0 = E[Tn[0]][Pn]                    # emission of token 0 at letter j (state j+1)
        init = np.zeros(m + 1); init[1:START + 2] = 1.0 / (START + 1)
        # token 0: match from start j -> j+1 ; null: stays at start j (emit null)
        a = np.zeros(m + 1)
        a[1:] += init[:-1] * p_match * em0
        a[2:] += init[:-2] * p_skip * E[Tn[0]][Pn[1:]]
        a += init * p_null
        scale[0] = a.sum(); alpha[0] = a / scale[0]
        for i in range(1, n):
            prev = alpha[i - 1]; em = E[Tn[i]][Pn]
            a = np.zeros(m + 1)
            a[1:] += prev[:-1] * p_match * em
            a[2:] += prev[:-2] * p_skip * em[1:]
            a += prev * p_null
            scale[i] = a.sum() + 1e-300; alpha[i] = a / scale[i]
        # backward
        beta = np.zeros((n, m + 1)); beta[n - 1] = 1.0
        for i in range(n - 2, -1, -1):
            nxt = beta[i + 1]; em = E[Tn[i + 1]][Pn]
            b = np.zeros(m + 1)
            b[:-1] += nxt[1:] * p_match * em
            b[:-2] += nxt[2:] * p_skip * em[1:]
            b += nxt * p_null
            beta[i] = b / (b.sum() + 1e-300)
        # expected counts of (token i emitted at letter j) for match transitions
        C = np.zeros((K, L)); nullmass = 0.0
        for i in range(n):
            prev = init if i == 0 else alpha[i - 1]
            em = E[Tn[i]][Pn]
            post_match = prev[:-1] * p_match * em * beta[i][1:]
            post_skip = np.zeros(m); post_skip[1:] = prev[:-2] * p_skip * em[1:] * beta[i][2:]
            post_null = prev * p_null * beta[i]
            z = post_match.sum() + post_skip.sum() + post_null.sum() + 1e-300
            w = (post_match + post_skip) / z
            np.add.at(C[Tn[i]], Pn, w)
            nullmass += post_null.sum() / z
        E = (C + 0.02) / (C + 0.02).sum(axis=1, keepdims=True)
        if it < iters - 3:
            E = E ** sharpen; E = E / E.sum(axis=1, keepdims=True)
        ll = np.log(scale).sum()
        if verbose:
            print('iter %d loglik %.1f expected nulls %.1f' % (it, ll, nullmass), flush=True)
    # Viterbi-ish readout: argmax letter per token type
    key = {}
    for t in types:
        row = C[tix[t]]
        if row.sum() > 0.5:
            best = np.argsort(-row)[:3]
            key[t] = (letters[best[0]], row[best[0]] / row.sum(), row.sum(), [(letters[b], round(row[b] / row.sum(), 2)) for b in best[1:]])
    return key, E, C


if __name__ == '__main__':
    T = load_tokens(sys.argv[1]); P = load_pt(sys.argv[2])
    iters = int(sys.argv[3]) if len(sys.argv) > 3 else 15; START = int(sys.argv[4]) if len(sys.argv) > 4 else 80
    print('tokens', len(T), 'types', len(set(T)), 'letters', len(P))
    key, E, C = run(T, P, iters, START)
    inv = collections.defaultdict(list)
    print('\ntoken  n     letter share  alternatives')
    for t, (c, sh, nn, alt) in sorted(key.items(), key=lambda kv: -kv[1][2]):
        print('%-5s %5.1f  %s %.2f  %s' % (t, nn, c, sh, alt))
        inv[c].append((t, round(nn)))
    print('\nletter -> tokens')
    for c in sorted(inv):
        print(c, ' '.join('%s(%d)' % x for x in sorted(inv[c], key=lambda x: -x[1])))
    json.dump({t: [c, float(sh), float(nn)] for t, (c, sh, nn, alt) in key.items()}, open('key_hmm.json', 'w'))
