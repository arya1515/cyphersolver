"""Re-join split digit groups in the DECODE transcriptions: where an off-key token sits next to another token,
try the concatenation; accept when it is a key value. Prints per-record counts before and after."""
import re, glob, sys
from pathlib import Path
R = Path(__file__).resolve().parent
sys.argv = [sys.argv[0]]
exec(open(R/'decode.py', encoding='utf-8').read().split('if __name__')[0])
def toks(line):
    s = re.sub(r"<[^>]*>", " | ", line); out = []
    for tok in re.split(r"\s{2,}|\|", s):
        t = tok.replace(" ", "").strip("—-–.,")
        if re.fullmatch(r"\d+", t): out.append(t)
        elif t: out.append(None)
    return out
tot = {}
for f in sorted(glob.glob(str(R/'DOC_R*_D*.txt'))):
    rid = Path(f).name.split('_')[1]
    if rid in ('R580', 'R581', 'R452'): continue
    before = after = n = 0; fixes = []
    for line in Path(f).read_text(encoding='utf-8-sig', errors='replace').splitlines():
        if line.startswith('#') or '<PLAINTEXT' in line: continue
        t = toks(line); i = 0
        while i < len(t):
            x = t[i]
            if x is None: i += 1; continue
            n += 1
            if int(x) in KEY: before += 1; after += 1; i += 1; continue
            if int(x) > 322: i += 1; continue
            if i+1 < len(t) and t[i+1] and int(x+t[i+1]) in KEY and int(t[i+1]) not in KEY:
                fixes.append(x+'+'+t[i+1]); after += 1; n -= 0; i += 2; continue
            i += 1
    tot[rid] = (n, before, after, fixes)
    print(rid, n, before, after, fixes[:12])
