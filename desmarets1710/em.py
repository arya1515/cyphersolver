"""EM alignment of the glossed lines of R10198: each figure group emits a contiguous run of the
gloss line's letters (0..MAXL). Learns P(run | group); prints the Viterbi segmentation and the key."""
import re, math, json, collections, sys, unicodedata

MAXL = 9

def norm(s):
    s = unicodedata.normalize('NFD', s)
    return re.sub(r'[^a-z]', '', s.lower().replace('(ent)', 'ent').replace('(ens)', 'ens').replace('(ue)', 'ue'))

def load():
    G, U, g = [], [], None
    for ln in open('desmarets1710/transcription.txt', encoding='utf-8'):
        if ln.startswith('G |'): g = norm(ln[3:])
        elif ln.startswith('C |'): G.append((g, ln[3:].split()))
        elif ln.startswith('U |'): U.append(ln[3:].split('|')[0].split())
    return G, U

def run(G, iters=40):
    P = collections.defaultdict(lambda: collections.defaultdict(lambda: 1.0))
    for it in range(iters):
        C = collections.defaultdict(lambda: collections.defaultdict(float))
        for text, gs in G:
            n, m = len(text), len(gs)
            def e(k, i, j):
                d = P[gs[k]]; tot = sum(d.values()) if d else 1
                v = d.get(text[i:j], 0.0) if it else 1.0
                return (v + 1e-3 * 0.2 ** (j - i)) / (tot + 1) * (0.3 if j == i else 1)
            F = [[0.0] * (n + 1) for _ in range(m + 1)]; F[0][0] = 1
            for k in range(m):
                for i in range(n + 1):
                    if F[k][i]:
                        for j in range(i, min(n, i + MAXL) + 1):
                            F[k + 1][j] += F[k][i] * e(k, i, j)
            B = [[0.0] * (n + 1) for _ in range(m + 1)]; B[m][n] = 1
            for k in range(m - 1, -1, -1):
                for i in range(n + 1):
                    B[k][i] = sum(e(k, i, j) * B[k + 1][j] for j in range(i, min(n, i + MAXL) + 1))
            Z = F[m][n]
            if not Z: continue
            for k in range(m):
                for i in range(n + 1):
                    if F[k][i]:
                        for j in range(i, min(n, i + MAXL) + 1):
                            p = F[k][i] * e(k, i, j) * B[k + 1][j] / Z
                            if p > 1e-6: C[gs[k]][text[i:j]] += p
        P = collections.defaultdict(dict, {g: dict(d) for g, d in C.items()})
    return P

def viterbi(P, text, gs):
    n, m = len(text), len(gs)
    V = [[(-1e18, None)] * (n + 1) for _ in range(m + 1)]; V[0][0] = (0, None)
    for k in range(m):
        d = P.get(gs[k], {}); tot = sum(d.values()) or 1
        for i in range(n + 1):
            if V[k][i][0] > -1e17:
                for j in range(i, min(n, i + MAXL) + 1):
                    s = V[k][i][0] + math.log((d.get(text[i:j], 0) + 1e-4) / tot)
                    if s > V[k + 1][j][0]: V[k + 1][j] = (s, i)
    out, j = [], n
    for k in range(m, 0, -1):
        i = V[k][j][1]; out.append(text[i:j]); j = i
    return out[::-1]

if __name__ == '__main__':
    G, U = load()
    P = run(G)
    key = collections.defaultdict(collections.Counter)
    for text, gs in G:
        seg = viterbi(P, text, gs)
        print(' '.join(f'{g}={s}' for g, s in zip(gs, seg)))
        for g, s in zip(gs, seg): key[g][s] += 1
    json.dump({g: dict(c) for g, c in key.items()}, open('desmarets1710/key_em.json', 'w'), indent=0, sort_keys=True)
