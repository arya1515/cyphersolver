"""Pull Lasry's aligned ciphertext/plaintext pairs out of the combined DECODE file.

The file prints, for each cipher line, two '|'-terminated rows in fixed columns:
the segmented ciphertext and, under it, the plaintext of each token.
"""
import re, json, sys, collections

SRC = 'ceva1632/decode/DOC_R74_D3230_3230.txt'

def tokens(row):
    """Column spans of each whitespace-delimited token."""
    return [(m.start(), m.group()) for m in re.finditer(r'\S+', row)]

def main():
    lines = open(SRC, encoding='utf-8', errors='replace').read().split('\n')
    docs, cur, out = [], None, []
    pairs = []
    for i, l in enumerate(lines):
        m = re.match(r'#CATALOG NAME:\s*(.+)', l)
        if m:
            cur = m.group(1).strip()
        if l.rstrip().endswith('|') and i + 1 < len(lines) and lines[i + 1].rstrip().endswith('|'):
            c, p = l.rstrip()[:-1], lines[i + 1].rstrip()[:-1]
            ct, pt = tokens(c), tokens(p)
            # match plaintext token to the ciphertext token at the same column
            starts = [s for s, _ in ct]
            row = []
            for s, tok in ct:
                # nearest plaintext token starting at or after this column,
                # but before the next ciphertext token's column
                nxt = next((x for x in starts if x > s), 10**9)
                val = [w for ps, w in pt if s - 1 <= ps < nxt]
                row.append((tok, ' '.join(val)))
            pairs.append((cur, row))
    json.dump(pairs, open('ceva1632/gold.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    # inventory
    inv = collections.defaultdict(collections.Counter)
    for _, row in pairs:
        for tok, val in row:
            inv[tok][val] += 1
    print('lines', len(pairs), 'distinct tokens', len(inv))
    for t in sorted(inv, key=lambda t: (len(t), t)):
        tot = sum(inv[t].values())
        best = inv[t].most_common(3)
        print(f'{t:>5} x{tot:<4} {best}')

main()
