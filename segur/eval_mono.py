"""Score a solve_mono.py log against a reference key.
usage: eval_mono.py run.log ct_files(comma) key.json|controlN_key.txt
Reports letter-token accuracy (tokens whose figure has a reference value), block accuracy, and per-seed agreement."""
import sys, re, json, ast
log = open(sys.argv[1], encoding='utf-8').read()
files = sys.argv[2].split(','); ref = sys.argv[3]
import os
LO = int(os.environ.get('LO', '12')); BLOCK0 = int(os.environ.get('BLOCK0', '63')); NBLK = int(os.environ.get('NBLK', '16'))
if ref.endswith('.json'):
    k = json.load(open(ref, encoding='utf-8'))
    refL = {int(a): v for a, v in k['letters'].items()}; refB = {int(a): v for a, v in k['blocks'].items()}
else:
    lines = open(ref, encoding='utf-8').read().split('\n')
    refL = ast.literal_eval(lines[0]); blk = ast.literal_eval(lines[1]); refB = {v: c for c, v in blk.items()}
def norm(v): return {'v': 'u', 'j': 'i', '': '-'}.get(v, v)
toks = []
for fn in files:
    for line in open(fn, encoding='utf-8'):
        if line.startswith('#'): continue
        line = re.sub(r'\[[^\]]*\]', ' ', line).replace('INS', ' ').replace('/INS', ' ')
        toks += [int(t.rstrip('?')) for t in line.split() if t.rstrip('?').isdigit()]
def parse_key(desc):
    out = {}
    for part in desc.split(', '):
        lab, rng = part.rsplit(' ', 1)
        a, b = (rng.split('-') + [rng])[:2] if '-' in rng else (rng, rng)
        for f in range(int(a), int(b) + 1): out[f] = lab
    return out
def parse_blocks(s):
    return {int(a): b for a, b in re.findall(r"(\d+): '(\w)'", s)}
seeds = re.findall(r"^(\d+) (-[\d.]+) \| (.*)$\n  BLOCKS (\{.*\})", log, re.M)
for sd, score, desc, blocks in seeds:
    key = parse_key(desc); B = parse_blocks(blocks)
    lt = [t for t in toks if t in refL and refL[t] not in ('-', '')]
    ok = sum(1 for t in lt if norm(key.get(t, '?')) == norm(refL[t]))
    st = [t for t in toks if BLOCK0 <= t < BLOCK0 + 5 * NBLK]
    bok = sum(1 for t in st if norm(B.get(BLOCK0 + 5 * ((t - BLOCK0) // 5), '?')) == norm(refB.get(BLOCK0 + 5 * ((t - BLOCK0) // 5), '?')))
    blocks_ok = sum(1 for b0 in refB if norm(B.get(b0, '?')) == norm(refB[b0]))
    print(f"seed {sd} score {score}: letter tokens {ok}/{len(lt)} = {ok/len(lt):.1%}; syllable tokens {bok}/{len(st)}; blocks {blocks_ok}/{len(refB)}")
