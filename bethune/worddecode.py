"""Lexicon-driven noisy-channel decoder for the Béthune cipher.
Cipher tokens emit letter strings with P(unit|token) from em_model.json (plus fixed word signs). Words come from a
trie built on the Xivrey volumes (Henri IV's letters, 1590s-1600s spelling) plus a list of names of the moment.
DP over token positions: best[i] = best score of a segmentation of tokens[:i] into words; extend by walking the trie
through the emission alternatives of tokens i, i+1, ... A word may also be an 'unknown' spelled letter by letter at
a heavy per-letter penalty, so that no line is left undecoded.  usage: python worddecode.py ct_file [--top K]"""
import sys, json, math, re, collections, unicodedata, glob
sys.stdout.reconfigure(encoding='utf-8')
MAXWORD = 14
UNK_LETTER = -7.0            # per letter of an out-of-lexicon word
MINP = 0.03                  # ignore emission alternatives below this
NAMES = '''aldobrandin ossat espaigne espagne naples milan sauoye sauoie biron rome pape cardinal cardinaux
rochepot fresnes uenise florence ferrare mirande modene fuentes archiduc infante roy royne dauphin duc ducs comte
mantoue parme lorraine geneue berne suisses turin piedmont montferrat gennes genes sicile portugal flandres
anglois angleterre escosse irlande hollandois pays bas ostende nimegue cardinalat legat legation nonce consistoire
conclaue promotion pension pensionnaire ligue liguez confederez alliez armee armes galeres soldats gens
sillery uilleroy rosny bethune canaye brulart ambassadeur ambassade secretaire'''.split()

def norm(s):
    s = unicodedata.normalize('NFKD', s.lower()); s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.replace('j','i').replace('v','u').replace('œ','oe').replace('æ','ae')
    return re.sub(r'[^a-z]', '', s)

def build_lexicon(paths):
    cnt = collections.Counter()
    for p in paths:
        txt = open(p, encoding='utf-8', errors='ignore').read()
        for w in re.findall(r"[A-Za-zÀ-ÿ]+", txt):
            w2 = norm(w)
            if 1 <= len(w2) <= MAXWORD: cnt[w2] += 1
    for w in NAMES: cnt[norm(w)] += 20
    # drop OCR junk: single letters other than a, y, o; rare 2-3 letter words
    lex = {}
    for w, c in cnt.items():
        if len(w) == 1 and w not in 'ayo': continue
        if len(w) <= 3 and c < 4: continue
        if c < 2: continue
        lex[w] = c
    return lex

class Trie:
    __slots__ = ('ch', 'word')
    def __init__(self): self.ch = {}; self.word = None
def build_trie(lex):
    root = Trie()
    for w in lex:
        n = root
        for c in w: n = n.ch.setdefault(c, Trie())
        n.word = w
    return root

def load_model(path='bethune/em_model.json'):
    m = json.load(open(path, encoding='utf-8'))
    return {tok: {(u if u != '-' else ''): p for u, p in d.items() if p >= MINP} for tok, d in m.items()}

FIXED = {'48': {'cardinal': 1.0}, '17': {'aldobrandin': 1.0}, 'f,': {'le': 1.0}, 'x,': {'que': 1.0}, 'r,': {'par': 1.0},
         'g,': {'la': 1.0}, '61': {'qui': 1.0}, '63': {'re': 1.0}, 'x:': {'et': 1.0}, 'x^': {'et': 1.0}, 'd,': {'ie': 1.0},
         'DL,': {'ie': 1.0}, '65': {'si': 1.0}, 's,': {'pro': 1.0}, 't:': {'de': 1.0}, 't.': {'de': 1.0}, 'p:': {'ce': 1.0},
         'q,': {'pour': 1.0}, 's:': {'dit': 1.0}, 'J,': {'mais': 1.0}}
LETTERS = 'abcdefghilmnopqrstuxyz'

def emissions(tok, model):
    if tok in FIXED: return FIXED[tok]
    if tok in model: return model[tok]
    if any(ch.isdigit() for ch in tok): return {f'[{tok}]': 1.0}
    return {c: 1.0/22 for c in LETTERS}

def decode(tokens, model, trie, lex, total, topk=1):
    n = len(tokens)
    em = [emissions(t, model) for t in tokens]
    best = [None]*(n+1); best[0] = (0.0, None, None)      # (score, prev_index, word)
    logtot = math.log(total)
    for i in range(n):
        if best[i] is None: continue
        base = best[i][0]
        # --- 1. dictionary words via trie walk (also fixed multi-letter signs land here as whole words)
        # stack: (trie node, token index j, emission logp so far, string so far)
        stack = [(trie, i, 0.0, '')]
        while stack:
            node, j, lp, s = stack.pop()
            if node.word is not None and j > i:
                sc = base + lp + math.log(lex[node.word]) - logtot
                if best[j] is None or sc > best[j][0]: best[j] = (sc, i, node.word)
            if j >= n or len(s) >= MAXWORD: continue
            for u, p in em[j].items():
                if u.startswith('['): continue
                if u == '':                                   # null token: stay in place in the trie
                    if j+1 <= n: stack.append((node, j+1, lp + math.log(p) - 1.0, s))
                    continue
                nd = node; ok = True
                for c in u:
                    nd = nd.ch.get(c)
                    if nd is None: ok = False; break
                if ok: stack.append((nd, j+1, lp + math.log(p), s+u))
        # --- 2. word-sign / bracket tokens as their own words
        for u, p in em[i].items():
            if u.startswith('['):
                sc = base + math.log(p) - 4.0
                if best[i+1] is None or sc > best[i+1][0]: best[i+1] = (sc, i, u)
        # --- 3. unknown word: best single-letter chain of length 1..6 (fallback)
        for L in range(1, 7):
            if i+L > n: break
            lp = 0.0; s = ''
            for j in range(i, i+L):
                cands = [(u, p) for u, p in em[j].items() if not u.startswith('[')]
                if not cands: lp = None; break
                u, p = max(cands, key=lambda x: x[1]); lp += math.log(p); s += u
            if lp is None or not s: continue
            sc = base + lp + UNK_LETTER*len(s) - 3.0
            if best[i+L] is None or sc > best[i+L][0]: best[i+L] = (sc, i, s.upper())
    if best[n] is None: return None, []
    words = []; i = n
    while i > 0:
        sc, pi, w = best[i]; words.append(w); i = pi
    return best[n][0], words[::-1]

def main():
    ctf = sys.argv[1]
    model = load_model()
    lex = build_lexicon(glob.glob('bethune/xivrey/*.txt')); total = sum(lex.values())
    trie = build_trie(lex)
    lines = [l for l in open(ctf, encoding='utf-8') if l.strip() and not l.startswith('#')]
    for l in lines:
        parts = [x.strip() for x in l.split('|')]
        lab, ct = parts[0], (parts[2] if len(parts) >= 4 else parts[1])
        toks = ct.replace('s: 4 8', 's: 48').replace('f s 4 8', 'f s 48').split()
        sc, words = decode(toks, model, trie, lex, total)
        print(f'{lab:5s} {sc if sc is not None else 0:8.1f} | ' + ' '.join(words))
if __name__ == '__main__':
    main()
