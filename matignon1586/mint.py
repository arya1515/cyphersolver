"""Mint labelled exemplars from a forced alignment, keeping only pairings the evidence supports.

A box is minted only if it aligned one-box-to-one-letter AND that letter is its best or near-best
match among all letters that have exemplars (margin test). Unknown letters (no exemplars yet) are
minted only when the alignment around them is solid, since that is the only way new letters enter.
"""
import json, sys, io, os
_o = sys.stdout; sys.stdout = io.StringIO()
from forcealign import run, load_exemplars, emission
sys.stdout = _o
from PIL import Image

def mint(line, text, tag, skip_boxes=(), margin=0.06):
    _o = sys.stdout; sys.stdout = io.StringIO()
    bs, path, a, toks = run('hi/f18rflat.png', 'f18r_lines.txt', line, 14, text)
    sys.stdout = _o
    from readleaf import vec_from
    by = load_exemplars()
    man = json.load(open('exemplars/manifest.json')); have = {m['file'] for m in man}
    im = Image.fromarray(a); made = []; refused = []
    for bi0, bi1, tj0, tj1, op in path:
        if op != '1': continue
        k = bi0 + 1
        if k in skip_boxes: continue
        tok = toks[tj0]
        x0, x1, y0, y1 = bs[bi0]
        v = vec_from(a[y0:y1, x0:x1])
        mine = emission(v, by, tok)
        best = max(emission(v, by, t) for t in by if len(t) == 1)
        if tok in by and mine < best - margin:
            refused.append(f'{k}:{tok}'); continue
        lab = tok.strip('<>')
        fn = f'exemplars/{tag}_{k:02d}_{lab}.png'
        if fn in have: continue
        im.crop((x0-4, y0-6, x1+4, y1+6)).save(fn)
        man.append({'file': fn, 'letter': lab, 'src': tag, 'box': [x0, x1, y0, y1],
                    'crib': f'forced alignment of line {line}'})
        made.append(f'{k}:{lab}')
    json.dump(man, open('exemplars/manifest.json', 'w'), indent=1)
    print(f'line {line}: minted {len(made)}  refused {len(refused)} on margin')
    print('   minted :', ' '.join(made))
    if refused: print('   refused:', ' '.join(refused))

if __name__ == '__main__':
    mint(int(sys.argv[1]), sys.argv[2], sys.argv[3],
         skip_boxes=tuple(int(x) for x in sys.argv[4].split(',')) if len(sys.argv) > 4 and sys.argv[4] else ())
