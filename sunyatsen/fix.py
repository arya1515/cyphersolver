"""Explore corrections for doubtful codes under the recovered table (rot8 eaiou vow off1).
1) For each doubtful code, list one-letter substitutions and the resulting characters.
2) For the garbled tail 'zpongobunibai', enumerate parsings with <=2 edits and score."""
import os, sys, itertools, math
from family import code2ch, lp, CONS, VOW, make_table
from show import key_from_name
sys.stdout = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fix_out.txt'), 'w', encoding='utf-8')
tbl, rot = key_from_name('rot8', 'eaiou', 'vow', 1)
inv = {v: k for k, v in tbl.items()}

def code(s1, s2): return '%02d%02d' % (tbl[s1], tbl[s2])
def alts(s1, s2, label):
    print('== %s  %s %s = %s %s' % (label, s1, s2, code(s1, s2), code2ch.get(code(s1, s2), '□')))
    seen = set()
    for pos in (0, 1):
        syl = [s1, s2][pos]
        for i, cls in ((0, CONS), (1, VOW)):
            for ch in cls:
                if ch == syl[i]: continue
                new = syl[:i] + ch + syl[i+1:]
                pair = [new, s2] if pos == 0 else [s1, new]
                c = code(*pair)
                if c in code2ch and c not in seen:
                    seen.add(c)
                    print('   %s %s -> %s %s' % (pair[0], pair[1], c, code2ch[c]))
    print()

alts('xu', 'pe', '2nd char (潮_)')
alts('he', 'mi', '亦_復')
alts('xi', 'to', '翼_')
alts('ha', 'tu', '_持')
alts('pa', 'va', '_慧返')
alts('je', 'jo', '文_返')
alts('ro', 'pe', '文慧_')

# --- tail --------------------------------------------------------------------
tail = 'zpongobunibai'
print('== tail', tail)
def parses(s):
    """yield (syllables, edits) for parsing s into CV syllables allowing deletions/insertions of a partner letter/substitutions (<=2 edits)"""
    res = []
    def rec(i, acc, edits, log):
        if edits > 2: return
        if i == len(s):
            if len(acc) % 2 == 0: res.append((acc, edits, log))
            return
        ch = s[i]
        # normal syllable
        if i + 1 < len(s) and ch in CONS and s[i+1] in VOW:
            rec(i + 2, acc + [ch + s[i+1]], edits, log)
        # delete this letter
        rec(i + 1, acc, edits + 1, log + ['del %s@%d' % (ch, i)])
        # consonant with missing vowel
        if ch in CONS:
            for v in VOW:
                rec(i + 1, acc + [ch + v], edits + 1, log + ['ins vowel after %s@%d' % (ch, i)])
        # vowel with missing consonant
        if ch in VOW:
            for c in CONS:
                rec(i + 1, acc + [c + ch], edits + 1, log + ['ins cons before %s@%d' % (ch, i)])
        # substitute this letter by same class then pair
        if i + 1 < len(s):
            if ch in CONS and s[i+1] in CONS:  # ch is a misread vowel? no: next is cons -> ch should be vowel? skip
                pass
            if ch in VOW and s[i+1] in VOW:
                for c in CONS:
                    rec(i + 2, acc + [c + s[i+1]], edits + 1, log + ['sub %s@%d->%s' % (ch, i, c)])
    rec(0, [], 0, [])
    return res
scored = []
for syl, edits, log in parses(tail):
    codes = [code(syl[i], syl[i+1]) for i in range(0, len(syl), 2)]
    if not all(c in code2ch for c in codes): continue
    sc = sum(lp(code2ch[c]) for c in codes) - 3.0 * edits
    scored.append((sc, ' '.join(syl), ' '.join(codes), ''.join(code2ch[c] for c in codes), log))
scored.sort(key=lambda x: -x[0])
for r in scored[:40]:
    print('%.1f  %s | %s | %s | %s' % r)
