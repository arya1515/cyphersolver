"""render.py <tokens.json> <par_output.txt> [out.txt]: apply the fasthomo BEST map to the token stream, line by line."""
import sys, json, ast, re
d = json.load(open(sys.argv[1]))
txt = open(sys.argv[2], encoding='utf-8', errors='replace').read()
m = re.search(r"^MAP (.*)$", txt, re.M)
mp = dict(ast.literal_eval(m.group(1)))
toks = d['tokens']
out = []
for page in d['regions']:
    out.append('## ' + page)
    for k in range(len(d['regions'][page]['lines'])):
        out.append(''.join(mp.get(f"{t['cl']:02d}", '?') for t in toks if t['page'] == page and t['line'] == k))
s = '\n'.join(out)
open(sys.argv[3] if len(sys.argv) > 3 else 'render.txt', 'w', encoding='utf-8').write(s)
print(s)
