"""oracle.py - upper bound on what the decoder could read.

For each known-plaintext block, a monotone DP aligns the token sequence to the true letter string,
letting every token emit any unit in its model support (plus the empty string). The score is the number
of true letters covered by a token that can actually produce them. This separates two failure modes:

  oracle high, decode low  -> the search / language model is at fault
  oracle low               -> the transcription or the key is at fault, and no decoder can fix it

usage: python bethune/oracle.py [--model em_model_v2.json] [--minp 0.02] [--wide]
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lm as LMOD
import decode2 as D
sys.stdout.reconfigure(encoding='utf-8')

# visually confusable token families, from the 4x re-reading recorded in NOTES.md
FAMILIES = [
    ['Cm', 'Cu', 'm', 'x'],
    ['g', 'n', 'y', 'q'],
    ['r', 'R2', 'd'],
    ['Z', 'ff', 'EP', '0'],
    ['f', '+', 't'],
    ['h', 'B', 'S', 'l'],
    ['b', 'e', 'c', '6'],
    ['p', 'T', 'o'],
    ['4', '6', 'u'],
    ['v', 'a', '1'],
]


def widen(model, eps=0.25):
    """add each token's family partners' units at weight eps"""
    part = {}
    for fam in FAMILIES:
        for t in fam:
            part.setdefault(t, set()).update(x for x in fam if x != t)
    out = {}
    for tok, items in model.items():
        d = {u: p*(1-eps) for u, p in items}
        for q in part.get(tok, ()):
            for u, p in model.get(q, ()):
                d[u] = d.get(u, 0.0) + eps*p/max(1, len(part.get(tok, ())))
        out[tok] = sorted(d.items(), key=lambda kv: -kv[1])[:10]
    return out


def units_of(tok, model):
    if tok in D.FIXED:   return {D.FIXED[tok]}
    if tok in D.PARTIAL: return {D.PARTIAL[tok]}
    if tok in model:     return set(u for u, p in model[tok]) | {''}
    return set(D.LETTERS) | {''}


def oracle(tokens, truth, model):
    """max letters of truth emitted by a monotone assignment of units to tokens"""
    toks = [tokens[i-1] if (t == 'PH' and i > 0) else t for i, t in enumerate(tokens)]
    us = [units_of(t, model) for t in toks]
    n, m = len(toks), len(truth)
    NEG = -10**9
    prev = [0]*(m+1)                      # dp over letters consumed, tokens 0
    for i in range(1, m+1):
        prev[i] = NEG                     # cannot consume letters with no tokens
    for k in range(n):
        cur = [NEG]*(m+1)
        for j in range(m+1):
            if prev[j] == NEG:
                continue
            if cur[j] < prev[j]:
                cur[j] = prev[j]          # token emits nothing
            for u in us[k]:
                if not u:
                    continue
                L = len(u)
                if j+L <= m:
                    gain = sum(1 for a, b in zip(u, truth[j:j+L]) if a == b)
                    if prev[j]+gain > cur[j+L]:
                        cur[j+L] = prev[j]+gain
        prev = cur
    return max(x for x in prev if x > NEG)


def main():
    model_path = sys.argv[sys.argv.index('--model')+1] if '--model' in sys.argv else 'bethune/em_model_v2.json'
    if '--minp' in sys.argv:
        D.MINP = float(sys.argv[sys.argv.index('--minp')+1])
    model = D.load_model(model_path)
    if '--wide' in sys.argv:
        model = widen(model)
    tot = totn = 0
    for line in open('bethune/corpus_v2.txt', encoding='utf-8'):
        if line.startswith('#') or '|' not in line:
            continue
        p = [x.strip() for x in line.split('|')]
        lab, ct = p[0], p[2]
        truth = LMOD.norm_keep_spaces(p[3]).replace(' ', '')
        g = oracle(ct.split(), truth, model)
        tot += g; totn += len(truth)
        print('%-3s oracle %3d/%3d = %5.1f%%' % (lab, g, len(truth), 100.0*g/len(truth)))
    print('\nORACLE TOTAL %d/%d = %.1f%%  [minp %.3f%s]' %
          (tot, totn, 100.0*tot/totn, D.MINP, ', widened' if '--wide' in sys.argv else ''))


main()
