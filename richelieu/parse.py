"""Parse Tomokiyo's transcription of BnF fr.3829 f.87 / f.89 (Richelieu -> M. de Rancé, 1629).

Format: semicolon-separated tokens. Numeric tokens (optionally prefixed with '~' = diacritic)
are cipher symbols; alphabetic tokens (underscored) are cleartext words.
"""
from collections import Counter
import re, pathlib

SRC = pathlib.Path(__file__).with_name('richelieu1629.txt')

def load():
    letters = {}   # name -> list of segments; each segment = list of tokens (str) ; cipher tokens tagged
    cur = None
    text = SRC.read_text(encoding='utf-8')
    # join lines that were wrapped mid-token (a line starting with ';' or a digit after a line ending w/o ';')
    lines = [l.rstrip('\n') for l in text.splitlines()]
    joined, buf = [], ''
    for l in lines:
        if l.startswith('#') or not l.strip():
            if buf: joined.append(buf); buf = ''
            joined.append(l); continue
        if buf and not buf.endswith(';'):
            buf += l
        else:
            if buf: joined.append(buf)
            buf = l
    if buf: joined.append(buf)
    for l in joined:
        if l.startswith('# '):
            cur = l[2:].strip(); letters[cur] = []; continue
        if l.startswith('#') or not l.strip() or cur is None:
            continue
        toks = [t for t in l.split(';') if t != '']
        letters[cur].append(toks)
    return letters

def is_cipher(tok):
    return re.fullmatch(r'~?\d+', tok) is not None

def stream(letters):
    """Yield (letter, line_idx, token, is_cipher)."""
    for name, lines in letters.items():
        for i, toks in enumerate(lines):
            for t in toks:
                yield name, i, t, is_cipher(t)

if __name__ == '__main__':
    L = load()
    allc = Counter(); perletter = {}
    for name, lines in L.items():
        c = Counter(t for toks in lines for t in toks if is_cipher(t))
        perletter[name] = c; allc.update(c)
        print(f"{name}: {sum(c.values())} cipher symbols, {len(c)} distinct")
    print(f"TOTAL: {sum(allc.values())} symbols, {len(allc)} distinct\n")
    tot = sum(allc.values())
    for s, n in allc.most_common():
        both = all(s in perletter[k] for k in perletter)
        print(f"{s:>4} {n:3d} {100*n/tot:5.1f}%  {'both' if both else ''}")

    # cipher-only runs (segments between cleartext), for n-gram analysis
    runs = []
    for name, lines in L.items():
        for toks in lines:
            run = []
            for t in toks + ['|']:
                if is_cipher(t): run.append(t)
                else:
                    if run: runs.append((name, run)); run = []
    print(f"\n{len(runs)} cipher runs; lengths:", sorted(len(r) for _, r in runs))
    big = Counter()
    for _, r in runs:
        for a, b in zip(r, r[1:]): big[(a, b)] += 1
    print("\nTop bigrams:")
    for (a, b), n in big.most_common(25): print(f"  {a}-{b}: {n}")
    tri = Counter()
    for _, r in runs:
        for a, b, c in zip(r, r[1:], r[2:]): tri[(a, b, c)] += 1
    print("\nTop trigrams:")
    for k, n in tri.most_common(15):
        if n > 1: print(f"  {'-'.join(k)}: {n}")
