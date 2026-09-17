"""decode2.py - word-lattice decoder for the Bethune cipher, with a bigram LM.

Each cipher token emits letter strings with P(unit|token) from an EM model plus the fixed word signs.
A beam search over word boundaries scores each candidate word with a period-French bigram LM
(bethune/lm.py), backing off to a character 6-gram for words outside the lexicon, so names and rare
spellings can still be read. Code groups (two-digit figures with no key value) pass through as [nn].

usage
  python bethune/decode2.py ct_file [--model em_model_v2.json] [--beam 60]
  python bethune/decode2.py --control      decode every known-plaintext block and score it
"""
import sys, os, json, math, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lm as LMOD
sys.stdout.reconfigure(encoding='utf-8')

MAXWORD  = 15
MINP     = 0.02
MAXALT   = 6
BEAM     = 60
UNK_PEN  = -3.0      # added to the char-LM score of an out-of-lexicon word
UNK_PER  = -0.55     # extra per letter of an out-of-lexicon word
WORD_PEN = -0.4
SPLIT_FIGURES = False   # measured worse; see NOTES.md, kept as an option      # per word, discourages shredding into short words

FIXED = {
    '48': 'cardinal', '17': 'aldobrandin',
    'f,': 'le', 'g,': 'la', "g'": 'la', 'x,': 'que', 'r,': 'par', 'R2,': 'par',
    's:': 'dit', 'S:': 'dit', 't:': 'de', 't.': 'de', 'p:': 'ce', 'p.': 'ce',
    'q,': 'pour', 'q_': 'pour', 'd,': 'ie', 'DL,': 'ie', 'x:': 'et', 'x^': 'et',
    'f:': 'au', 'J': 'bon', 'J,': 'mais', 'r:': 'du', 'a,': 'faict',
    '61': 'qui', '65': 'si', '68': 'tout',
}
# syllable signs: letter strings that join their neighbours inside one word
PARTIAL = {'s,': 'pro', '63': 're', '71': 'tion', 'm,': 'men', 'y:': 'ent'}
LETTERS = 'abcdefghilmnopqrstuxyz'


# visually confusable token families, from the 4x re-reading recorded in NOTES.md; a token's emissions
# are mixed with its family partners' so that a mis-read glyph can still be recovered by context
FAMILIES = [
    ['Cm', 'Cu', 'm', 'x'],
    ['g', 'n', 'y', 'q'],
    ['r', 'R2', 'd'],
    ['Z', 'ff', 'EP', '0'],
    ['f', '+', 't'],
    ['h', 'B', 'S', 'l'],
    ['b', 'e', 'c', '6'],
    ['p', 'T', 'o'],
    ['4', '6', 'u'],
    ['v', 'a', '1'],
]


def widen(model, eps):
    part = {}
    for fam in FAMILIES:
        for t in fam:
            part.setdefault(t, set()).update(x for x in fam if x != t)
    out = {}
    for tok, items in model.items():
        d = {u: p*(1-eps) for u, p in items}
        ps = part.get(tok, ())
        for q in ps:
            for u, p in model.get(q, ()):
                d[u] = d.get(u, 0.0) + eps*p/len(ps)
        out[tok] = sorted(d.items(), key=lambda kv: -kv[1])[:10]
    return out


# ---- figure runs -------------------------------------------------------------------------------
# The cipher writes its figures without separators, and one- and two-figure groups coexist (3, 5, 7, 8
# beside 61, 63, 65, 68, 71, 73). A run such as "6165" can be 61|65, 6|1|65, 61|6|5 ... so a
# transcription that commits to one split bakes an error in. Here every run is expanded into the
# concatenation of the values of each legal split, and the language model picks the split.
FIGVAL = {'61': 'qui', '63': 're', '65': 'si', '68': 'tout', '71': 'tion', '73': 'uostre',
          '48': 'cardinal', '17': 'aldobrandin', '7': 'leroydespaigne'}
MAXSPLIT = 24


