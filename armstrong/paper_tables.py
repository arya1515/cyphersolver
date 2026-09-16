"""Tables for the Cryptologia paper, generated from the merged THE=972 table.

  python paper_tables.py runs      -> Table 1: alphabetical runs of the code, with group ranges and counts
  python paper_tables.py ps        -> Table 2: the 49 postscript groups, value, grade, source frame(s)
  python paper_tables.py appendix  -> Appendix: the full merged table (group, value, grade, source)
  python paper_tables.py unread    -> frames downloaded but not read group by group
All output is LaTeX (booktabs). Grades: H pencil legible, C known plaintext (4 May 1806), M pencil doubtful, I inferred.
"""
import sys, re, os, glob
sys.argv, argv = ['x', 'none'], sys.argv
import decode972 as d
sys.argv = argv

# --- sources per group from pairs.txt ------------------------------------------------------------
SRC = {}
for line in open('pairs.txt', encoding='utf-8'):
    if line.startswith('#') or not line.strip():
        continue
    n, r, src, conf = line.rstrip('\n').split('\t')
    SRC.setdefault(int(n), []).append((r, src, conf))

def grade(c):
    return 'I' if c == '?' else c

def clean(r):
    return r.strip()

def merged():
    out = []
    for n in sorted(d.tab):
        b = d.best(n)
        if b is None:
            continue
        r, c = b
        if '...' in r or 'null' in r:
            continue
        out.append((n, clean(r), grade(c)))
    return out

def frames_for(n, reading):
    fr = sorted({s.split('L')[0].split('R')[0] for r, s, c in SRC.get(n, []) if r.strip().lower() == reading.lower()})
    return ', '.join(fr)

def sortkey(r):
    r = r.lower().strip('*?()[] ')
    return r

# --- Table 1: alphabetical runs -------------------------------------------------------------------
def runs():
    rows = merged()
    runs, cur = [], []
    for n, r, g in rows:
        k = sortkey(r)
        if cur and k < sortkey(cur[-1][1]):
            runs.append(cur); cur = []
        cur.append((n, r, g))
    if cur:
        runs.append(cur)
    # merge tiny runs (1 group) into neighbours as likely misreadings, but report them
    print('% runs detected:', len(runs))
    print(r'\begin{tabular}{@{}rrrll@{}}')
    print(r'\toprule')
    print(r'from & to & known & first & last \\')
    print(r'\midrule')
    for run in runs:
        if len(run) < 3:
            continue
        print(f'{run[0][0]} & {run[-1][0]} & {len(run)} & \\emph{{{run[0][1]}}} & \\emph{{{run[-1][1]}}} \\\\')
    print(r'\bottomrule')
    print(r'\end{tabular}')
    small = [run for run in runs if len(run) < 3]
    print('% runs of fewer than 3 known groups (omitted from the table):', [(run[0][0], run[0][1]) for run in small])

# --- Table 2: the postscript ----------------------------------------------------------------------
PS_GROUPS = [1394, 1116, 1273, 250, 1165, 1405, 972, 148, 1459, 1482, 1201, 821, 130, 821, 1429, 720, 970, 1482,
             992, 1319, 1048, 584, 687, 249, 736, 1013, 750, 967, 1459, 1482, 1202, 1561, 927, 1090, 1052, 832, 1482,
             934, 510, 860, 1459, 1482, 1320, 384, 1280, 1216, 1481, 1483, 555]
# groups whose grade in the paper is argued in the text rather than taken from the table
OVERRIDE = {1394: ('ru', 'H', '0194, 0201; 22 Feb 1808'), 555: ('man (1555)', 'I', 'slip; 1555 man on 0195, 0200'),
            1320: ('like', 'H', '0190')}

def ps():
    print(r'\begin{tabular}{@{}rllll@{}}')
    print(r'\toprule')
    print(r'\# & group & value & grade & source \\')
    print(r'\midrule')
    for i, n in enumerate(PS_GROUPS, 1):
        if n in OVERRIDE:
            r, g, src = OVERRIDE[n]
        else:
            b = d.best(n); r, c = b; g = grade(c)
            src = frames_for(n, r) if g in 'HM' else ('4 May 1806' if g == 'C' else 'slot')
        print(f'{i} & {n} & \\emph{{{r}}} & {g} & {src} \\\\')
    print(r'\bottomrule')
    print(r'\end{tabular}')

# --- Appendix -------------------------------------------------------------------------------------
def appendix():
    rows = merged()
    print('% entries:', len(rows))
    print(r'\begin{longtable}{@{}rlll@{}}')
    print(r'\toprule group & value & grade & source \\ \midrule \endhead')
    for n, r, g in rows:
        src = frames_for(n, r) if g in 'HM' else ('4 May 1806' if g == 'C' else 'inferred')
        r = r.replace('&', r'\&')
        print(f'{n} & {r} & {g} & {src} \\\\')
    print(r'\bottomrule')
    print(r'\end{longtable}')

def unread():
    have = sorted(int(re.search(r'(\d{4})', os.path.basename(p)).group(1)) for p in glob.glob('img13/M34-013-*.jpg'))
    read = {190, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201}
    print('downloaded:', have)
    print('not read group by group:', [f'{n:04d}' for n in have if n not in read])
    print('frames cited in pairs.txt:', sorted({s.split('L')[0].split('R')[0] for v in SRC.values() for r, s, c in v}))

if __name__ == '__main__':
    {'runs': runs, 'ps': ps, 'appendix': appendix, 'unread': unread}[argv[1]]()
