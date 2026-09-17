"""Score alternative readings of a no. 46 cipher line.

For a line of tokens (see decode46.py conventions) the single digits 0 and 1 may be intercalated nulls or part of a
two-digit group; this script enumerates those choices (and optional 0/8 swaps marked as '0?8'), decodes each, and
scores the letter string by a lexicon-based word segmentation (old-French corpora in ../bordeaux and ../chaulnes,
normalised u/v, i/j). Prints the best readings.
Usage: python segscore.py "88: 38_ 29 42 74 32 69 66 9 1 5 79 15"
"""
import sys, re, math, pathlib, itertools, collections
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE))
from decode46 import KEY

def load_lex():
    cnt = collections.Counter()
    for p in [HERE.parent / 'bordeaux' / 'corpus_fr.txt', HERE.parent / 'chaulnes' / 'corpus_fr.txt']:
        if p.exists():
            for w in re.findall(r"[a-zàâäéèêëîïôöùûüç]+", p.read_text(encoding='utf-8', errors='ignore').lower()):
                w = norm(w)
                if 1 <= len(w) <= 16:
                    cnt[w] += 1
    # old spellings that the modern corpora lack
    for w in 'quil quelle lon nay ny ayt soyt soit estoit estoyt feroit resons pluseurs come receu ambassadeur pape roy luy ay cest sest doibt voloit vouloit sil quon nen sen jay jen ceste cest dict faict faire mesme asseurer asseure secret segret bien besoin declarans charge'.split():
        cnt[norm(w)] += 50
    return cnt

def norm(w):
    w = w.replace('v', 'u').replace('j', 'i')
    w = re.sub(r'[àâä]', 'a', w); w = re.sub(r'[éèêë]', 'e', w); w = re.sub(r'[îï]', 'i', w)
    w = re.sub(r'[ôö]', 'o', w); w = re.sub(r'[ùûü]', 'u', w); w = w.replace('ç', 'c')
    return w

LEX = None
def word_score(s):
    """Best segmentation log-score of letter string s (nomenclator words already separated by |)."""
    global LEX
    if LEX is None:
        LEX = load_lex()
    total = sum(LEX.values())
    def seg(t):
        n = len(t); best = [(-1e9, None)] * (n + 1); best[0] = (0.0, None)
        for i in range(1, n + 1):
            for j in range(max(0, i - 16), i):
                w = t[j:i]
                if w in LEX:
                    sc = best[j][0] + math.log(LEX[w] / total) + 1.5
                else:
                    if i - j == 1:
                        sc = best[j][0] - 9.0
                    else:
                        continue
                if sc > best[i][0]:
                    best[i] = (sc, j)
        i = n; words = []
        while i > 0:
            j = best[i][1]; words.append(t[j:i]); i = j
        return best[n][0], ' '.join(reversed(words))
    score = 0.0; out = []
    for part in s.split('|'):
        if part.startswith('<'):
            out.append(part); score += 2.0
        elif part:
            sc, ws = seg(part); score += sc; out.append(ws)
    return score, ' '.join(out)

def decode_seq(tokens):
    """tokens: list of (fig, mark). Returns string with '|' separating nomenclator items."""
    parts = []; cur = ''
    for fig, mark in tokens:
        f = str(int(fig))
        if mark == '_':
            v = KEY.get(('B', f), '?B' + f)
            parts.append(cur); parts.append('<' + v + '>'); cur = ''
        elif mark == ':':
            v = KEY.get(('D', f), '?D' + f)
            parts.append(cur); parts.append('<' + v + '>'); cur = ''
        else:
            if ('A', f) in KEY:
                cur += KEY[('A', f)]
            elif ('N', f) in KEY:
                pass
            elif ('P', f) in KEY:
                parts.append(cur); parts.append('<' + KEY[('P', f)] + '>'); cur = ''
            else:
                cur += '?'
    parts.append(cur)
    return '|'.join(parts)

def variants(line):
    """Enumerate readings: digits in plain runs re-paired with optional deletion of 0/1 singles."""
    raw = line.split()
    # group into runs of plain digits and marked tokens
    items = []
    for t in raw:
        m = re.fullmatch(r'(\d+)([_:]?)', t)
        if not m:
            continue
        if m.group(2):
            items.append(('M', m.group(1), m.group(2)))
        else:
            if items and items[-1][0] == 'R':
                items[-1] = ('R', items[-1][1] + m.group(1), '')
            else:
                items.append(('R', m.group(1), ''))
    def run_options(d):
        # positions of 0/1 that may be dropped
        idx = [i for i, c in enumerate(d) if c in '01']
        opts = set()
        for r in range(0, min(len(idx), 4) + 1):
            for drop in itertools.combinations(idx, r):
                s = ''.join(c for i, c in enumerate(d) if i not in drop)
                if len(s) % 2 == 0:
                    opts.add(tuple((s[i:i + 2], '') for i in range(0, len(s), 2)))
        return list(opts)
    pools = []
    for kind, d, mk in items:
        if kind == 'M':
            pools.append([((d, mk),)])
        else:
            o = run_options(d)
            pools.append(o if o else [tuple()])
    for combo in itertools.product(*pools):
        toks = [t for grp in combo for t in grp]
        yield toks

if __name__ == '__main__':
    line = sys.argv[1]
    res = []
    for toks in variants(line):
        s = decode_seq(toks)
        if '?' in s:
            continue
        sc, ws = word_score(s)
        res.append((sc, ws, ' '.join(f + m for f, m in toks)))
    res.sort(reverse=True)
    for sc, ws, tk in res[:8]:
        print(f'{sc:8.1f}  {ws}\n          {tk}')
