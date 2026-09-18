"""union.py - what two independent readings of the same line are worth together.

Reader A is the second pass's transcription, reader B a fresh reading of the same ink at full
resolution. The two are aligned to each other by edit distance; where they agree the token is taken as
read, where they disagree BOTH tokens' emissions are offered to the decoder. That is targeted widening
- only at the positions two careful readers actually differ - as against the blanket confusion widening
that was measured worse.

Reports the oracle bound (how many true letters each reading, and the union, could possibly produce).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lm as LMOD, decode2 as D, oracle as O
sys.stdout.reconfigure(encoding='utf-8')


def align(a, b):
    """token-level alignment; returns list of (tok_a|None, tok_b|None)"""
    n, m = len(a), len(b)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1):
        dp[i][0] = i
    for j in range(m+1):
        dp[0][j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1] + (a[i-1] != b[j-1]))
    out = []
    i, j = n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and dp[i][j] == dp[i-1][j-1] + (a[i-1] != b[j-1]):
            out.append((a[i-1], b[j-1])); i -= 1; j -= 1
        elif i > 0 and dp[i][j] == dp[i-1][j]+1:
            out.append((a[i-1], None)); i -= 1
        else:
            out.append((None, b[j-1])); j -= 1
    return out[::-1]


def union_units(pair, model):
    ua = O.units_of(pair[0], model) if pair[0] else {''}
    ub = O.units_of(pair[1], model) if pair[1] else {''}
    return ua | ub


def oracle_pairs(pairs, truth, model):
    us = [union_units(p, model) for p in pairs]
    n, m = len(us), len(truth)
    NEG = -10**9
    prev = [0] + [NEG]*m
    for k in range(n):
        cur = [NEG]*(m+1)
        for j in range(m+1):
            if prev[j] == NEG:
                continue
            if cur[j] < prev[j]:
                cur[j] = prev[j]
            for u in us[k]:
                if not u:
                    continue
                L = len(u)
                if j+L <= m:
                    g = sum(1 for x, y in zip(u, truth[j:j+L]) if x == y)
                    if prev[j]+g > cur[j+L]:
                        cur[j+L] = prev[j]+g
        prev = cur
    return max(x for x in prev if x > NEG)


def main():
    model = D.load_model('bethune/em_model_v2.json')
    lab = sys.argv[1]
    b_toks = open(sys.argv[2], encoding='utf-8').read().split()
    a_toks = truth = None
    for line in open('bethune/corpus_v2.txt', encoding='utf-8'):
        if line.startswith(lab + ' |'):
            p = [x.strip() for x in line.split('|')]
            a_toks = p[2].split()
            truth = LMOD.norm_keep_spaces(p[3]).replace(' ', '')
    a_toks = [a_toks[i-1] if (t == 'PH' and i > 0) else t for i, t in enumerate(a_toks)]
    b_toks = [b_toks[i-1] if (t == 'PH' and i > 0) else t for i, t in enumerate(b_toks)]
    pairs = align(a_toks, b_toks)
    agree = sum(1 for x, y in pairs if x == y)
    oa = O.oracle(a_toks, truth, model)
    ob = O.oracle(b_toks, truth, model)
    ou = oracle_pairs(pairs, truth, model)
    print('block %s   %d letters' % (lab, len(truth)))
    print('  reader A (2nd pass) %3d tokens   oracle %3d = %5.1f%%' % (len(a_toks), oa, 100.0*oa/len(truth)))
    print('  reader B (this pass) %3d tokens  oracle %3d = %5.1f%%' % (len(b_toks), ob, 100.0*ob/len(truth)))
    print('  aligned %3d positions, agree on %d (%.0f%%)' % (len(pairs), agree, 100.0*agree/len(pairs)))
    print('  UNION                            oracle %3d = %5.1f%%' % (ou, 100.0*ou/len(truth)))


main()
