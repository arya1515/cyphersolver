"""Six-vowel condenser family (a e i o u y) for the June 1917 telegrams (frames 0509, 0511).
Consonant set: the letters seen in consonant position, alphabetical, rotated/reversed; vowels any order;
cells numbered vowel-major or consonant-major, from 0 or 1, taken mod 100."""
import sys, os, io, itertools, statistics
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from family import code2ch, score_codes
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
V6 = 'aeiouy'
TEXTS = {
 '0511': "mukoacyobe myzoasdoke catejidoke yokigeleyi liriopen duricidule kohokycuee kuxomifumu hutadynyyg capakazuye mycykafevu damoumhosy cydicapayo benyzoac hinucuge rifyjabo mahykagica fegajiriby jomoaxfojy micycoteco fuhodijige cafemigymu pokycekige rudubyrijo jorinimafy fojylisiby mikypomice miyaminoma fykazokipa",
 '0509': "lidajysamy vemucayri mevecafema pokelutazi riyecafafi cymefymeca madamymiri pujihokehe"}
def segs_of(text, cons):
    segs, cur, pos = [], [], 0
    for w in text.split():
        ok = len(w) == 10 and all(w[i] in cons and w[i+1] in V6 for i in range(0, 10, 2))
        if ok:
            if not cur: st = pos
            cur += [w[i:i+2] for i in range(0, 10, 2)]
        elif cur: segs.append((st, cur)); cur = []
        pos += len(w) // 2
    if cur: segs.append((st, cur))
    return segs
def run(key, cons_set):
    segs = segs_of(TEXTS[key], set(cons_set))
    base = sorted(cons_set); n = len(base); res = []
    for r in range(n):
        for rev in (0, 1):
            co = base[r:] + base[:r]
            if rev: co = co[::-1]
            for vo in itertools.permutations(V6):
                for fill in ('vow', 'cons'):
                    for off in (0, 1):
                        t = {c + v: ((6*ci + vi if fill == 'cons' else n*vi + ci) + off) % 100
                             for ci, c in enumerate(co) for vi, v in enumerate(vo)}
                        tot = 0; txt = []
                        for k, (st, seg) in enumerate(segs):
                            nums = [t[s] for s in seg]
                            best = None
                            for a in ((0,) if st == 0 else (0, 1)):
                                codes = ['%02d%02d' % (nums[i], nums[i+1]) for i in range(a, len(nums)-1, 2)]
                                sc = score_codes(codes)
                                if best is None or sc > best[0]: best = (sc, codes)
                            tot += best[0]; txt.append(''.join(code2ch.get(c, '□') for c in best[1]))
                        res.append((tot, '%s%d %s %s off%d' % ('rev' if rev else 'rot', r, ''.join(vo), fill, off), ' | '.join(txt)))
    s = [x[0] for x in res]; mu, sd = statistics.mean(s), statistics.pstdev(s)
    res.sort(key=lambda x: -x[0])
    print(key, ''.join(base), 'keys', len(res), 'mean %.1f sd %.1f' % (mu, sd))
    for x in res[:6]: print('  %.1f z=%.1f %s  %s' % (x[0], (x[0]-mu)/sd, x[1], x[2]))
if __name__ == '__main__':
    for cs in ('bcdfghjklmnprstvz', 'bcdfghjklmnprstvxz'):
        run('0511', cs)