def split_run(run, depth=0):
    """all segmentations of a digit run into 1- and 2-figure pieces; yields (pieces, known_count)"""
    if not run:
        yield [], 0
        return
    if depth > 8:
        return
    for k in (2, 1):
        if len(run) >= k:
            head = run[:k]
            for rest, n in split_run(run[k:], depth+1):
                yield [head] + rest, n + (1 if head in FIGVAL else 0)


def run_emissions(run):
    cands = []
    for pieces, known in split_run(run):
        if not pieces:
            continue
        s = ''.join(FIGVAL.get(p, '[' + p + ']') for p in pieces)
        # prefer splits that use known groups, and fewer pieces
        w = (known + 1.0)**2 / (len(pieces)**1.5)
        cands.append((s, w))
    if not cands:
        return [('[' + run + ']', 1.0)]
    agg = {}
    for s, w in cands:
        agg[s] = max(agg.get(s, 0.0), w)
    tot = sum(agg.values())
    out = sorted(((s, w/tot) for s, w in agg.items()), key=lambda kv: -kv[1])[:MAXSPLIT]
    return out


def merge_figures(tokens):
    """join adjacent pure-figure tokens back into one run so the split can be re-decided"""
    out = []
    for t in tokens:
        if re.fullmatch(r'\d+', t) and out and re.fullmatch(r'\d+', out[-1]):
            out[-1] = out[-1] + t
        else:
            out.append(t)
    return out


def load_model(path):
    m = json.load(open(path, encoding='utf-8'))
    out = {}
    for tok, d in m.items():
        items = sorted(((u if u != '-' else '', p) for u, p in d.items()), key=lambda x: -x[1])
        items = [(u, p) for u, p in items if p >= MINP][:MAXALT]
        if items:
            out[tok] = items
    return out


def emissions(tok, model):
    if SPLIT_FIGURES and re.fullmatch(r'\d+', tok) and len(tok) > 2:
        return run_emissions(tok)          # a merged run: let the language model choose the split
    if tok in FIXED:   return [(FIXED[tok], 1.0)]
    if tok in PARTIAL: return [(PARTIAL[tok], 1.0)]
    if tok in model:   return model[tok]
    if re.fullmatch(r"\d+", tok):        return [('[' + tok + ']', 1.0)]
    if re.fullmatch(r"\d+[.,:^_]", tok): return [('[' + tok + ']', 1.0)]
    return [(c, 1.0/len(LETTERS)) for c in LETTERS]


class Trie:
    __slots__ = ('ch', 'w')
    def __init__(self):
        self.ch = {}; self.w = None


def build_trie(vocab):
    root = Trie()
    for w in vocab:
        n = root
        for c in w:
            n = n.ch.setdefault(c, Trie())
        n.w = w
    return root


def decode(tokens, model, lm, trie, beam=BEAM, unk_pen=UNK_PEN):
    # the doubling sign repeats the previous token
    toks = [tokens[i-1] if (t == 'PH' and i > 0) else t for i, t in enumerate(tokens)]
    if SPLIT_FIGURES:
        toks = merge_figures(toks)
    n = len(toks)
    em = [emissions(t, model) for t in toks]
    states = [dict() for _ in range(n+1)]
    states[0]['<s>'] = (0.0, -1, None, None)
    for i in range(n):
        if not states[i]:
            continue
        states[i] = dict(sorted(states[i].items(), key=lambda kv: -kv[1][0])[:beam])
        cands = []
        stack = [(trie, i, 0.0, '')]
        guard = 0
        while stack and guard < 60000:
            guard += 1
            node, j, lp, s = stack.pop()
            if node.w is not None and j > i:
                cands.append((j, node.w, lp))
            if j >= n or len(s) >= MAXWORD:
                continue
            for u, p in em[j]:
                if u.startswith('['):
                    continue
                if u == '':
                    stack.append((node, j+1, lp+math.log(p)-0.7, s)); continue
                nd = node; ok = True
                for c in u:
                    nd = nd.ch.get(c)
                    if nd is None:
                        ok = False; break
                if ok:
                    stack.append((nd, j+1, lp+math.log(p), s+u))
        # out-of-lexicon word: greedy best letters
        lp = 0.0; s = ''
        for j in range(i, min(n, i+10)):
            alts = [(u, p) for u, p in em[j] if not u.startswith('[')]
            if not alts:
                break
            u, p = alts[0]
            lp += math.log(p); s += u
            if len(s) >= 2:
                cands.append((j+1, '~'+s, lp))
        for u, p in em[i]:
            if u.startswith('['):
                cands.append((i+1, u, math.log(p)))
        for j, w, elp in cands:
            if w.startswith('~'):
                word = w[1:]; key = word; wlp = lm.logp_char(word) + unk_pen + UNK_PER*len(word)
            elif w.startswith('['):
                word = w; key = w; wlp = -6.0
            else:
                word = w; key = w; wlp = None
            for prev, st in states[i].items():
                lp_w = wlp if wlp is not None else lm.logp_bi(prev, word)
                tot = st[0] + elp + lp_w + WORD_PEN
                cur = states[j].get(key)
                if cur is None or tot > cur[0]:
                    states[j][key] = (tot, i, prev, word)
    if not states[n]:
        return None, []
    bw = max(states[n].items(), key=lambda kv: kv[1][0])[0]
    words = []; i = n; key = bw
    while i > 0:
        sc, pi, pw, pe = states[i][key]
        words.append(pe); i = pi; key = pw
    return states[n][bw][0], words[::-1]


