"""Decrypt Cardinal Alessandrino's 1568 ciphers to the nuncio in Spain (ASV Segr. Stato Spagna 6/I, DECODE R93-R102).

Key: George Lasry's reconstruction on DECODE (DOC_R9x_D32xx.txt, Oct 2020). Polyphonic: each digit 1-9 stands for
two letters, 0 is a null; nomenclator codes are four digits X0Y0 (the zeros null-like) or dotted pairs.
Each digit has two readings, so the text is chosen by a beam search scored by the shared Italian model
(lang/, it-cinquecento, no spaces). Unknown X0Y0 groups are also allowed to read as two letters with nulls.

usage: python decrypt.py [transcription ...]    (default: decode/DOC_R*_D16xx/D2342 transcriptions)
"""
import glob, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
for p in (os.path.join(HERE, '..'), os.path.join(HERE, '..', '..', 'cypher-lang')):
    if os.path.isdir(os.path.join(p, 'lang')):
        sys.path.insert(0, os.path.abspath(p)); break
from lang import lm

POLY = {'4': 'al', '8': 'bc', '7': 'dr', '6': 'en', '3': 'fg', '2': 'im', '5': 'os', '9': 'pz', '1': 'ut'}
# Lasry's nomenclator (DOC_32xx); '?' glosses are his tentative ones.
NOM = {
    '1010': 'nostro signore', '1020': 'sua santita', '4010': 'sua santita', '9010': 'sua santita',
    '1040': 'regina di francia', '1050': 'francia', '1090': 'vostra signoria', '2020': 'con',
    '2040': 'concilio', '2060': 'non', '2090': 'che', '3010': 're', '3040': 'fiandra', '4030': 'sua maesta',
    '4060': 'questo', '4090': 'germania', '9030': 'germania', '5020': 'per', '5090': 'qui', '6090': 'quel',
    '7090': 'quello', '8010': 're di francia', '8090': 'sauere', '9020': 'quelle', '9060': 'questa',
}
DOTTED = {'00': '', '39': 'qua'}
NULL_COST = -1.5   # zeros are very common nulls
NOM_BONUS = 1.0

M = lm.load('it-cinquecento', spaces=False)
A, K = M.A, M.order
IDX = M.index
LP = M.lp.reshape(-1, A)
MOD = A ** (K - 1)


def enc(s):
    return [IDX[ch] for ch in lm.norm(s, 'early', False)]


def step(ctx, chars):
    s = 0.0
    for x in chars:
        s += float(LP[ctx, x])
        ctx = (ctx * A + x) % MOD
    return ctx, s


def parse(path):
    """Yield (image, items); item = digit str, or ('D', code) for a dotted group, '?' for unreadable."""
    out, cur, items = [], None, []
    for line in open(path, encoding='utf-8', errors='replace'):
        line = line.rstrip('\n')
        m = re.match(r'#IMAGE NAME:\s*(\S+)', line)
        if m:
            if items:
                out.append((cur, items))
            cur, items = m.group(1), []
            continue
        if line.startswith('#'):
            continue
        line = re.sub(r'<[^>]*>', ' ', line)
        toks = line.split()
        for i, t in enumerate(toks):
            if '^.' in t:
                # dotted digit: pair with the previous plain digit (Lasry: "2 digits, the second has dot on top")
                prev = items.pop() if items and isinstance(items[-1], str) and items[-1].isdigit() else ''
                items.append(('D', prev + re.sub(r'\D', '', t)))
                continue
            d = re.sub(r'[^0-9]', '', t)
            if not d:
                items.append('?')
            items.extend(d)
    if items:
        out.append((cur, items))
    return out


def decode(items, beam=300):
    start = 0
    for x in enc('ente'):
        start = (start * A + x) % MOD
    n = len(items)
    states = [dict() for _ in range(n + 1)]
    states[0][start] = (0.0, None)
    for p in range(n):
        if not states[p]:
            continue
        best = sorted(states[p].items(), key=lambda kv: -kv[1][0])[:beam]
        for ctx, (sc, _) in best:
            it = items[p]
            moves = []
            if isinstance(it, tuple):
                g = DOTTED.get(it[1])
                moves.append((1, g if g is not None else '[' + it[1] + '.]', enc(g) if g else [], 0.0 if g is not None else -4.0))
            elif it == '?':
                moves.append((1, '?', [], -3.0))
            elif it == '0':
                moves.append((1, '', [], NULL_COST))
            else:
                for ch in POLY[it]:
                    moves.append((1, ch, enc(ch), 0.0))
                seg = items[p:p + 4]
                if len(seg) == 4 and all(isinstance(x, str) for x in seg):
                    code = ''.join(seg)
                    if code in NOM:
                        pt = NOM[code]
                        moves.append((4, '[' + pt.upper() + ']', enc(pt), NOM_BONUS))
            for L, txt, chars, pen in moves:
                nctx, s = step(ctx, chars)
                ns = sc + s + pen
                q = p + L
                old = states[q].get(nctx)
                if old is None or ns > old[0]:
                    states[q][nctx] = (ns, (p, ctx, txt))
    end = max(states[n].items(), key=lambda kv: kv[1][0])
    out, q, ctx = [], n, end[0]
    while states[q][ctx][1] is not None:
        p, pctx, txt = states[q][ctx][1]
        out.append(txt)
        q, ctx = p, pctx
    return ''.join(reversed(out)), end[1][0] / max(1, n)


def main():
    files = sys.argv[1:] or sorted(glob.glob(os.path.join(HERE, 'decode', 'DOC_R*_D1[6]*.txt')) +
                                   glob.glob(os.path.join(HERE, 'decode', 'DOC_R100_D2342_2342.txt')) + glob.glob(os.path.join(HERE, 'decode', 'DOC_R115_D1*.txt')),
                                   key=lambda f: int(re.search(r'DOC_R(\d+)', f).group(1)))
    for f in files:
        rec = re.search(r'DOC_(R\d+)', f).group(1)
        for img, items in parse(f):
            txt, per = decode(items)
            print(f'== {rec} {img} ({len(items)} items, {per:.2f}/item)')
            print(txt)
            print()


if __name__ == '__main__':
    main()
