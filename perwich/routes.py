"""Route reads over Perwich's grid, and over each of its two pages separately.

Two attacks have failed. Reading straight down the transcribed columns is not English, and treating
the cells as a stream and searching every columnar period from 4 to 26 never converges - the best
score sits far closer to a shuffle than to English.

But the index of coincidence of the single letters is 0.0636 against English's 0.0667, so these are
English letters out of order. Something is transposing them, and if it is not a columnar key then it
is a route. Seventeenth-century English practice had plenty: Samuel Morland, who ran Thurloe's cipher
office and whose systems Tomokiyo raises as a possibility here, used grid routes rather than keyword
columns.

This tries the standard routes over the grid as transcribed, and - because the passage is written
across two manuscript pages, sixteen rows on page 3 and six on page 4 - over each page on its own, in
case each is a grid in its own right.

Usage: python routes.py
"""
import re, sys

import grid
import solve as S


def cell_text(c):
    c = grid.norm(c)
    low = c.lower()
    if low in S.EXPAND:
        return S.EXPAND[low]
    if c.isdigit():
        return ''
    return re.sub(r'[^A-Za-z]', '', c).lower()


def pages():
    """The grid split at the page break: 16 rows then 6."""
    rows = grid.load()
    return rows[:16], rows[16:]


def routes(rows):
    """Every standard reading route over a ragged grid."""
    w = max(len(r) for r in rows)
    cols = [[r[c] for r in rows if c < len(r)] for c in range(w)]
    out = {}
    out['rows L-R'] = [c for r in rows for c in r]
    out['rows R-L'] = [c for r in rows for c in reversed(r)]
    out['rows boustro'] = [c for i, r in enumerate(rows) for c in (r if i % 2 == 0 else list(reversed(r)))]
    out['cols L-R down'] = [c for col in cols for c in col]
    out['cols L-R up'] = [c for col in cols for c in reversed(col)]
    out['cols R-L down'] = [c for col in reversed(cols) for c in col]
    out['cols R-L up'] = [c for col in reversed(cols) for c in reversed(col)]
    out['cols boustro'] = [c for i, col in enumerate(cols) for c in (col if i % 2 == 0 else list(reversed(col)))]
    # diagonals
    diag = {}
    for ri, r in enumerate(rows):
        for ci, c in enumerate(r):
            diag.setdefault(ri + ci, []).append(c)
    out['diagonals'] = [c for k in sorted(diag) for c in diag[k]]
    anti = {}
    for ri, r in enumerate(rows):
        for ci, c in enumerate(r):
            anti.setdefault(ci - ri, []).append(c)
    out['antidiagonals'] = [c for k in sorted(anti) for c in anti[k]]
    return out


def main():
    lm = S.LM()
    allrows = grid.load()
    p3, p4 = pages()
    eng = -1.71
    shuf = -5.18
    for name, rows in (('whole grid (22 rows)', allrows), ('page 3 only (16)', p3), ('page 4 only (6)', p4)):
        print('\n=== %s' % name)
        res = []
        for rname, seq in routes(rows).items():
            txt = ''.join(cell_text(c) for c in seq)
            res.append((lm.score(txt), rname, txt))
        res.sort(reverse=True)
        for sc, rname, txt in res:
            print('   %-15s %.4f  %s' % (rname, sc, txt[:72]))
    print('\ncalibration: real English %.2f, shuffled %.2f' % (eng, shuf))


if __name__ == '__main__':
    main()
