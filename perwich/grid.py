"""William Perwich to Lord Arlington, Paris, 9 April 1670 - parsing the transposition grid.

TNA SP 78/129 f.180, published by the National Archives in August 2025 and transcribed by Satoshi
Tomokiyo, who reads it as an undeciphered transposition.

The enciphered passage is not a stream but a GRID, written out in rows across two pages, and its
cells give the plaintext language away immediately. Alongside single letters they hold **ye**, **yt**,
**wt** and **ym** - the standard early-modern scribal abbreviations for *the*, *that*, *with* and
*them* - together with a handful of bare numbers (40, 60, 61, 96, 97, 192, 910) which will be
nomenclator codes for names or words, and a few odd groups (QR, Rom, nd, pa, rq).

So the plaintext is English prose of 1670 with abbreviations and a small nomenclature, and the only
thing standing between the grid and a reading is the order in which its columns are meant to be taken.
That is a columnar transposition, and it is attackable: score candidate column orders with an English
model and hill-climb.

Usage:
    python grid.py show      - the parsed grid, with its shape
    python grid.py read      - straight column reads, every rotation and both directions
"""
import re, sys


def load(path='perwich.txt'):
    """Return the grid as a list of rows, each a list of cell strings."""
    t = open(path, encoding='utf-8-sig', errors='ignore').read()
    rows = []
    for line in t.split('\n'):
        if '\t' not in line:
            continue
        cells = [c.strip() for c in line.split('\t')]
        cells = [c for c in cells if c != '']
        if len(cells) < 8:
            continue
        rows.append(cells)
    return rows


def norm(cell):
    """Strip editorial punctuation but keep the token."""
    return cell.rstrip('.,').strip()


def columns(rows):
    w = max(len(r) for r in rows)
    cols = []
    for c in range(w):
        col = [norm(r[c]) for r in rows if c < len(r) and norm(r[c])]
        cols.append(col)
    return cols


def show():
    rows = load()
    print('%d grid rows' % len(rows))
    for i, r in enumerate(rows):
        print('%2d (%2d) %s' % (i + 1, len(r), ' '.join(r)))
    cols = columns(rows)
    print('\n%d columns; heights %s' % (len(cols), [len(c) for c in cols]))
    print('\ncells that are not a single letter:')
    odd = {}
    for r in rows:
        for c in r:
            n = norm(c)
            if len(n) != 1:
                odd[n] = odd.get(n, 0) + 1
    for k, v in sorted(odd.items(), key=lambda kv: -kv[1]):
        print('   %-6s x%d' % (k, v))
    tot = sum(len(r) for r in rows)
    print('\ntotal cells: %d' % tot)


def read():
    rows = load()
    cols = columns(rows)
    n = len(cols)
    print('straight read down each column, in natural order:')
    print('   ' + ''.join(''.join(c) for c in cols)[:300])
    print('\nreversed column order:')
    print('   ' + ''.join(''.join(c) for c in reversed(cols))[:300])
    print('\nby row, as written:')
    print('   ' + ''.join(''.join(r) for r in rows)[:300])
    print('\neach column separately:')
    for i, c in enumerate(cols):
        print('   %2d  %s' % (i + 1, ''.join(c)))


if __name__ == '__main__':
    {'show': show, 'read': read}[sys.argv[1] if len(sys.argv) > 1 else 'show']()