def lev_acc(a, b):
    """letters of b recovered by a, by Levenshtein alignment"""
    n, m = len(a), len(b)
    prev = list(range(m+1))
    for i in range(1, n+1):
        cur = [i] + [0]*m
        ca = a[i-1]
        for j in range(1, m+1):
            cur[j] = min(prev[j]+1, cur[j-1]+1, prev[j-1] + (ca != b[j-1]))
        prev = cur
    return m - prev[m] if prev[m] <= m else 0, m


def main():
    model_path = 'bethune/em_model_v2.json'
    if '--model' in sys.argv:
        model_path = sys.argv[sys.argv.index('--model')+1]
    beam = int(sys.argv[sys.argv.index('--beam')+1]) if '--beam' in sys.argv else BEAM
    model = load_model(model_path)
    if '--wide' in sys.argv:
        model = widen(model, float(sys.argv[sys.argv.index('--wide')+1]))
    lm = LMOD.load()
    vocab = [w for w, c in lm.uni.items() if w != '<s>' and (c >= 2 or len(w) > 6)]
    trie = build_trie(vocab)
    print('# model %s  vocab %d  beam %d' % (model_path, len(vocab), beam), file=sys.stderr)
    if '--control' in sys.argv:
        tot_ok = tot_n = 0; tot_lok = tot_ln = 0
        for line in open('bethune/corpus_v2.txt', encoding='utf-8'):
            if line.startswith('#') or '|' not in line:
                continue
            p = [x.strip() for x in line.split('|')]
            lab, ct, truth = p[0], p[2], LMOD.norm_keep_spaces(p[3])
            sc, words = decode(ct.split(), model, lm, trie, beam)
            got = ' '.join(words)
            tw = truth.split(); gw = got.split()
            ok = sum(1 for a, b in zip(tw, gw) if a == b)
            L_ok, L_n = lev_acc(''.join(gw), ''.join(tw))
            tot_lok += L_ok; tot_ln += L_n
            tot_ok += ok; tot_n += len(tw)
            print('%-3s %3d/%3d  %s' % (lab, ok, len(tw), got))
            print('    truth: %s' % truth)
        print('\nTOTAL exact-position word accuracy %d/%d = %.1f%%' % (tot_ok, tot_n, 100.0*tot_ok/tot_n))
        return
    ctf = [a for a in sys.argv[1:] if a.endswith('.txt')][0]
    for line in open(ctf, encoding='utf-8'):
        if line.startswith('#') or not line.strip():
            continue
        p = [x.strip() for x in line.split('|')]
        lab = p[0]; ct = p[2] if len(p) >= 4 else p[-1]
        sc, words = decode(ct.split(), model, lm, trie, beam)
        print('%-6s %9.1f | %s' % (lab, sc if sc else 0, ' '.join(words)))


if __name__ == '__main__':
    main()
