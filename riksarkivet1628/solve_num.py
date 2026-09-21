"""Homophonic / simple-substitution annealer for the numeric Riksarkivet items.

usage: python solve_num.py <transcription.txt> <model> [restarts] [fix=34:e,42:n]
Tokens are whitespace-separated; '?' suffixes are dropped, '??' and [..] are skipped.
Each distinct number maps freely to one letter (homophonic allowed); the score is the model's
log-probability of the spaceless decryption.
"""
import os, sys, re, random, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from lang import lm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qg


def load_tokens(path, keep_lines=False):
    lines = []
    for ln in open(path, encoding='utf8'):
        if ln.startswith('#') or not ln.strip():
            continue
        if ln.startswith('## '):
            lines.append(None)
            continue
        ln = re.sub(r'\[[^\]]*\]', ' | ', ln)
        toks = []
        for t in ln.split():
            if t == '|':
                toks.append('|')
                continue
            t = t.rstrip('?^')
            if t and t.isdigit():
                toks.append(t)
        lines.append(toks)
    return lines if keep_lines else [t for l in lines if l for t in l if t != '|']


def solve(tokens, model, restarts=6, iters=int(os.environ.get("ITERS","60000")), fixed=None, seed=1):
    lp = qg.table(model[:2])
    alpha = 'abcdefghiklmnopqrstuxyz' if 'la' not in model else 'abcdefghilmnopqrstux'
    LET = lambda t: 30 <= int(t) <= 59 if os.environ.get('CODEBREAK') else True
    segs, cur_ = [], []
    for t in tokens:
        if t == '|':
            if cur_: segs.append(cur_)
            cur_ = []
        elif LET(t): cur_.append(t)
        else:
            if cur_: segs.append(cur_)
            cur_ = []
    if cur_: segs.append(cur_)
    tokens = [t for t in tokens if LET(t)]
    syms = sorted(set(tokens), key=lambda s: -tokens.count(s))
    idx = {s: i for i, s in enumerate(syms)}
    seq = [idx[t] for t in tokens]
    fixed = fixed or {}
    rnd = random.Random(seed)
    best_all = (-1e18, None)
    freq = {'nl': 'enatirodslguhkmbpczfxy', 'de': 'enirstadhulgcmobfkzpuyx',
            'la': 'eiutasrnomclpdqbgfhx', 'fr': 'esainrtoulcdmpqfhbgxyz', 'sv': 'eantrslidogkmhfupbcxyz', 'en': 'etaoinshrdlucmfygpbkx', 'it': 'eaionlrtscdupmghfbqzx', 'es': 'eaosnrildtucmpbhqyfgxz', 'pt': 'aeosrinmdtucpulqhbfgxz', 'da': 'erntidalgoskmfuhbpcyx'}[model[:2]]
    counts = [tokens.count(s) for s in syms]
    for r in range(restarts):
        pool = list(alpha); rnd.shuffle(pool)
        key = [freq[i] if i < len(freq) else pool[i % len(pool)] for i in range(len(syms))] if not os.environ.get('HOMO') else [rnd.choice(freq[:14]) for _ in syms]
        rnd.shuffle(key[:0])
        for _ in range(r * 3):
            a, b = rnd.randrange(len(syms)), rnd.randrange(len(syms)); key[a], key[b] = key[b], key[a]
        for s, c in fixed.items():
            if s in idx:
                key[idx[s]] = c
        sidx = [[idx[t] for t in g] for g in segs]
        uni = __import__('numpy').exp(0)*0
        import numpy as _np
        if not hasattr(solve, 'U'):
            solve.U = {}
        if model[:2] not in solve.U:
            txt = qg.norm(open(os.path.join(qg.CORP, model[:2] + '-gutenberg.txt'), encoding='utf8', errors='ignore').read()[:2000000])
            solve.U[model[:2]] = _np.bincount(qg.encode(txt), minlength=len(qg.A)) / len(txt)
        P = solve.U[model[:2]]
        cnts = _np.array(counts, dtype=float)
        W = float(os.environ.get('UNIW', '0'))
        def score(k):
            pen = 0.0
            if W:
                f = _np.zeros(len(qg.A))
                _np.add.at(f, [qg.IDX[c] for c in k], cnts)
                f /= f.sum()
                pen = W * len(tokens) * _np.abs(f - P).sum()
            return -pen + sum(qg.score(lp, qg.encode(''.join(k[i] for i in g))) for g in sidx)
        cur = score(key)
        for it in range(iters):
            T = max(0.05, 2.0 * (1 - it / iters))
            a = rnd.randrange(len(syms))
            if syms[a] in fixed:
                continue
            old = key[:]
            if os.environ.get('HOMO') or False:
                key[a] = rnd.choice(alpha)
            else:
                b = rnd.randrange(len(syms))
                if syms[b] in fixed:
                    continue
                key[a], key[b] = key[b], key[a]
            new = score(key)
            if new >= cur or rnd.random() < math.exp((new - cur) / T):
                cur = new
            else:
                key = old
        print(f'restart {r}: {cur/len(seq):.3f}', ''.join(key[i] for i in seq)[:120], flush=True)
        if cur > best_all[0]:
            best_all = (cur, dict(zip(syms, key)))
    return best_all


if __name__ == '__main__':
    path, model = sys.argv[1], sys.argv[2]
    restarts = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    fixed = {}
    if len(sys.argv) > 4:
        for kv in sys.argv[4].split(','):
            a, b = kv.split(':'); fixed[a] = b
    toks = [t for l in load_tokens(path, keep_lines=True) if l for t in l + ['|']]
    sc, key = solve(toks, model, restarts, fixed=fixed)
    print('best', sc / len(toks))
    print(' '.join(f'{s}={c}' for s, c in sorted(key.items(), key=lambda x: (len(x[0]), x[0]))))
    for l in load_tokens(path, keep_lines=True):
        if l is None:
            print('--'); continue
        print(''.join(key.get(t, '['+t+']') if t != '|' else ' | ' for t in l))
