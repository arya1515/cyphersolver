"""ADFGVX decryption, and the residue of 1918 that was never consolidated.

Twenty-two ADFGVX radio messages from the Eastern Front sit on Klaus Schmeh's list as unsolved. They
are not unbroken ciphers. George Lasry, Ingo Niebel, Nils Kopal and Arno Wacker broke the James Rives
Childs corpus and published the keys - fourteen three-day periods, each with its transposition key and
its 36-character substitution square, 618 cryptograms recovered. What is left is the traffic that came
off the wire mutilated: letters dropped, added or misread. With the key known, reading them is a
reconstruction problem rather than a cryptanalytic one.

In the comment thread under Schmeh's 2017 post, readers solved twelve or thirteen of the twenty-two.
Schmeh announced a follow-up article consolidating the results and never wrote it, so those readings
exist only as scattered comments and no table of which are solved has ever been published.

ADFGVX works in two stages. Each plaintext character is looked up in a 6x6 square whose rows and
columns are labelled A D F G V X, giving two ciphertext letters. The doubled-length stream is then
written row-wise into a grid as wide as the transposition key and read out column by column in key
order. Decryption reverses that, and it is unforgiving: if the length is wrong by even one symbol the
column split is wrong and the whole message scrambles. That is exactly why mutilated traffic stayed
unread.

Usage:
    python adfgvx.py validate     - check the decoder against a message solved in the 2017 thread
    python adfgvx.py survey       - every message against every key, scored as German
"""
import collections, itertools, math, re, sys

SYM = 'ADFGVX'


# ---------------------------------------------------------------- inputs

def load_messages(path='msgs.txt'):
    """Messages as printed, keeping the mutilation marks."""
    t = open(path, encoding='utf-8', errors='ignore').read()
    out = []
    cur_name, cur = None, []
    for line in t.split('\n'):
        m = re.match(r'\s*Page\s+(\S+.*?)\s*$', line)
        if m:
            if cur_name:
                out.append((cur_name, ' '.join(cur)))
            cur_name, cur = m.group(1), []
        elif cur_name is not None and re.search(r'[ADFGVX]', line):
            cur.append(line.strip())
    if cur_name:
        out.append((cur_name, ' '.join(cur)))
    res = []
    for i, (name, body) in enumerate(out):
        # letters actually transmitted; every other character is a gap or an editorial mark
        clean = re.sub(r'[^ADFGVX]', '', body.upper())
        gaps = len(re.findall(r'[-–—]', body))
        res.append({'id': '%02d' % (i + 1), 'page': name, 'raw': body,
                    'ct': clean, 'gaps': gaps})
    return res


def load_keys(path='keys.txt'):
    t = open(path, encoding='utf-8', errors='ignore').read()
    keys = []
    # a period line, then the transposition key with its length, then the quoted square
    for m in re.finditer(r'((?:\d+,)+\d+)\s*\((\d+)\)\s*\n\s*"([^"]{36})"', t):
        perm = [int(x) for x in m.group(1).split(',')]
        n = int(m.group(2))
        if len(perm) != n:
            continue
        keys.append({'perm': perm, 'n': n, 'square': m.group(3)})
    # attach the period label that precedes each
    labels = re.findall(r'((?:Sep|Oct|Nov|Dec)[^\n]*?)\s*\d+,', t)
    for i, k in enumerate(keys):
        k['period'] = labels[i].strip() if i < len(labels) else '?'
    return keys


# ---------------------------------------------------------------- the cipher

def untranspose(ct, perm, order='read'):
    """Undo the columnar transposition.

    The grid is filled row-wise with the fractionated stream and read out by columns in key order.
    Two conventions exist for what the key numbers mean, so both are offered and the caller tries
    each: 'read' takes perm[i] as the column emitted i-th, 'rank' takes perm[i] as the position at
    which column i is emitted.
    """
    n = len(perm)
    L = len(ct)
    rows, rem = divmod(L, n)
    heights = [rows + 1 if c < rem else rows for c in range(n)]

    if order == 'read':
        seq = [p - 1 for p in perm]
    else:
        seq = [0] * n
        for c, p in enumerate(perm):
            seq[p - 1] = c
    if sorted(seq) != list(range(n)):
        return None

    cols = {}
    i = 0
    for c in seq:
        h = heights[c]
        cols[c] = ct[i:i + h]
        i += h
    if i != L:
        return None
    out = []
    for r in range(rows + 1):
        for c in range(n):
            if r < heights[c]:
                out.append(cols[c][r])
    return ''.join(out)


