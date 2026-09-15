"""Reading mutilated ADFGVX traffic against known keys, by searching for the dropped letters.

The twenty-two messages on Schmeh's list are not unbroken ciphers. Lasry, Niebel, Kopal and Wacker
published the keys. What defeats these particular messages is that letters were lost or added in
transmission, and ADFGVX is unforgiving about length: the columnar stage splits the stream by the
key length, so one missing letter moves every column boundary after it and the whole message
scrambles.

Page 100 makes the point. A reader solved it in the 2017 comment thread as

    KEINE STOERUNG DURCH FEIND X MITTAGS 2 FEINDL X DIV X IM MARSCH AUF BELGRAD X

which is 62 characters, so 124 ADFGVX letters. Only 122 were received. Two are missing, and until
they are put back in the right places no key reads it.

So: for each key, and each way of inserting the missing letters, decrypt and score. The inserted
positions are unknown but few, and the search is small enough to be exhaustive. Placeholders are
inserted rather than guessed letters, because the placeholder's own plaintext pair is unreadable
either way and what matters is restoring the column boundaries for everything else.

Usage:
    python repair.py validate         - recover page 100 and check it against the published reading
    python repair.py solve [page]     - search a message, or all of them
"""
import collections, itertools, json, re, sys

SYM = 'ADFGVX'
PLACE = '#'


def load_keys(path='keys.json'):
    return json.load(open(path, encoding='utf-8'))


def load_messages(path='msgs.txt'):
    t = open(path, encoding='utf-8', errors='ignore').read()
    out, name, cur = [], None, []
    for line in t.split('\n'):
        m = re.match(r'\s*Page\s+(\S+.*?)\s*$', line)
        if m:
            if name:
                out.append((name, ' '.join(cur)))
            name, cur = m.group(1), []
        elif name is not None and re.search(r'[ADFGVX]', line):
            cur.append(line.strip())
    if name:
        out.append((name, ' '.join(cur)))
    res = []
    for i, (nm, body) in enumerate(out):
        res.append({'i': i + 1, 'page': nm, 'raw': body,
                    'ct': re.sub(r'[^ADFGVX]', '', body.upper())})
    return res


def untranspose(ct, perm, n, conv='A'):
    """conv A: perm[i] is the column emitted i-th.  conv B: perm[i] is when column i is emitted."""
    L = len(ct)
    rows, rem = divmod(L, n)
    h = [rows + 1 if c < rem else rows for c in range(n)]
    seq = [p - 1 for p in perm] if conv == 'A' else sorted(range(n), key=lambda c: perm[c])
    cols, i = {}, 0
    for c in seq:
        cols[c] = ct[i:i + h[c]]
        i += h[c]
    out = []
    for r in range(rows + 1):
        for c in range(n):
            if r < h[c]:
                out.append(cols[c][r])
    return ''.join(out)


def unfractionate(s, square):
    out = []
    for a, b in zip(s[0::2], s[1::2]):
        if a not in SYM or b not in SYM:
            out.append('.')
            continue
        ch = square[SYM.index(a) * 6 + SYM.index(b)]
        out.append(ch if ch != '-' else '.')
    return ''.join(out)


# ---------------------------------------------------------------- German scoring

WORDS = ['KEINE', 'STOERUNG', 'DURCH', 'FEIND', 'FEINDL', 'MITTAGS', 'MARSCH', 'BELGRAD',
         'DIVISION', 'DIV', 'ARMEE', 'KORPS', 'FRONT', 'ANGRIFF', 'MELDUNG', 'ABTEILUNG',
         'STELLUNG', 'GESTERN', 'HEUTE', 'MORGEN', 'ABEND', 'NACHT', 'UHR', 'BATAILLON',
         'REGIMENT', 'KOMMANDO', 'GENERAL', 'OBERST', 'NICHT', 'WIRD', 'SIND', 'EINE',
         'DIE', 'DER', 'DAS', 'UND', 'VON', 'FUER', 'MIT', 'AUF', 'AUS', 'IST', 'BEI',
         'ZUM', 'ZUR', 'IM', 'AM', 'AN', 'VOR', 'NACH', 'UEBER', 'GEGEN', 'BIS', 'ODER',
         'SOLL', 'MUSS', 'KANN', 'HAT', 'HABEN', 'WERDEN', 'WORDEN', 'GEMELDET', 'BEFEHL',
         'TRUPPEN', 'STAB', 'FUNK', 'STELLE', 'LAGE', 'RUHIG', 'ARTILLERIE', 'INFANTERIE']

