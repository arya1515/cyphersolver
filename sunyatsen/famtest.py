"""Run the systematic-condenser family (../family.py) on any telegram transcription.
Usage: python famtest.py "word word word ..."   (words that are not clean CV strings split the stream)
Also prints the decodes under the two keys known so far (Swatow 1916, Shanghai 1917)."""
import sys, io, itertools, statistics
from family import code2ch, CONS, VOW, make_table, score_codes
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
KNOWN = {'swatow1916': (8, 'eaiou', 0), 'shanghai1917': (7, 'aeuoi', 0),
         'shanghai1916': (0, 'ioaeu', 1), 'manila1916': (4, 'oeuai', 0)}   # (rotation, vowel order, reversed)
def segs_of(words):
    segs, cur, pos = [], [], 0
    for w in words:
        ok = len(w) % 2 == 0 and all(w[i] in CONS and w[i+1] in VOW for i in range(0, len(w), 2))
        if ok:
            if not cur: start = pos
            cur += [w[i:i+2] for i in range(0, len(w), 2)]
        else:
            if cur: segs.append((start, cur)); cur = []
        pos += len(w) // 2
    if cur: segs.append((start, cur))
    return segs
def dec(t, seg, a, add=0):
    n = [t[s] for s in seg]
    return ['%04d' % ((n[i]*100 + n[i+1] + add) % 10000) for i in range(a, len(n)-1, 2)]
def best(t, segs, add=0):
    tot, txt = 0, []
    for k, (st, seg) in enumerate(segs):
        al = (st % 2,) if k == 0 and st == 0 else (0, 1)
        sc, a = max((score_codes(dec(t, seg, a, add)), a) for a in al)
        tot += sc; txt.append(''.join(code2ch.get(c, '□') for c in dec(t, seg, a, add)))
    return tot, ' | '.join(txt)
def table(r, vo, rev=False, fill='vow', off=1):
    base = list(CONS); co = base[r:] + base[:r]
    if rev: co = co[::-1]
    return make_table(co, list(vo), fill, off)
if __name__ == '__main__':
    words = sys.argv[1].lower().split()
    segs = segs_of(words)
    print('segments:', [(s, len(g)) for s, g in segs])
    for k, (r, vo, rv) in KNOWN.items(): print(k, '%.1f' % best(table(r, vo, rv), segs)[0], best(table(r, vo, rv), segs)[1])
    res = []
    for r in range(20):
        for rev in (0, 1):
            for vo in itertools.permutations('aeiou'):
                for fill in ('vow', 'cons'):
                    for off in (0, 1):
                        t = table(r, vo, rev, fill, off)
                        for add in (0, 111, -111):
                            sc, txt = best(t, segs, add)
                            res.append((sc, '%s%d %s %s off%d add%d' % ('rev' if rev else 'rot', r, ''.join(vo), fill, off, add), txt))
    res.sort(key=lambda x: -x[0]); s = [x[0] for x in res]
    print('mean %.1f sd %.1f' % (statistics.mean(s), statistics.pstdev(s)))
    mu, sd = statistics.mean(s), statistics.pstdev(s)
    for x in res[:8]: print('%.1f z=%.1f %s  %s' % (x[0], (x[0]-mu)/sd, x[1], x[2]))
