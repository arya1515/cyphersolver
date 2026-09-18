"""Systematic-condenser family brute force on the Sunwen telegram, Shanghai -> Tokyo, 23 Mar 1917
(JACAR B03050090200, frame 0504). Same family as ../family.py (57 600 keys)."""
import sys, os, io, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from family import code2ch, CONS, VOW, make_table, score_codes, lp
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# My reading of the received form (g/q ambiguous in this hand).
WORDS = ("naroxoziji kojipanejo facorabixa pixaqaqe eianakerele befacoyohi tebovocega "
         "kalamanaro rugoqasuxe bixaziqaso yusoxozipa bujihoceno poqiqaforu qocaxoqasu "
         "xebiqabiqo mujuvamako qabokezaka cagexuxala banegerapo qixapfete").split()
def sy(w): return [w[i:i+2] for i in range(0, len(w), 2)]
SEG_A = sum((sy(w) for w in WORDS[0:3]), [])          # syllables 0-14, alignment fixed
SEG_B = sum((sy(w) for w in WORDS[5:19]), [])         # syllables 25-94 if the damaged pair is 20 letters
SEGS = [(SEG_A, (0,)), (SEG_B, (0, 1))]

def dec(tbl, seg, a, add=0):
    n = [tbl[s] for s in seg]
    return ['%04d' % ((n[i]*100 + n[i+1] + add) % 10000) for i in range(a, len(n)-1, 2)]

def run():
    base = list(CONS); res = []
    for r in range(20):
        for rev in (0, 1):
            co = base[r:] + base[:r]
            if rev: co = co[::-1]
            for vo in itertools.permutations(VOW):
                for fill in ('cons', 'vow'):
                    for off in (0, 1):
                        t = make_table(co, vo, fill, off)
                        for add in (0, 111, -111):
                            tot = 0; txt = []
                            for seg, al in SEGS:
                                b = max(((score_codes(dec(t, seg, a, add)), a) for a in al))
                                tot += b[0]; txt.append(''.join(code2ch.get(c, '□') for c in dec(t, seg, b[1], add)))
                            res.append((tot, ('rev' if rev else 'rot')+str(r), ''.join(vo), fill, off, add, ' | '.join(txt)))
    res.sort(key=lambda x: -x[0])
    import statistics
    s = [x[0] for x in res]
    print('keys', len(res), 'mean %.1f sd %.1f' % (statistics.mean(s), statistics.pstdev(s)))
    for x in res[:12]: print('%.1f %s %s %s off%d add%d  %s' % x)

if __name__ == '__main__':
    base = list(CONS); rot = base[8:] + base[:8]
    t = make_table(rot, list('eaiou'), 'vow', 1)
    for seg, al in SEGS:
        for a in al:
            c = dec(t, seg, a); print('Swatow key, align', a, ' '.join(c)); print('   ', ''.join(code2ch.get(x, '□') for x in c))
    run()
