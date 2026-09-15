"""Brute-force the garbled tail 'zpongobunibai' (letters after 返): all strings within
edit distance <= 2 that parse cleanly into CV syllables (even count), decoded with the
recovered table; rank by codebook validity + LM."""
import os, sys, itertools
from family import code2ch, lp, CONS, VOW
from show import key_from_name
sys.stdout = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tail_out.txt'), 'w', encoding='utf-8')
tbl, rot = key_from_name('rot8', 'eaiou', 'vow', 1)
ALPHA = CONS + VOW
tail = sys.argv[1] if len(sys.argv) > 1 else 'zpongobunibai'
maxed = int(sys.argv[2]) if len(sys.argv) > 2 else 2

CONFUSE = {'n': 'hu', 'h': 'n', 'u': 'na', 'a': 'ou', 'o': 'a', 'e': 'ci', 'c': 'e', 'i': 'e', 'z': 'x', 'x': 'z', 'v': 'u', 'r': 'v'}
def neighbours(s, restricted):
    out = set()
    for i in range(len(s)):
        out.add(s[:i] + s[i+1:])                      # delete
        subs = CONFUSE.get(s[i], '') if restricted else ALPHA
        for ch in subs:
            if ch != s[i]: out.add(s[:i] + ch + s[i+1:])  # substitute
    for i in range(len(s) + 1):
        ins = (VOW if (i > 0 and s[i-1] in CONS) else CONS) if restricted else ALPHA
        for ch in ins:
            out.add(s[:i] + ch + s[i:])              # insert
    return out

def parse_clean(s):
    if len(s) % 2: return None
    syl = [s[i:i+2] for i in range(0, len(s), 2)]
    if all(a in CONS and b in VOW for a, b in syl) and len(syl) % 2 == 0:
        return syl
    return None

seen = {tail: 0}
frontier = {tail}
restricted = maxed >= 3
for d in range(1, maxed + 1):
    nxt = set()
    for s in frontier:
        for t in neighbours(s, restricted):
            if t not in seen:
                seen[t] = d; nxt.add(t)
    frontier = nxt
print('candidates', len(seen))
res = []
for s, d in seen.items():
    syl = parse_clean(s)
    if not syl: continue
    codes = ['%02d%02d' % (tbl[syl[i]], tbl[syl[i+1]]) for i in range(0, len(syl), 2)]
    nbad = sum(c not in code2ch for c in codes)
    if nbad > 1: continue
    chars = ''.join(code2ch.get(c, '□') for c in codes)
    sc = sum(lp(ch) if ch != '□' else -25 for ch in chars) - 2.5 * d
    res.append((sc, d, s, ' '.join(codes), chars))
res.sort(key=lambda x: -x[0])
for r in res[:60]:
    print('%.1f d%d %-16s %s  %s' % r)
