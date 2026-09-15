"""Compare a vsolve output on syn/ with the true plaintext: letter accuracy via alignment-free LCS ratio and key match."""
import sys, re, ast, pathlib, difflib
HERE = pathlib.Path(__file__).parent
out = open(sys.argv[1], encoding='utf8', errors='replace').read()
pt = out.split('PLAINTEXT:')[1]
dec = re.sub(r'[^a-z]', '', pt)
true = re.sub(r'[^a-z]', '', (HERE / 'syn' / 'plain.txt').read_text())
sm = difflib.SequenceMatcher(None, dec[:3000], true[:3000], autojunk=False)
print(f'decoded {len(dec)} chars, true {len(true)}; similarity(first 3000) = {sm.ratio():.3f}')
print('DEC:', dec[:300]); print('TRU:', true[:300])
lines = (HERE / 'syn' / 'key.txt').read_text().splitlines()
vd = ast.literal_eval(lines[0].split(' ', 1)[1]); cd = ast.literal_eval(lines[1].split(' ', 1)[1])
print('true vowels', vd); print('true cons', cd)
print(out.split('PLAINTEXT:')[0][:1200])
