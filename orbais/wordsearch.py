"""For each open cipher group of fr. 3413 no. 62, list 1-3 word French sequences consistent with
(a) glyphs already fixed by cribs, (b) same glyph -> same letter, (c) different glyphs may share a letter
(homophones), optional nulls for glyphs in NULLOK. Lexicon = the period corpus used for raince's LM."""
import re, glob, unicodedata, collections, sys, math
def norm(t):
    t = unicodedata.normalize('NFD', t.lower()); t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return t.replace('j', 'i').replace('v', 'u').replace('w', 'u')
files = (glob.glob('../dubellay/ref/legrand3_*.txt') + glob.glob('../nevers1593/*.txt') + glob.glob('../debosnys/corpus/fr*.txt'))
cnt = collections.Counter()
for f in files:
    cnt.update(re.findall(r"[a-z]+", norm(open(f, encoding='utf-8', errors='ignore').read())))
words = {w: c for w, c in cnt.items() if c >= 3 and len(w) <= 14}
tot = sum(words.values())
FIX = dict(W='c', V='a', S='s', I9='i', N='n', R='r', O='o', OOO='t', E='e', M='o', B='p', C8='t', PHI2='i', U='u',
           HH='n', Z2='b', ETA='g', DASH='a')
NULLOK = {'X'}
GROUPS = {
 'S1':  'B ONE SIX E S | W H4 X R DASH T',
 'S2':  'F3 D3 O HH E N',
 'C':   'PHI O P V X T S',
 'Fend':'NA X ETA N E',
 'G':   'MR F3 TAU X E N NABLA V I9 OOO N E',
 'H':   'T U E PHI U N ETA DASH SEVEN SIX PHI Z2',
 'I':   'W E N E I9 R X X',
}
byfirst = collections.defaultdict(list)
for w, c in words.items(): byfirst[w[0]].append((w, c))
def search(glyphs, maxw=3, top=25):
    out = []
    def rec(i, m, seq, lp):
        if i == len(glyphs):
            out.append((lp, ' '.join(seq))); return
        if len(seq) >= maxw: return
        for w, c in words_iter(glyphs[i]):
            if i + len(w) > len(glyphs): continue
            m2 = dict(m); ok = True
            for k, ch in enumerate(w):
                g = glyphs[i+k]
                if g in FIX and FIX[g] != ch: ok = False; break
                if m2.get(g, ch) != ch: ok = False; break
                m2[g] = ch
            if ok: rec(i+len(w), m2, seq+[w], lp+math.log(c/tot))
    def words_iter(g):
        if g in FIX: return byfirst[FIX[g]]
        return words.items()
    rec(0, {}, [], 0.0)
    out.sort(reverse=True); return out[:top]
if __name__ == '__main__':
    for k in (sys.argv[1:] or GROUPS):
        gl = GROUPS[k].replace('|', '').split()
        variants = [gl] + ([[g for g in gl if not (g in NULLOK)]] if any(g in NULLOK for g in gl) else [])
        print('==', k, GROUPS[k])
        for v in variants:
            for lp, s in search(v, maxw=3 if len(v) < 12 else 4): print('  %7.1f  %s' % (lp, s))
            print('  --')
