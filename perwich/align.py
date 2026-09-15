import re, sys
import grid
ABB = {'the': 'ye', 'that': 'yt', 'them': 'ym', 'with': 'wt', 'and': '&'}

def stream():
    s = []
    for r in grid.load():
        for c in r:
            c = grid.norm(c)
            if c: s.append(c.lower() if len(c) == 1 or c.lower() in ('ye','yt','ym','wt') else c)
    return s

def ptoks(abbr):
    words = re.findall(r"[A-Za-z']+|\d+", open('plaintext_tna.txt').read())
    t = []
    for w in words:
        wl = w.lower().replace("'", '')
        if w.isdigit(): t.append(w)
        elif abbr and wl in ABB: t.append(ABB[wl])
        else: t.extend(list(wl))
    return t

def sw(a, b):
    """local alignment of short a inside long b; return (score, start, end)"""
    n, m = len(a), len(b)
    H = [[0]*(m+1) for _ in range(n+1)]
    best = (0, 0, 0)
    for i in range(1, n+1):
        for j in range(1, m+1):
            s = H[i-1][j-1] + (2 if a[i-1] == b[j-1] else -1)
            H[i][j] = max(0, s, H[i-1][j]-2, H[i][j-1]-2)
            if H[i][j] > best[0]: best = (H[i][j], i, j)
    # traceback start
    sc, i, j = best
    while i > 0 and j > 0 and H[i][j] > 0:
        if H[i][j] == H[i-1][j-1] + (2 if a[i-1] == b[j-1] else -1): i, j = i-1, j-1
        elif H[i][j] == H[i-1][j]-2: i -= 1
        else: j -= 1
    return sc, j, best[2], i

if __name__ == '__main__':
    S = stream()
    for abbr in (True,):
        P = ptoks(abbr)
        W = int(sys.argv[1]) if len(sys.argv) > 1 else 20
        print('plaintext tokens', len(P), 'stream', len(S))
        for j in range(W):
            col = P[j::W]
            sc, st, en, pi = sw(col, S)
            print('%2d len%2d score%3d stream[%3d:%3d] %s | %s' % (j, len(col), sc, st, en, ''.join(col), ' '.join(S[st:en])))