BIG = collections.Counter({
    'EN': 45, 'ER': 42, 'CH': 32, 'DE': 30, 'EI': 29, 'ND': 28, 'TE': 27, 'IN': 26, 'IE': 25,
    'GE': 24, 'ST': 22, 'NE': 21, 'BE': 20, 'ES': 20, 'UN': 19, 'RE': 18, 'AN': 18, 'HE': 16,
    'AU': 15, 'SC': 15, 'IC': 14, 'SE': 14, 'RI': 13, 'NG': 13, 'LI': 12, 'HT': 12, 'UE': 11,
})


def score(s):
    if not s:
        return -99.0
    v = 0.0
    for w in WORDS:
        v += (len(w) ** 1.5) * s.count(w)
    for a, b in zip(s, s[1:]):
        v += BIG.get(a + b, 0) * 0.03
    v -= 2.0 * s.count('.')
    v -= 0.8 * sum(1 for c in s if c.isdigit())
    return v


# ---------------------------------------------------------------- the search

def attempts(ct, n_ins, n_del=0):
    """Every way of inserting n_ins placeholders (and deleting n_del letters)."""
    L = len(ct)
    if n_del:
        for combo in itertools.combinations(range(L), n_del):
            s = ''.join(c for i, c in enumerate(ct) if i not in combo)
            yield s, ('del', combo)
        return
    if n_ins == 0:
        yield ct, ('exact', ())
        return
    for combo in itertools.combinations_with_replacement(range(L + 1), n_ins):
        s, off = ct, 0
        for p in combo:
            s = s[:p + off] + PLACE + s[p + off:]
            off += 1
        yield s, ('ins', combo)


def search(ct, keys, max_ins=2, max_del=1, topn=5):
    best = []
    for k in keys:
        n, perm, sq = k['n'], k['perm'], k['square']
        for n_ins in range(0, max_ins + 1):
            for cand, how in attempts(ct, n_ins):
                if len(cand) % 2:
                    continue
                pt = unfractionate(untranspose(cand, perm, n, 'B'), sq)
                best.append((score(pt), k, ('B',) + how, pt))
        for n_del in range(1, max_del + 1):
            for cand, how in attempts(ct, 0, n_del):
                if len(cand) % 2:
                    continue
                pt = unfractionate(untranspose(cand, perm, n, 'B'), sq)
                best.append((score(pt), k, ('B',) + how, pt))
    best.sort(key=lambda x: -x[0])
    return best[:topn]


def validate():
    keys = load_keys()
    msgs = {m['page']: m for m in load_messages()}
    ct = msgs['100']['ct']
    want = 'KEINESTOERUNGDURCHFEINDXMITTAGS2FEINDLXDIVXIMMARSCHAUFBELGRADX'
    print('page 100: %d letters received; the published reading needs %d' % (len(ct), 2 * len(want)))
    res = search(ct, keys, max_ins=2, max_del=0, topn=6)
    for sc, k, how, pt in res:
        tag = 'MATCH' if pt.replace('.', '') and want[:20] in pt else ''
        print('   %8.1f  len%-3d %-16s %s %s' % (sc, k['n'], str(how)[:16], pt[:64], tag))


def solve(page=None, start=0):
    keys = load_keys()
    msgs = load_messages()
    for m in msgs:
        if m['i'] <= start:
            continue
        if page and not m['page'].startswith(page):
            continue
        res = search(m['ct'], keys, max_ins=2, max_del=1, topn=2)
        print('\npage %-5s (%d letters)' % (m['page'], len(m['ct'])))
        for sc, k, how, pt in res:
            print('   %8.1f len%-3d %-18s %s' % (sc, k['n'], str(how)[:18], pt[:70]))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'validate'
    if mode == 'validate':
        validate()
    else:
        a = sys.argv[2] if len(sys.argv) > 2 else None
        if a and a.startswith('from'):
            solve(None, int(a[4:]))
        else:
            solve(a)
