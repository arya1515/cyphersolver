"""Second pass: for each cipher token take the top-K readings from the quadgram beam (decode.py), then rescore each by
its best segmentation into words of period French (matignon1586/corpus_words.txt, u/v and i/j folded). Picks the
reading whose words are most French; unknown stretches pay a per-letter penalty."""
import math, re, functools
import decode as D
W = {}
for l in open('../matignon1586/corpus_words.txt', encoding='utf-8'):
    w, n = l.split('\t'); W[w] = int(n)
TOT = sum(W.values())
def norm(s): return s.lower().replace('v', 'u').replace('j', 'i')
def segscore(s):
    s = norm(s); n = len(s)
    @functools.lru_cache(None)
    def f(i):
        if i == n: return (0.0, ())
        best = (-1e9, ())
        for j in range(i + 1, min(n, i + 16) + 1):
            w = s[i:j]
            sc = math.log10(W[w] / TOT) if w in W and (len(w) > 1 or w in 'ay') else -3.5 * (j - i) - 2
            r = f(j); cand = (sc + r[0], (w,) + r[1])
            if cand[0] > best[0]: best = cand
        return best
    return f(0)
def topk(run, ctx, K=300, B=600):
    beams = [(0.0, ctx, '')]
    for ch in run:
        nb = {}
        for s, c, o in beams:
            for p in D.KEY.get(ch, '?'):
                s2 = s + (D.lp((c + p.lower())[-4:]) if len(c) == 3 else 0) + D.PRIOR.get((ch, p), 0)
                c2 = (c + p.lower())[-3:]; k = o + p
                if k not in nb or nb[k][0] < s2: nb[k] = (s2, c2, k)
        beams = sorted(nb.values(), key=lambda x: -x[0])[:B]
    return beams[:K]
out = []
for line in open('transcription.txt', encoding='utf-8'):
    line = line.rstrip('\n')
    if line.startswith('#'): continue
    if line.startswith('=='): out.append('\n' + line); continue
    ctx, res = '   ', []
    for part in re.split(r'(\[[^\]]*\])', line):
        if part.startswith('['):
            res.append(part[1:-1].lower()); ctx = ('   ' + re.sub('[^a-z]', '', part[1:-1].lower()))[-3:]; continue
        for tok in part.split():
            cands = topk(tok, ctx)
            best = max(cands, key=lambda b: 0.5 * b[0] + segscore(b[2])[0])
            res.append(' '.join(segscore(best[2])[1]).upper()); ctx = best[1]
    out.append(' '.join(res))
txt = '\n'.join(out); open('decoded.txt', 'w', encoding='utf-8').write(txt + '\n'); print(txt)
