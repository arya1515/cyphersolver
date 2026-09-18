import sys, math
from wordsearch import words, tot, byfirst, GROUPS, FIX as FIX0
# Tomokiyo key values (letters a glyph may take); used as bonus, not as constraint
KEY = dict(X='e', T='t', PHI='u', P='p', ETA='g', H4='h', D3='d', NABLA='m', ONE='l', B='u', SIX='', F3='', TAU='',
           MR='', SEVEN='', U='u', E='e', NA='r')
FIX = dict(W='c', V='a', S='s', I9='i', N='n', R='r', O='o', OOO='t', E='e', M='o', C8='t', PHI2='i', HH='n', Z2='b', NA='r')
def search(glyphs, maxw, top=30):
    out = []
    def rec(i, m, seq, lp):
        if i == len(glyphs):
            agree = sum(1 for g, ch in m.items() if KEY.get(g) == ch and g not in FIX)
            out.append((lp + 3.0*agree, agree, ' '.join(seq))); return
        if len(seq) >= maxw: return
        cands = byfirst[m[glyphs[i]]] if glyphs[i] in m else (byfirst[FIX[glyphs[i]]] if glyphs[i] in FIX else words.items())
        for w, c in cands:
            if i + len(w) > len(glyphs): continue
            m2 = dict(m); ok = True
            for k, ch in enumerate(w):
                g = glyphs[i+k]
                if g in FIX and FIX[g] != ch: ok = False; break
                if m2.get(g, ch) != ch: ok = False; break
                m2[g] = ch
            if ok: rec(i+len(w), m2, seq+[w], lp+math.log(c/tot))
    rec(0, {}, [], 0.0)
    out.sort(reverse=True); return out[:top]
G = dict(GROUPS)
G['I'] = 'W E N E I9 R X X'; G['I2'] = 'W E N E I9 R'; G['I3'] = 'W HH N E I9 R'
G['C2'] = 'PHI O P V T S'
for k in sys.argv[1:]:
    gl = G[k].replace('|', '').split(); print('==', k, G[k])
    for s, a, t in search(gl, 3 if len(gl) < 12 else 4): print('  %6.1f %d  %s' % (s, a, t))
