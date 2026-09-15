"""Build a --fix spec for vsolve from syn/key.txt (true synthetic key) and print it."""
import ast, pathlib
HERE = pathlib.Path(__file__).parent
lines = (HERE / 'syn' / 'key.txt').read_text().splitlines()
vd = ast.literal_eval(lines[0].split(' ', 1)[1]); cd = ast.literal_eval(lines[1].split(' ', 1)[1]); syl = ast.literal_eval(lines[2].split(' ', 1)[1])
dig = {d: [] for d in range(10)}
for v, d in vd.items(): dig[d].append(v)
for c, d in cd.items(): dig[d].append(c)
parts = [f'{d}={"/".join(v)}' for d, v in dig.items() if v]
dotted = set()
for s, code in syl.items():
    if '^' in code:
        a, b = code.split('^'); parts.append(f'^{b}={s}'); dotted.add(a)
    else:
        parts.append(f'{code}={s}')
for a in dotted: parts.append(f'{a}^=')
print(','.join(parts))
