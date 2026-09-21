# Hard-EM monotone alignment of code groups to contemporary decipherments (after balbases1677/align2.py).
# Inline clear words in the cipher are soft anchors; dotted gaps are wildcards.
import re, math, collections, sys, json, unicodedata
sys.stdout.reconfigure(encoding='utf-8')

def norm(s):
    s = unicodedata.normalize('NFD', s.lower())
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^a-z]', '', s.replace('ÿ', 'y'))

def read_cipher(f, cut=None):
    toks = []
    for line in open(f, encoding='utf-8'):
        if line.startswith('#'): continue
        line = re.sub(r'\{[^}]*\}', ' ', line)
        for m in re.finditer(r'\[([^\]]*)\]|(\S+)', line):
            if m.group(1) is not None:
                inner = m.group(1)
                if re.fullmatch(r'\.+', inner.strip()): toks.append('*')
                else: toks += ['=' + norm(w) for w in inner.split() if norm(w)]
            else:
                t = m.group(2).rstrip('?,.:;')
                if re.fullmatch(r'\d+', t): toks.append(t)
                if cut and t == cut: return toks
    return toks

def read_clear(f, start=None, end=None):
    txt = []
    for line in open(f, encoding='utf-8'):
        if line.startswith('#') or line.lstrip().startswith('[catchword') or line.lstrip().startswith('[folio'): continue
        line = re.sub(r'<[^>]*>', '', line); line = re.sub(r'\[[^\]]*\]', '', line)
        line = line.replace('{', '').replace('}', '')
        txt.append(line.rstrip('\n').rstrip('-'))
    s = norm(''.join(txt) if False else ' '.join(txt).replace('- ', ''))
    if start: s = s[s.index(norm(start)):]
    if end: s = s[:s.index(norm(end)) + len(norm(end))]
    return s

def lev(a, b):
    p = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        c = [i]
        for j, y in enumerate(b, 1): c.append(min(p[j] + 1, c[j - 1] + 1, p[j - 1] + (x != y)))
        p = c
    return p[-1]

MAXL = 12
LP = [.2, .12, .2, .2, .15, .1, .06, .04, .03, .02, .015, .01, .01]
SKIP = 8.0
cnt = collections.defaultdict(collections.Counter)
FIX = {}

def cost(tok, sub):
    if tok == '*': return 0.5 * len(sub) ** 0.5
    if tok[0] == '=':
        w = tok[1:]
        return 0.0 if sub == w else 2.5 * lev(sub, w) + 1
    if tok in FIX: return 0.0 if sub in FIX[tok] else 25.0
    c = cnt[tok]; n = sum(c.values()); a = 0.5
    L = min(len(sub), 12)
    p = (c[sub] + a * LP[L] * (1 / 18) ** L) / (n + a)
    return -math.log(p)

def maxlen(tok):
    if tok == '*': return 60
    if tok[0] == '=': return len(tok) + 3
    return MAXL

def align(t, s):
    I, J = len(t), len(s); INF = 1e18
    D = [dict() for _ in range(I + 1)]; B = [dict() for _ in range(I + 1)]
    D[0][0] = 0.0
    band = max(80, int(0.12 * J))
    for i in range(I + 1):
        c = i * J / max(I, 1); lo = max(0, int(c - band)); hi = min(J, int(c + band))
        Di = D[i]
        for j in sorted(k for k in Di if lo <= k <= hi or i == I):
            d = Di[j]
            if j < J and d + SKIP < Di.get(j + 1, INF): Di[j + 1] = d + SKIP; B[i][j + 1] = (i, j, None)
            if i < I:
                tok = t[i]; Dn = D[i + 1]; Bn = B[i + 1]
                for L in range(0, min(maxlen(tok), J - j) + 1):
                    v = d + cost(tok, s[j:j + L])
                    if v < Dn.get(j + L, INF): Dn[j + L] = v; Bn[j + L] = (i, j, s[j:j + L])
    if J not in D[I]: return INF, []
    i, j = I, J; path = []
    while (i, j) != (0, 0):
        pi, pj, sub = B[i][j]
        path.append((t[pi] if sub is not None else None, sub if sub is not None else s[pj]))
        i, j = pi, pj
    return D[I][J], path[::-1]

DATA = [
    ('R2121', read_cipher('tx/R2121_cipher.txt', cut='3107'), read_clear('tx/R2121_clear.txt', 'Bij eene volgende', 'volmaakt geschikt')),
]
if __name__ == '__main__':
    extra = sys.argv[2:] if len(sys.argv) > 2 else []
    for x in extra:
        n, cf, pf = x.split(':'); DATA.append((n, read_cipher(cf), read_clear(pf)))
    for n, t, s in DATA: print(n, len(t), 'tokens', len(s), 'chars', flush=True)
    for it in range(int(sys.argv[1]) if len(sys.argv) > 1 else 8):
        new = collections.defaultdict(collections.Counter); tot = 0; paths = {}
        for n, t, s in DATA:
            c, p = align(t, s); tot += c; paths[n] = p
            for tok, sub in p:
                if tok is not None and tok[0] not in '=*': new[tok][sub] += 1
        cnt = new; print('iter', it, round(tot), flush=True)
    json.dump(paths, open('paths.json', 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump({k: dict(v) for k, v in cnt.items()}, open('counts.json', 'w', encoding='utf-8'), ensure_ascii=False)
