"""Recover a key from an imperfect crib by alternating two steps, EM-style:
   (1) align the current decode to the crib with an edit-distance DP that tolerates the gaps in
       both (my dropped figures, the crib's words lost in the binding);
   (2) re-estimate each figure's letter from whatever it aligned to.
Neither step needs the crib to be complete or the transcription perfect.
   python cribem.py <cipher.txt> <crib.txt> [rounds]"""
import sys, re, collections, random
toks = [t for t in open(sys.argv[1], encoding='utf-8').read().split() if not re.fullmatch(r'\d+', t)]
crib = re.sub(r'[^a-z]', '', open(sys.argv[2], encoding='utf-8').read().lower().replace('v', 'u').replace('j', 'i'))
rounds = int(sys.argv[3]) if len(sys.argv) > 3 else 25
AL = 'abcdefghilmnopqrstuxyz'
syms = [s for s, _ in collections.Counter(toks).most_common()]
random.seed(0)
import os, json
m = {s: random.choice(AL) for s in syms}
if os.environ.get('SEEDKEY'):                      # start from a related cipher's key
    k = json.load(open(os.environ['SEEDKEY']))
    for s in syms:
        if s in k and len(k[s][0]) == 1: m[s] = k[s][0]
if os.environ.get('SEEDMAP'):                      # or from a map printed by cribfit
    for p in open(os.environ['SEEDMAP'], encoding='utf-8').read().split():
        if '=' in p:
            a, b = p.split('=', 1)
            if a in syms and b and b[0] in AL: m[a] = b[0]
def align(dec, crib):
    """Needleman-Wunsch; returns pairs (index in dec, char in crib)."""
    n, k = len(dec), len(crib)
    GAP = -1.0
    prev = [GAP*j for j in range(k+1)]
    back = [[0]*(k+1) for _ in range(n+1)]
    for j in range(k+1): back[0][j] = 1
    for i in range(1, n+1):
        curr = [GAP*i] + [0.0]*k
        back[i][0] = 2
        ci = dec[i-1]
        for j in range(1, k+1):
            d = prev[j-1] + (2.0 if ci == crib[j-1] else -1.0)
            u = prev[j] + GAP
            l = curr[j-1] + GAP
            if d >= u and d >= l: curr[j], back[i][j] = d, 0
            elif u >= l: curr[j], back[i][j] = u, 2
            else: curr[j], back[i][j] = l, 1
        prev = curr
    i, j, pairs = n, k, []
    while i > 0 or j > 0:
        b = back[i][j]
        if b == 0 and i > 0 and j > 0: pairs.append((i-1, crib[j-1])); i -= 1; j -= 1
        elif b == 2 and i > 0: i -= 1
        else: j -= 1
    return pairs[::-1], prev[k]
best = None
for rd in range(rounds):
    dec = ''.join(m[t] for t in toks)
    pairs, sc = align(dec, crib)
    votes = collections.defaultdict(collections.Counter)
    for i, ch in pairs: votes[toks[i]][ch] += 1
    agree = sum(1 for i, ch in pairs if m[toks[i]] == ch)
    if best is None or sc > best[0]:
        best = (sc, dict(m), agree, len(pairs))
    new = dict(m)
    for s, c in votes.items():
        if c: new[s] = c.most_common(1)[0][0]
    if new == m: break
    m = new
sc, m, agree, np = best
dec = ''.join(m[t] for t in toks)
pairs, _ = align(dec, crib)
agree = sum(1 for i, ch in pairs if m[toks[i]] == ch)
print(f'alignment score {sc:.1f}; {agree}/{len(pairs)} aligned positions agree ({100*agree/max(1,len(pairs)):.0f}%)')
print('decode:', dec[:400])
print()
print('map:', ' '.join(f'{s}={m[s]}' for s in syms))
import os
if os.environ.get('OUTMAP'):
    open(os.environ['OUTMAP'],'w').write(' '.join(f'{s}={m[s]}' for s in syms))
