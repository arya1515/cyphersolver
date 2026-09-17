# Recover a homophonic key from a cipher transcription and its contemporary decipherment by hard-EM alignment.
# Tokens map to one plaintext letter each; a token may be a null (consumes nothing); a plaintext letter may be
# skipped (covered by a word-sign). usage: python align_key.py ct_c019.txt pt_f9r.txt [iters]
import sys, re, math, collections, json, unicodedata
ct_file, pt_file = sys.argv[1], sys.argv[2]
iters = int(sys.argv[3]) if len(sys.argv) > 3 else 12


def load_ct(f):
    toks = []
    for l in open(f, encoding='utf-8'):
        if l.startswith('#') or not l.strip():
            continue
        l = re.sub(r'^\d+[ab]?:\s*', '', l.strip())
        toks += [t for t in l.split() if t != '?']
    return toks


def load_pt(f):
    s = ''
    for l in open(f, encoding='utf-8'):
        if l.startswith('#'):
            continue
        s += l
    s = unicodedata.normalize('NFD', s.lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    s = re.sub(r'\[\?\]', '', s)
    return re.sub(r'[^a-z]', '', s)


T = load_ct(ct_file); P = load_pt(pt_file)
print('tokens', len(T), 'distinct', len(set(T)), '| plaintext letters', len(P))
letters = sorted(set(P))
# initial emission: uniform
types = sorted(set(T))
emit = {t: {c: 1.0 / len(letters) for c in letters} for t in types}
NULL, SKIP, ENDFREE = -3.5, -3.0, True


def viterbi():
    n, m = len(T), len(P)
    NEG = -1e18
    # dp[i][j]: best score with i tokens and j letters consumed
    dp = [[NEG] * (m + 1) for _ in range(n + 1)]
    bp = [[None] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0.0
    for i in range(n + 1):
        for j in range(m + 1):
            v = dp[i][j]
            if v <= NEG / 2:
                continue
            if i < n and j < m:
                s = v + math.log(emit[T[i]][P[j]])
                if s > dp[i + 1][j + 1]:
                    dp[i + 1][j + 1] = s; bp[i + 1][j + 1] = ('M', i, j)
            if i < n:
                s = v + NULL
                if s > dp[i + 1][j]:
                    dp[i + 1][j] = s; bp[i + 1][j] = ('N', i, j)
            if j < m:
                s = v + SKIP
                if s > dp[i][j + 1]:
                    dp[i][j + 1] = s; bp[i][j + 1] = ('S', i, j)
    # end: all tokens consumed, plaintext may end anywhere (free end) -> pick best j
    jend = max(range(m + 1), key=lambda j: dp[n][j]) if ENDFREE else m
    path = []; i, j = n, jend
    while (i, j) != (0, 0):
        mv, pi, pj = bp[i][j]; path.append((mv, pi, pj)); i, j = pi, pj
    return dp[n][jend], path[::-1], jend


for it in range(iters):
    score, path, jend = viterbi()
    cnt = {t: collections.Counter() for t in types}
    nm = nn = ns = 0
    for mv, i, j in path:
        if mv == 'M':
            cnt[T[i]][P[j]] += 1; nm += 1
        elif mv == 'N':
            nn += 1
        else:
            ns += 1
    alpha = 0.05
    for t in types:
        tot = sum(cnt[t].values())
        emit[t] = {c: (cnt[t][c] + alpha) / (tot + alpha * len(letters)) for c in letters}
    print('iter %d score %.1f matched %d nulls %d skips %d plaintext used %d/%d' % (it, score, nm, nn, ns, jend, len(P)))

# report key
key = {}
print('\n%-6s %5s  %s' % ('token', 'n', 'letter (share)  alternatives'))
for t in sorted(types, key=lambda t: -sum(cnt[t].values())):
    tot = sum(cnt[t].values())
    if tot == 0:
        key[t] = None; continue
    top = cnt[t].most_common(3)
    key[t] = top[0][0]
    print('%-6s %5d  %s (%.2f)  %s' % (t, tot, top[0][0], top[0][1] / tot, ' '.join('%s:%d' % x for x in top[1:])))
json.dump({'key': key, 'counts': {t: dict(cnt[t]) for t in types}}, open('key_1571.json', 'w'), indent=0)
# letter -> tokens
inv = collections.defaultdict(list)
for t, c in key.items():
    if c:
        inv[c].append(t)
print('\nletter -> tokens')
for c in sorted(inv):
    print(c, ' '.join(sorted(inv[c])))
# show alignment as decode
dec = ''.join((key[T[i]] or '?') if mv == 'M' else ('_' if mv == 'N' else '') for mv, i, j in path)
open('align_out.txt', 'w', encoding='utf-8').write(dec + '\n')
print('\ndecode of the cipher with the recovered key (first 600):\n' + dec[:600])
