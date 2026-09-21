"""Test whether the Italian note under the R118 cipher is its decipherment: beam-search a tokenisation
of the digit string (tokens of 1-2 symbols, X = the barred 4) aligned letter by letter with the note,
keeping the token->letter map functional and minimising the number of distinct tokens."""
import sys
C = "2070530740244208X15240434X03070302056024380X90106073032440X703210903550" \
    "40962450038042960505056094005303243060056009246112424456662491124207053106" + "0"
P = sys.argv[1] if len(sys.argv) > 1 else "ilnuntiohatrattatocolsignorperezttuttoquellochevsillmascrive"
beam = [(0, 0, {}, [])]  # (ci, pi, map, path)
for step in range(len(P)):
    nb = []
    for ci, pi, m, path in beam:
        for L in (1, 2, 3):
            t = C[ci:ci+L]
            if len(t) < L: continue
            if t in m and m[t] != P[pi]: continue
            m2 = dict(m); m2[t] = P[pi]
            nb.append((ci+L, pi+1, m2, path+[t]))
    nb.sort(key=lambda s: (len(s[2]) - 0.001*s[0]))
    beam = nb[:4000]
b = beam[0]
print(len(b[2]), 'distinct tokens for', len(P), 'letters; cipher used', b[0], '/', len(C))
print(' '.join('%s=%s' % (t, P[i]) for i, t in enumerate(b[3])))
