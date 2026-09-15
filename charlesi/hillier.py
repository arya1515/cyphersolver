"""Harvest the Titus nomenclator from Hillier's 1852 printing of the Carisbrooke letters.

George Hillier, "Narrative of the Attempted Escapes of Charles the First from Carisbrook Castle"
(London, 1852), prints fifteen letters from Charles I to Captain Silius Titus with the cipher groups
and their decipherment side by side - the numbers in roman, the plaintext in italics immediately
after the run it translates. That makes the book a large aligned known-plaintext corpus for the one
Carisbrooke cipher whose key is effectively published.

Why this matters here: on 22 May 1648 Charles wrote both to Titus (Hillier's letter number XII) and
to Edward Worsley, and the Worsley letter is one of the two that remain unread. Contemporary keys
show Titus was "W" and Worsley "Z" in the King's letter-code, and the 16 May letter has Worsley
carrying the King's post to Titus at Southampton. So the natural question, which the 2021 Cipherbrain
thread raised and never settled, is whether the Worsley cipher is the Titus cipher.

The text is 1852 letterpress read by OCR, with long s as f and colons variously as ':', ';', '-.',
'^' and '='; Hillier's italic delimiters come back as any of ) ] } \\ . Everything here is therefore
built to be conservative: a pair is kept only when the run of codes and its gloss can be read
without guessing, and the harvest is reported with its own error bars.

Usage:
    python hillier.py pairs      - every (codes, gloss) pair the parser can find
    python hillier.py key        - the code -> plaintext assignments that follow unambiguously
"""
import collections, re, sys

SRC = 'src/narrativeofattem00hilluoft.txt'
ALT = 'src/cu31924028050940.txt'

# the three stretches of the book that carry ciphered letters, found by digit-group density
REGIONS = [(218000, 240000), (298000, 312000), (338000, 352000)]


def normalise(t):
    """Undo the OCR's treatment of the separator between code groups."""
    t = t.replace('—', '-')
    # long s
    # (left alone: we only need the numbers, and f/s confusion does not affect them)
    # separators that should be a colon
    t = re.sub(r'(\d)\s*-\s*\.\s*(\d)', r'\1 : \2', t)
    t = re.sub(r'(\d)\s*\^\s*(\d)', r'\1 : \2', t)
    t = re.sub(r'(\d)\s*=\s*(\d)', r'\1 : \2', t)
    t = re.sub(r'(\d)\s*;\s*(\d)', r'\1 : \2', t)
    t = re.sub(r'(\d)\s*\.\s*(\d\d)', r'\1 : \2', t)
    # OCR splits digits of one group across spaces: "1 1 8" for 118, "21 -.41" handled above.
    # Only join when the pieces are separated by a single space and no colon intervenes.
    for _ in range(3):
        t = re.sub(r'\b(\d)\s(\d)\b(?!\s*:)', r'\1\2', t)
    t = re.sub(r'[ \t]+', ' ', t)
    return t


CODE = r'\d{1,3}'
OPEN = r'[\(\[]'
CLOSE = r'[\)\]\}\\]'


def load(path=SRC):
    t = open(path, encoding='utf-8', errors='ignore').read()
    return '\n'.join(normalise(t[a:b]) for a, b in REGIONS)


def clean_gloss(g):
    g = re.sub(r'\s+', ' ', g).strip()
    g = g.replace('­', '')
    g = re.sub(r'-\s+', '', g)             # line-break hyphens
    # 1852 long s, printed as f, comes back as f: repair only where it is unambiguous
    for a, b in (('ftand', 'stand'), ('muft', 'must'), ('fhall', 'shall'), ('Jhall', 'shall'),
                 ('fhip', 'ship'), ('Jhip', 'ship'), ('Jhif', 'ship'), ('efcape', 'escape'),
                 ('defyre', 'desyre'), ('defire', 'desire'), ('firft', 'first'),
                 ('fatisfaction', 'satisfaction'), ('lykewife', 'likewise'),
                 ('likewife', 'likewise'), ('paffe', 'passe'), ('pajfe', 'passe'),
                 ('pajje', 'passe'), ('frends', 'frends'), ('Jo', 'so'), ('Jhe', 'she'),
                 ('/he', 'she'), ('ajfifted', 'assisted'), ('ajjifted', 'assisted'),
                 ('bujinejs', 'business'), ('bufinefs', 'business'), ('fince', 'since'),
                 ('Whorwoodj', 'Whorwood'), ('TVhorwood', 'Whorwood'), ('Car li/le', 'Carlisle'),
                 ('Carlijle', 'Carlisle'), ('Carli/le', 'Carlisle'), ('OJborne', 'Osborne'),
                 ('Qjborri', 'Osborne'), ('Worjley', 'Worsley'), ('Worftey', 'Worsley'),
                 ('Creffet', 'Cresset'), ('dejcend', 'descend'), ('wached', 'watched'),
                 ('wherjor', 'wherfor'), ('faill', 'faill'), ('fatt', 'fait')):
        g = g.replace(a, b)
    return g


def pairs(t):
    """Every (codes, gloss) pair: a gloss translates the run of code groups just before it."""
    out = []
    # a run of code groups, then an italic gloss
    pat = re.compile(r'((?:%s\s*:\s*)+%s\s*:?\s*)%s([^\(\)\[\]\{\}\\]{2,400})%s'
                     % (CODE, CODE, OPEN, CLOSE))
    for m in pat.finditer(t):
        codes = [int(x) for x in re.findall(r'\d{1,3}', m.group(1))]
        g = clean_gloss(m.group(2))
        if not g or g[0].isdigit():
            continue
        out.append((codes, g, m.start()))
    # single code immediately before a gloss, e.g. "187 (for)"
    pat1 = re.compile(r'(?<![\d:])\s(%s)\s*:?\s*%s([^\(\)\[\]\{\}\\]{2,120})%s' % (CODE, OPEN, CLOSE))
    have = {p[2] for p in out}
    for m in pat1.finditer(t):
        if any(abs(m.start() - h) < 400 for h in have):
            continue
        g = clean_gloss(m.group(2))
        if not g or g[0].isdigit():
            continue
        out.append(([int(m.group(1))], g, m.start()))
    out.sort(key=lambda x: x[2])
    return [(c, g) for c, g, _ in out]


def words(g):
    return [w for w in re.split(r'[^A-Za-z\']+', g) if w]


def unambiguous_key(ps):
    """Assignments that need no alignment guess: one code per word, run length == word count."""
    votes = collections.defaultdict(collections.Counter)
    for codes, g in ps:
        ws = words(g)
        if len(codes) == len(ws) and 1 <= len(codes) <= 6:
            for c, w in zip(codes, ws):
                votes[c][w.lower()] += 1
    key = {}
    for c, v in votes.items():
        w, n = v.most_common(1)[0]
        key[c] = (w, n, sum(v.values()), dict(v))
    return key


def main():
    t = load()
    ps = pairs(t)
    mode = sys.argv[1] if len(sys.argv) > 1 else 'pairs'
    if mode == 'pairs':
        print('%d aligned passages\n' % len(ps))
        for codes, g in ps:
            print('%-3d codes  %s' % (len(codes), ' '.join(map(str, codes))))
            print('           -> %s\n' % g)
    elif mode == 'key':
        key = unambiguous_key(ps)
        print('%d code groups fixed by one-to-one passages\n' % len(key))
        for c in sorted(key):
            w, n, tot, v = key[c]
            flag = '' if n == tot else '   (contested: %s)' % v
            print('   %3d = %-22s x%d%s' % (c, w, n, flag))


if __name__ == '__main__':
    main()
