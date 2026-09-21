"""Parse tr/*.txt (see tr/CONVENTION.md) into cipher token runs and gloss pairs.

    from parse import load
    runs, glosses = load()        # runs: list of (file, [tokens]) split at clear text; glosses: list of (token, gloss, file)
"""
import glob, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ORDER = ['R3812', 'R3811', 'R3813', 'R3814', 'R3815', 'R4625', 'R4645', 'R4734', 'R4736']


def files(records=None):
    fs = sorted(glob.glob(os.path.join(HERE, 'tr', 'IMG_*.txt')),
                key=lambda f: (ORDER.index(re.search(r'R\d+', f).group()) if re.search(r'R\d+', f).group() in ORDER else 99,
                               int((re.findall(r'_P(\d+)', f) or ['0'])[0]), f))
    if records:
        fs = [f for f in fs if re.search(r'R\d+', f).group() in records]
    return fs


def tokens_of(line):
    """Yield ('clear', text) or ('tok', token, gloss) items for one transcription line."""
    i = 0
    out = []
    for m in re.finditer(r'\{[^}]*\}|\S+', line):
        s = m.group()
        if s.startswith('{'):
            out.append(('clear', s[1:-1]))
            continue
        tok, _, gl = s.partition('=')
        tok = tok.rstrip('+').strip('~[]').rstrip(',.:;')
        if tok.startswith('~') or tok in ('/', '#ins'):
            continue
        gl = gl.rstrip('+')
        if not tok:
            continue
        out.append(('tok', tok, gl or None))
    return out


def load(records=None):
    runs, glosses = [], []
    for f in files(records):
        name = os.path.basename(f)[:-4]
        cur = []
        for line in open(f, encoding='utf-8'):
            s = line.strip()
            if not s or s == '#' or s.startswith('# ') or s.startswith('##') or s.startswith('legend') or s.lower().startswith('legend'):
                continue
            for it in tokens_of(s):
                if it[0] == 'clear':
                    if cur:
                        runs.append((name, cur)); cur = []
                else:
                    cur.append(it[1])
                    if it[2]:
                        glosses.append((it[1], it[2], name))
        if cur:
            runs.append((name, cur))
    return runs, glosses


if __name__ == '__main__':
    import collections, sys
    runs, gl = load(sys.argv[1:] or None)
    n = sum(len(r) for _, r in runs)
    c = collections.Counter(t for _, r in runs for t in r)
    print(n, 'tokens,', len(runs), 'runs,', len(c), 'distinct,', len(gl), 'glosses')
    print(' '.join(f'{k}:{v}' for k, v in c.most_common()))
