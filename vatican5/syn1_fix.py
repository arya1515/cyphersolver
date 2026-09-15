"""--fix spec for the true syn1 key."""
import ast, pathlib
HERE = pathlib.Path(__file__).parent
L = (HERE / 'syn1' / 'key.txt').read_text().splitlines()
letter = ast.literal_eval(L[0].split(' ', 1)[1]); null = L[1].split()[1]
def val(line): return ast.literal_eval(line[line.index('{'):])
syl = val(L[2]); sa = val(L[3]); ra = val(L[4])
dig = {}
for ch, d in letter.items(): dig.setdefault(d, []).append(ch)
parts = [f'{d}={"/".join(v)}' for d, v in sorted(dig.items())]
parts += [f'{code}={s}' for s, code in syl.items()]
parts += [f'.{d}={s}' for s, d in sa.items()]
parts += [f'{d}^={s}' for s, d in ra.items()]
print(','.join(parts))
print('NULL', null)
