"""Enumerate every English reading of a Catokwacopa line that the mechanism admits exactly.

For a line (A = 8 May stream, B = 20 May stream) find word sequences P such that an interleaving of A
and B is a subsequence of P, with no misprints allowed. Rank by

    sum over words of  log P(word)                         (unigram, 24 Gutenberg novels + a name list)
                     + log P(source of the word's first letter | consonant/vowel initial)
                     - OMIT * omitted letters

The positional prior is fitted on the seven exact readings nobody disputes (lines 1, 7, 16, 17, 24,
27, 28): consonant-initial words begin in the 8 May stream, vowel-initial words mostly do not.

The point is not to 'solve' a line but to measure it: when the accepted reading comes out on top and
far ahead, the line is determined; when hundreds of readings fit about as well, it is not, and any
reading of it is a guess.

Usage: python search.py LINE [LINE ...]   |   python search.py control
"""
import collections, glob, heapq, math, os, re, sys
from ads import PAIRS

CORPUS = os.path.join('..', 'beale', 'lmcorpus')
OMIT = 2.3                   # log-cost per omitted letter (about one in ten)
MAX_WORD_OMIT = 4
# Names and terms the published readings rely on, which a novel corpus lacks. Given the frequency of an
# uncommon word so that they can appear but are never favoured.
EXTRA = ('conington jowett balliol shirley oxford hertford horace satirs satires qui fit motto mottoes '
         'lecsures lecsurs scholarship examination declaration exam lectures commoner tutor fellow '
         'dean proctor'.split())

PRIOR = {('c', 'A'): math.log(.92), ('c', 'B'): math.log(.04), ('c', '-'): math.log(.04),
         ('v', 'A'): math.log(.35), ('v', 'B'): math.log(.45), ('v', '-'): math.log(.20)}


def vocab(min_count=4):
    cache = 'vocab.tsv'
    if os.path.exists(cache):
        cnt = {w: int(c) for w, c in (l.split('\t') for l in open(cache, encoding='utf-8'))}
    else:
        cnt = collections.Counter()
        for f in glob.glob(os.path.join(CORPUS, '*.txt')):
            cnt.update(re.findall('[a-z]+', open(f, encoding='utf-8', errors='ignore').read().lower()))
        cnt = {w: c for w, c in cnt.items() if c >= min_count and (len(w) > 1 or w in ('a', 'i'))}
        with open(cache, 'w', encoding='utf-8') as fh:
            for w, c in cnt.items(): fh.write('%s\t%d\n' % (w, c))
    for w in EXTRA:
        cnt[w] = max(cnt.get(w, 0), 5)
    tot = sum(cnt.values())
    return {w: math.log(c / tot) for w, c in cnt.items()}


def trie(words):
    root = {}
    for w in words:
        node = root
        for ch in w: node = node.setdefault(ch, {})
        node['$'] = w
    return root


def edges_from(i0, j0, A, B, T):
    """All words that can be read starting at stream positions (i0, j0): (word, i, j, omitted, first_src)."""
    out = []
    stack = [(T, ((i0, j0, 0, None),))]
    while stack:
        node, states = stack.pop()
        if '$' in node:
            w = node['$']
            best = {}
            for i, j, om, src in states:
                if (i, j) != (i0, j0) and om <= len(w) - 1:
                    k = (i, j, src)
                    if k not in best or om < best[k]: best[k] = om
            for (i, j, src), om in best.items():
                out.append((w, i, j, om, src))
        for ch, child in node.items():
            if ch == '$': continue
            nxt = {}
            for i, j, om, src in states:
                first = src is None
                if i < len(A) and A[i] == ch:
                    k = (i + 1, j, 'A' if first else src); nxt[k] = min(nxt.get(k, 99), om)
                if j < len(B) and B[j] == ch:
                    k = (i, j + 1, 'B' if first else src); nxt[k] = min(nxt.get(k, 99), om)
                if om < MAX_WORD_OMIT:
                    k = (i, j, '-' if first else src); nxt[k] = min(nxt.get(k, 99), om + 1)
            if nxt:
                stack.append((child, tuple((i, j, om, s) for (i, j, s), om in nxt.items())))
    return out


def kbest(A, B, LP, T, K=40, per_node=60):
    a, b = len(A), len(B)
    # nodes in order of i+j; each node keeps its best `per_node` partial readings
    best = collections.defaultdict(list)
    best[(0, 0)] = [(0.0, ())]
    order = sorted(((i, j) for i in range(a + 1) for j in range(b + 1)), key=lambda x: x[0] + x[1])
    for (i, j) in order:
        if not best[(i, j)] or (i, j) == (a, b): continue
        for w, ni, nj, om, src in edges_from(i, j, A, B, T):
            kind = 'v' if w[0] in 'aeiou' else 'c'
            s = LP[w] + PRIOR[(kind, src)] - OMIT * om
            lst = best[(ni, nj)]
            for sc, words in best[(i, j)]:
                lst.append((sc + s, words + (w,)))
            if len(lst) > 4 * per_node:
                lst.sort(reverse=True); del lst[per_node:]
    seen, final = set(), []
    for sc, ws in sorted(best[(a, b)], reverse=True):
        if ws not in seen:
            seen.add(ws); final.append((sc, ws))
    return final[:K]


def main(lines, extra=True):
    global EXTRA
    if not extra: EXTRA = []
    LP = vocab(); T = trie(LP)
    for ln in lines:
        A, B = PAIRS[ln - 1]
        res = kbest(A, B, LP, T)
        print('\nline %d  %s / %s' % (ln, A, B))
        for sc, ws in res[:15]:
            print('   %7.1f  %s' % (sc, ' '.join(ws)))
        sys.stdout.flush()


if __name__ == '__main__':
    args = sys.argv[1:]
    extra = '--no-names' not in args
    args = [x for x in args if x != '--no-names']
    if args == ['control']: args = ['1', '7', '16', '17', '24', '27', '28']
    if args == ['all']:
        from ads import LETTER_LINES
        args = [str(x) for x in LETTER_LINES if x != 23]
    main([int(x) for x in args], extra)
