"""Monogram hypothesis: each glyph is a stack of marks, each mark a letter (unordered within the glyph).

Hill-climb a mark -> letter key against a letter quadgram model, letting each glyph's letters take the best
order given the preceding letters. Real glyph order must beat a control in which the same glyphs are shuffled
between positions (composition kept, sequence destroyed); if it does not, the sequence carries no
letter-level language under this reading.

Usage: python monogram.py fr|en [restarts]
"""
import collections, glob, itertools, math, os, random, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from verse_transcription import lines
from marks import decompose

AL = 'abcdefghijklmnopqrstuvwxyz'


def quadgrams(lang):
    cache = os.path.join(HERE, 'corpus', 'q4_%s.tsv' % lang)
    if os.path.exists(cache):
        d = {k: float(v) for k, v in (l.split('\t') for l in open(cache, encoding='utf-8'))}
        return d, d.pop('__floor__')
    files = glob.glob(os.path.join(HERE, 'corpus', 'fr*.txt' if lang == 'fr' else 'pg*.txt'))
    cnt = collections.Counter()
    tr = str.maketrans('àâäéèêëîïôöûùüÿçœ', 'aaaeeeeiioouuuyco')
    for f in files:
        t = open(f, encoding='utf-8', errors='ignore').read().lower().translate(tr)
        t = re.sub('[^a-z]', '', t)
        for i in range(len(t) - 3): cnt[t[i:i + 4]] += 1
    tot = sum(cnt.values())
    d = {k: math.log10(v / tot) for k, v in cnt.items()}
    floor = math.log10(0.01 / tot)
    with open(cache, 'w', encoding='utf-8') as fh:
        for k, v in d.items(): fh.write('%s\t%f\n' % (k, v))
        fh.write('__floor__\t%f\n' % floor)
    return d, floor


def glyph_marks():
    out = []
    for l in lines():
        row = []
        for g in l:
            d = decompose(g)
            if d: row.append(tuple(d))
        out.append(row)
    return out


class Scorer:
    def __init__(self, lang):
        self.q, self.floor = quadgrams(lang)

    def text(self, rows, key):
        s = 0.0
        for row in rows:
            ctx = ''
            for marks in row:
                letters = [key[m] for m in marks]
                best, bl = None, None
                for perm in set(itertools.permutations(letters)):
                    t = ctx[-3:] + ''.join(perm); v = 0.0
                    for i in range(max(0, 4 - len(ctx[-3:])) and 0, len(t) - 3):
                        v += self.q.get(t[i:i + 4], self.floor)
                    if best is None or v > best: best, bl = v, ''.join(perm)
                ctx += bl
            s += sum(self.q.get(ctx[i:i + 4], self.floor) for i in range(len(ctx) - 3))
        return s

    def decode(self, rows, key):
        out = []
        for row in rows:
            ctx = ''
            for marks in row:
                letters = [key[m] for m in marks]
                best, bl = None, None
                for perm in set(itertools.permutations(letters)):
                    t = ctx[-3:] + ''.join(perm)
                    v = sum(self.q.get(t[i:i + 4], self.floor) for i in range(len(t) - 3))
                    if best is None or v > best: best, bl = v, ''.join(perm)
                ctx += bl
            out.append(ctx)
        return out


CAP = collections.Counter({c: 1 for c in AL})
CAP.update({'e': 3, 'a': 1, 'i': 1, 'n': 1, 'o': 1, 'r': 1, 's': 1, 't': 1, 'l': 1, 'u': 1, 'd': 1, 'h': 1, 'c': 1, 'm': 1, 'p': 1})


def climb(rows, sc, rnd, iters=5000):
    """Key under a capacity constraint: each letter may take at most CAP[letter] marks (a near-bijection
    with room for a few homophones), so the climber cannot collapse everything onto e, t and s."""
    marks = sorted({m for row in rows for g in row for m in g})
    pool = [c for c in AL for _ in range(CAP[c])]
    rnd.shuffle(pool)
    key = dict(zip(marks, pool)); spare = pool[len(marks):]
    cur = sc.text(rows, key)
    for it in range(iters):
        if rnd.random() < 0.6 or not spare:
            a, b = rnd.sample(marks, 2)
            key[a], key[b] = key[b], key[a]
            v = sc.text(rows, key)
            if v >= cur: cur = v
            else: key[a], key[b] = key[b], key[a]
        else:
            a = rnd.choice(marks); k = rnd.randrange(len(spare))
            key[a], spare[k] = spare[k], key[a]
            v = sc.text(rows, key)
            if v >= cur: cur = v
            else: key[a], spare[k] = spare[k], key[a]
    return cur, dict(key)


def main():
    lang = sys.argv[1]; restarts = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    sc = Scorer(lang)
    rows = glyph_marks()
    n = sum(len(m) for row in rows for m in row)
    flat = [g for row in rows for g in row]
    best_real = max((climb(rows, sc, random.Random(r)) for r in range(restarts)), key=lambda x: x[0])
    ctrl = []
    for r in range(restarts):
        f = list(flat); random.Random(100 + r).shuffle(f); k = 0; R = []
        for row in rows: R.append(f[k:k + len(row)]); k += len(row)
        ctrl.append(climb(R, sc, random.Random(r))[0])
    print('%s: %d marks; real order best %.0f (%.3f per mark); shuffled controls %s'
          % (lang, n, best_real[0], best_real[0] / n, ['%.0f' % c for c in ctrl]))
    for l in sc.decode(rows, best_real[1])[:6]: print('   ', l)


if __name__ == '__main__':
    main()
