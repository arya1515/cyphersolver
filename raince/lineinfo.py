"""lineinfo.py PAGE [LINE] : token count and cluster ids per line, with x positions."""
import json, sys
d = json.load(open('raince_tokens.json'))
page = sys.argv[1]
r = d['regions'][page]; toks = [t for t in d['tokens'] if t['page'] == page]
xmin = min(t['x0'] for t in toks); xmax = max(t['x1'] for t in toks); W = xmax - xmin
lines = sorted({t['line'] for t in toks})
sel = [int(sys.argv[2])-1] if len(sys.argv) > 2 else lines
for L in sel:
    ts = sorted([t for t in toks if t['line'] == L], key=lambda t: t['x0'])
    print(f"{page} line {L+1:02d}  n={len(ts)}")
    print('  cl:', ' '.join(f"{t['cl']:02d}" for t in ts))
    print('  fx:', ' '.join(f"{(t['x0']-xmin)/W:.2f}" for t in ts))
