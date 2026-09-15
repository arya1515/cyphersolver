"""segem.py -- unsupervised unit segmentation by unigram EM over units of 1..MAXL digits.

The null 4 splits the stream into segments. Dots are ignored for the segmentation itself and then
analysed against the recovered unit boundaries (dot on a unit's last digit = 'dot on the antecedent';
dot on a unit's first digit = a dotted code).

usage: python segem.py [MAXL=2] [ALPHA=0.05] [PRUNE=2] [--runs file.json]
"""
import sys, math, json, collections

NULL = '4'

def load_runs(path=None):
    """Runs of digit tokens ('7', '7^.', ...). Real cipher from parse5, or a JSON list of runs."""
    if path:
        return json.load(open(path))
    from parse5 import load, digit_stream
    return digit_stream(load())

def segments_from_runs(runs):
    """Split at the null; return list of segments, each a list of (digit, dotted)."""
    segs = []
    for r in runs:
        cur = []
        for t in r:
            d = t[0]; dotted = ('^' in t)
            if d == NULL:
                if cur: segs.append(cur)
                cur = []
            else:
                cur.append((d, dotted))
        if cur: segs.append(cur)
    return segs

def digamma(x):
    r = 0.0
    while x < 6: r -= 1.0/x; x += 1
    return r + math.log(x) - 1/(2*x) - 1/(12*x*x) + 1/(120*x**4) - 1/(252*x**6)

def forward_backward(s, p, MAXL):
    n = len(s)
    a = [0.0]*(n+1); a[0] = 1.0
    for i in range(1, n+1):
        v = 0.0
        for L in range(1, MAXL+1):
            if i-L >= 0:
                pu = p.get(s[i-L:i])
                if pu: v += a[i-L]*pu
        a[i] = v
    b = [0.0]*(n+1); b[n] = 1.0
    for i in range(n-1, -1, -1):
        v = 0.0
        for L in range(1, MAXL+1):
            if i+L <= n:
                pu = p.get(s[i:i+L])
                if pu: v += pu*b[i+L]
        b[i] = v
    return a, b

def em(strs, MAXL=2, ALPHA=0.05, PRUNE=2.0, ITERS=60, verbose=True):
    ndig = sum(len(s) for s in strs)
    cnt = collections.Counter()
    for s in strs:
        for i in range(len(s)):
            for L in range(1, MAXL+1):
                if i+L <= len(s): cnt[s[i:i+L]] += 1.0/L
    tot = sum(cnt.values()); p = {u: c/tot for u, c in cnt.items()}
    for it in range(ITERS):
        exp = collections.Counter(); ll = 0.0
        for s in strs:
            a, b = forward_backward(s, p, MAXL)
            Z = a[len(s)]
            if Z <= 0: continue
            ll += math.log(Z)
            for i in range(len(s)):
                for L in range(1, MAXL+1):
                    if i+L <= len(s):
                        u = s[i:i+L]; pu = p.get(u)
                        if pu: exp[u] += a[i]*pu*b[i+L]/Z
        keep = {u: c for u, c in exp.items() if c >= PRUNE or len(u) == 1}
        K = len(keep); T = sum(keep.values())
        denom = digamma(T + ALPHA*K)
        p = {u: math.exp(digamma(c + ALPHA) - denom) for u, c in keep.items()}
        if verbose and (it % 10 == 0 or it == ITERS-1):
            print(f'iter {it:2d} loglik {ll:10.1f}  types {K:4d}  tokens {sum(keep.values()):7.1f}  bits/digit {-ll/math.log(2)/ndig:.3f}')
    return p

def viterbi(s, p, MAXL):
    n = len(s); best = [-1e300]*(n+1); back = [0]*(n+1); best[0] = 0.0
    for i in range(1, n+1):
        for L in range(1, MAXL+1):
            if i-L >= 0:
                pu = p.get(s[i-L:i])
                if pu and best[i-L] + math.log(pu) > best[i]:
                    best[i] = best[i-L] + math.log(pu); back[i] = L
    out = []; i = n
    while i > 0: out.append(s[i-back[i]:i]); i -= back[i]
    return out[::-1]

def segment(runs, MAXL=2, ALPHA=0.05, PRUNE=2.0, ITERS=60, verbose=True):
    """Return (segs, tokens): segs = list of [(digit, dotted)], tokens = list of [(unit, dotted_any)]."""
    segs = segments_from_runs(runs)
    strs = [''.join(d for d, _ in s) for s in segs]
    if verbose: print(f'{len(strs)} segments, {sum(len(s) for s in strs)} non-null digits')
    p = em(strs, MAXL, ALPHA, PRUNE, ITERS, verbose)
    tokens = []
    for seg, s in zip(segs, strs):
        units = viterbi(s, p, MAXL); i = 0; toks = []
        for u in units:
            dotted = any(seg[i+j][1] for j in range(len(u)))
            toks.append((u, dotted)); i += len(u)
        tokens.append(toks)
    return segs, tokens

def report(segs, tokens):
    ndig = sum(len(s) for s in segs)
    ucount = collections.Counter(u for t in tokens for u, _ in t)
    ntok = sum(ucount.values())
    print(f'\nViterbi: {ntok} tokens, {len(ucount)} types, mean unit length {ndig/ntok:.2f}')
    print('tokens by unit length', dict(collections.Counter(len(u) for u in ucount.elements())))
    print('\nunit inventory:'); print(' '.join(f'{u}:{c}' for u, c in ucount.most_common()))
    fin = collections.Counter(t[-1][0] for t in tokens); ini = collections.Counter(t[0][0] for t in tokens)
    print('\nsegment-final units:', fin.most_common(25))
    print('segment-initial units:', ini.most_common(25))
    print('\nfinal/initial enrichment for units with >= 40 tokens:')
    for u, c in ucount.most_common():
        if c < 40: break
        print(f'  {u:>3} {c:4d}  final {fin[u]:3d}  enr {(fin[u]/len(tokens))/(c/ntok):.2f}   initial {ini[u]:3d}  enr {(ini[u]/len(tokens))/(c/ntok):.2f}')
    pos = collections.Counter(); dotted_units = collections.Counter(); after = collections.Counter()
    for seg, toks in zip(segs, tokens):
        i = 0
        for k, (u, _) in enumerate(toks):
            for j in range(len(u)):
                if seg[i+j][1]:
                    pos['single' if len(u) == 1 else ('first' if j == 0 else ('last' if j == len(u)-1 else 'middle'))] += 1
                    dotted_units[(u, j)] += 1
                    if j == len(u)-1 and k+1 < len(toks): after[toks[k+1][0]] += 1
            i += len(u)
    print('\ndot position within unit:', dict(pos))
    print('dotted (unit, position):', dotted_units.most_common(30))
    print('unit following a unit whose LAST digit is dotted:', after.most_common(20))
    big = collections.Counter()
    for t in tokens:
        for (a, _), (b, _) in zip(t, t[1:]): big[(a, b)] += 1
    print('\ntop unit bigrams:', [(a+'|'+b, c) for (a, b), c in big.most_common(40)])

if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--') and not a.endswith('.json')]
    runs_file = None
    if '--runs' in sys.argv: runs_file = sys.argv[sys.argv.index('--runs')+1]
    MAXL = int(args[0]) if len(args) > 0 else 2
    ALPHA = float(args[1]) if len(args) > 1 else 0.05
    PRUNE = float(args[2]) if len(args) > 2 else 2.0
    runs = load_runs(runs_file)
    segs, tokens = segment(runs, MAXL, ALPHA, PRUNE)
    report(segs, tokens)
