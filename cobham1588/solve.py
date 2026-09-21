"""Candidate-set solver for the Cobham cipher runs (runs.txt).

Each sign stands for a set of letters (from signs.tsv). For every cipher word, enumerate the letter strings it
can spell, normalise Elizabethan spelling (u/v, i/j/y, doubled letters, final e), and keep those found in a word
list of 1588 diplomatic English (wordfreq.tsv, built from CSP Foreign vol. 21 pt 4 and the glossed plaintext).
Candidates are ranked by corpus frequency. Context choice is left to the reader: the output lists each run with
its clear text around it.

    python solve.py            # all runs
    python solve.py f88        # runs whose id starts with f88
    python solve.py --build <corpus.txt>...   # rebuild wordfreq.tsv
"""
import itertools, re, sys, collections, os

HERE = os.path.dirname(os.path.abspath(__file__))
SETS = {
    'U': 'a', 'A': 'sta', '+': 'b', '8': 'c', 'D': 'd', 'T': 'dt', '7': 'e', 'H': 'f', 'G': 'g', 'h': 'h',
    'I': 'iay', 'k': 'k', 'l': 'lt', 'm': 'm', '#': 'mn', 'n': 'n', 'z': 'o', 'd': 'od', 'c': 'oae', 'p': 'p',
    'V': 'r', 'y': 'ry', ':': 'uv', 'w': 'w', 'X': 'i', 'L': 'e', 'K': 'abcdefghiklmnoprstuwy', '?': 'abcdefghiklmnoprstuwy',
}
GLOSSED = """infante maior mobility of this their great desir country discours sent from upon our arrival willing
to harken by the clergy they made means popes legat and divers newe sworne perform warres given out al for
cardinal is coming prelates perswade all men action authority treat persons doth argue much was angry commission
it drawen no soner thought upon condescend begin hope wel proue things may be caried treaty holding his forces
about him stil what further hoped at hands our abode in towne so advantagious litle tast"""


NAMES = """leith dumbarton dunbarton ayr air irwin irvine ryan rain kirkcudbright whithorn wigton galloway glasgow
edinburgh aberdeen dundee montrose orkney isles ireland scotland england spain portugal lisbon flanders dunkirk
dunkergh sluys ostend calais bruges nieuport antwerp bourbourg bullein bulleyn graveling gravelines flushing
semple sempill huntly maxwell bothwell morton crawford errol hamilton montgomery bruce chisholm crichton
parma mendoza guise medina sidonia recalde andrada portugals spaniards scots italians walloons almains"""


def norm(w):
    w = w.lower().replace('v', 'u').replace('j', 'i').replace('y', 'i')
    w = re.sub(r'(.)\1+', r'\1', w)
    return w[:-1] if len(w) > 3 and w.endswith('e') else w


def build(paths):
    c = collections.Counter()
    for p in paths:
        c.update(re.findall(r"[a-z]+", open(p, encoding='utf8', errors='ignore').read().lower()))
    for w in GLOSSED.split():
        c[w] += 50
    for w in NAMES.split():
        c[w] += 20
    with open(os.path.join(HERE, 'wordfreq.tsv'), 'w', encoding='utf8') as f:
        for w, n in c.most_common():
            if n >= 2 and len(w) > 1 or w in ('a', 'i'):
                f.write(f'{w}\t{n}\n')


def load():
    d = collections.defaultdict(lambda: [0, None])
    for line in open(os.path.join(HERE, 'wordfreq.tsv'), encoding='utf8'):
        w, n = line.rstrip('\n').split('\t')
        k = norm(w)
        d[k][0] += int(n)
        if d[k][1] is None:
            d[k][1] = w
    return d


def candidates(word, d, top=6):
    sets = [SETS.get(ch, ch) for ch in word]
    n = 1
    for s in sets:
        n *= len(s)
    found = {}
    if n <= 200000:
        for t in itertools.product(*sets):
            k = norm(''.join(t))
            if k in d and k not in found:
                found[k] = d[k]
    else:  # too many unknown signs: regex over the list
        rx = re.compile('^' + ''.join('[' + s + ']' for s in sets) + '$')
        for k, v in d.items():
            if rx.match(v[1] or ''):
                found[k] = v
    return sorted(((v[0], v[1]) for v in found.values()), reverse=True)[:top]


EQ = {'v': 'u', 'j': 'i', 'y': 'i'}


def cost(signs, word, cap):
    """Edit cost of spelling `word` with `signs`: 0 when each sign's set holds the letter; a doubled letter may
    share one sign for free; a wrong, extra (null) or missing sign costs 1."""
    w = ''.join(EQ.get(ch, ch) for ch in word)
    sets = [set(''.join(EQ.get(x, x) for x in SETS.get(g, g))) for g in signs]
    n, m = len(sets), len(w)
    INF = 99
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [INF] * m
        for j in range(1, m + 1):
            c = min(prev[j - 1] + (0 if w[j - 1] in sets[i - 1] else 1), prev[j] + 1, cur[j - 1] + 1)
            if j > 1 and w[j - 1] == w[j - 2]:
                c = min(c, cur[j - 1])
            cur[j] = c
        if min(cur) > cap:
            return INF
        prev = cur
    return prev[m]


def fuzzy(signs, words, top=6):
    cap = 1 if len(signs) < 7 else 2
    out = []
    for w, n in words:
        if abs(len(w) - len(signs)) > cap + 1:
            continue
        c = cost(signs, w, cap)
        if c <= cap:
            out.append((c, -n, w))
    out.sort()
    return [(c, w, -n) for c, n, w in out[:top]]


def main():
    if sys.argv[1:2] == ['--build']:
        build(sys.argv[2:])
        return
    d = load()
    lexicon = [(v[1], v[0]) for v in d.values() if v[1]]
    pick = sys.argv[1] if len(sys.argv) > 1 else ''
    for line in open(os.path.join(HERE, 'runs.txt'), encoding='utf8'):
        if line.startswith('#') or '|' not in line:
            continue
        rid, before, words, after = [x.strip() for x in line.split('|')]
        if not rid.startswith(pick):
            continue
        print(f'== {rid}: ...{before} [{words}] {after}...')
        for w in words.split():
            if w.startswith('['):
                print(f'   {w:14s} code sign')
                continue
            c = candidates(w, d)
            print(f'   {w:14s} exact: ' + ('  '.join(f'{x}({n})' for n, x in c) if c else '—'))
            f = [x for x in fuzzy(w, lexicon) if x[0] > 0]
            if f:
                print(f'   {"":14s} near:  ' + '  '.join(f'{x}({n},{e})' for e, x, n in f))


if __name__ == '__main__':
    main()
