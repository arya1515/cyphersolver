"""Second pass over the numeric letters (21 Sept 2026): decode.py's table plus
(1) run-together groups (4-6 digits) split into key values, (2) split groups re-joined when the join is a key value,
(3) 3-digit groups above 322 as nulls (as the interlinear decipherer treats them in R793-R796), except in R823,
where the 400-1000 figures are clear numerals, (4) 220 = a (grade C: unlisted, fits 'a' in context 8 of 11).
Usage: python decode2.py  -> per-record counts and <rec>_read2.txt files."""
import re, glob, sys
from pathlib import Path
R = Path(__file__).resolve().parent
sys.argv = [sys.argv[0]]
exec(open(R/'decode.py', encoding='utf-8').read().split('if __name__')[0])
EXTRA = {220: 'a'}
def val(n): return KEY.get(n, EXTRA.get(n))
def split(s):
    best = None
    def rec(i, acc):
        nonlocal best
        if i == len(s):
            if best is None or len(acc) < len(best): best = acc[:]
            return
        for w in (2, 3):
            p = s[i:i+w]
            if len(p) == w and p[0] != '0' and val(int(p)) is not None: rec(i+w, acc+[int(p)])
    rec(0, []); return best
def toks(line):
    s = re.sub(r"<[^>]*>", " | ", line); out = []
    for tok in re.split(r"\s{2,}|\|", s):
        t = tok.replace(" ", "").strip("—-–.,")
        if re.fullmatch(r"\d+", t): out.append(t)
    return out
summary = []
for f in sorted(glob.glob(str(R/'DOC_R*_D*.txt'))):
    rid = Path(f).name.split('_')[1]
    if rid in ('R580', 'R581', 'R452'): continue
    c = dict(groups=0, key=0, split=0, join=0, null=0, clear=0, c220=0, open=0); out = []
    for line in Path(f).read_text(encoding='utf-8-sig', errors='replace').splitlines():
        if line.startswith('#') or '<PLAINTEXT' in line: continue
        t = toks(line); i = 0; o = []
        while i < len(t):
            x = t[i]; n = int(x); c['groups'] += 1
            if n in KEY: c['key'] += 1; o.append(show(n))
            elif n == 220: c['c220'] += 1; o.append('a')
            elif i+1 < len(t) and n <= 322 and val(int(x+t[i+1])) is not None and val(int(t[i+1])) is None:
                c['join'] += 1; o.append(show(int(x+t[i+1]))); i += 1
            elif len(x) >= 4 and split(x):
                c['split'] += 1; o.append(''.join(show(p) if p in KEY else 'a' for p in split(x)))
            elif len(x) == 3 and n > 322:
                if rid == 'R823': c['clear'] += 1; o.append(f' {x} ')
                else: c['null'] += 1; o.append('·')
            elif rid == 'R823' and n >= 400: c['clear'] += 1; o.append(f' {x} ')
            else: c['open'] += 1; o.append(f' [{x}] ')
            i += 1
        if o: out.append(''.join(o))
    (R/f'{rid}_read2.txt').write_text('\n'.join(out)+'\n', encoding='utf-8')
    read = c['groups'] - c['open']
    print(rid, c, f"read {read}/{c['groups']} = {100*read/c['groups']:.1f}%"); summary.append(c)
G = sum(c['groups'] for c in summary); O = sum(c['open'] for c in summary)
print('TOTAL groups', G, 'open', O, f'{100*(G-O)/G:.2f}% read')