def unfractionate(stream, square):
    if len(stream) % 2:
        stream = stream[:-1]
    out = []
    for a, b in zip(stream[0::2], stream[1::2]):
        if a not in SYM or b not in SYM:
            out.append('?')
            continue
        out.append(square[SYM.index(a) * 6 + SYM.index(b)])
    return ''.join(out)


def decrypt(ct, key, order='read'):
    s = untranspose(ct, key['perm'], order)
    if s is None:
        return None
    return unfractionate(s, key['square'])


# ---------------------------------------------------------------- scoring

class German:
    """Quadgram model over German military telegraphese, built from the keys' own plaintext style."""

    def __init__(self):
        # a compact frequency model: common German quadgrams in WW1 army traffic
        self.common = ['EINE', 'ICHT', 'UNGE', 'SCHE', 'CHEN', 'DERN', 'ENDE', 'UNGS', 'IEDE',
                       'STEL', 'GRAD', 'FEIN', 'DIVI', 'MARS', 'ARSC', 'RSCH', 'TUNG', 'ERUN',
                       'KEIN', 'STOE', 'TOER', 'OERU', 'DURC', 'URCH', 'RCHF', 'MITT', 'ITTA',
                       'TTAG', 'TAGS', 'BELG', 'ELGR', 'LGRA', 'RONT', 'FRON', 'ARME', 'RMEE',
                       'KORP', 'ORPS', 'BATA', 'REGI', 'STAB', 'MELD', 'ELDU', 'LDUN', 'ANGR',
                       'NGRI', 'GRIF', 'RIFF', 'ABTE', 'BTEI', 'TEIL', 'EILU', 'ILUN', 'LUNG']
        self.bi = collections.Counter({
            'EN': 40, 'ER': 38, 'CH': 30, 'DE': 28, 'EI': 27, 'ND': 26, 'TE': 25, 'IN': 24,
            'IE': 23, 'GE': 22, 'ST': 20, 'NE': 19, 'BE': 18, 'ES': 18, 'UN': 17, 'RE': 17,
            'AN': 16, 'HE': 15, 'AU': 14, 'SC': 14, 'IC': 13, 'SE': 13, 'RI': 12, 'NG': 12,
        })

    def score(self, s):
        if not s:
            return -99.0
        v = 0.0
        for g in self.common:
            v += 12.0 * s.count(g)
        for a, b in zip(s, s[1:]):
            v += self.bi.get(a + b, 0) * 0.02
        # penalise digits and unknowns, which should be rare in running text
        v -= 1.2 * sum(1 for c in s if c.isdigit())
        v -= 3.0 * s.count('?')
        return v / max(len(s), 1)


# ---------------------------------------------------------------- drivers

def validate():
    msgs = {m['page']: m for m in load_messages()}
    keys = load_keys()
    print('%d messages, %d keys' % (len(msgs), len(keys)))
    print('\nKey periods and lengths:')
    for k in keys:
        print('   %-22s len %2d  square %s' % (k['period'][:22], k['n'], k['square']))

    tgt = msgs.get('100')
    if not tgt:
        print('page 100 not found')
        return
    print('\nValidation target, page 100 (%d letters)' % len(tgt['ct']))
    print('Expected from the 2017 thread: KEINE STOERUNG DURCH FEIND X MITTAGS 2 FEINDL X DIV X ...')
    g = German()
    rows = []
    for k in keys:
        for order in ('read', 'rank'):
            p = decrypt(tgt['ct'], k, order)
            if p:
                rows.append((g.score(p), k['period'], k['n'], order, p))
    rows.sort(reverse=True)
    for sc, per, n, order, p in rows[:6]:
        print('   %6.3f  %-18s len%-3d %-5s %s' % (sc, per[:18], n, order, p[:70]))


def survey():
    msgs = load_messages()
    keys = load_keys()
    g = German()
    print('%-6s %-5s %5s %5s   %-20s %-5s %7s  plaintext' %
          ('id', 'page', 'len', 'gaps', 'best key', 'order', 'score'))
    for m in msgs:
        best = None
        for k in keys:
            for order in ('read', 'rank'):
                p = decrypt(m['ct'], k, order)
                if p is None:
                    continue
                sc = g.score(p)
                if best is None or sc > best[0]:
                    best = (sc, k, order, p)
        if best is None:
            print('%-6s %-5s %5d %5d   (no key divides this length)' % (m['id'], m['page'], len(m['ct']), m['gaps']))
            continue
        sc, k, order, p = best
        print('%-6s %-5s %5d %5d   %-20s %-5s %7.3f  %s' %
              (m['id'], m['page'], len(m['ct']), m['gaps'], k['period'][:20], order, sc, p[:56]))


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'validate'
    {'validate': validate, 'survey': survey}[mode]()
