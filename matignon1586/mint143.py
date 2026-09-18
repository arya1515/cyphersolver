"""Mint exemplars for f. 143's own hand from a forced alignment of a line whose text is known.

Alignment uses f. 18's letters as a weak cross-hand prior plus f. 143's own set (codes first, then
whatever has been minted); only one-box-one-token pairings are kept, into manifest_f143.json.
"""
import json, sys, io
_o = sys.stdout; sys.stdout = io.StringIO()
import os
os.environ['EXMAN'] = 'exemplars/manifest_mix.json'
from forcealign import run
sys.stdout = _o
from PIL import Image

def remix():
    a = json.load(open('exemplars/manifest.json')); b = json.load(open('exemplars/manifest_f143.json'))
    json.dump(a + b, open('exemplars/manifest_mix.json', 'w'), indent=1)

def mint(line, gap, text):
    remix()
    _o = sys.stdout; sys.stdout = io.StringIO()
    bs, path, a, toks = run('hi/f143flat.png', 'f143_lines.txt', line, gap, text)
    sys.stdout = _o
    man = json.load(open('exemplars/manifest_f143.json')); have = {m['file'] for m in man}
    im = Image.fromarray(a); n = 0
    ops = ''.join(p[4] for p in path)
    for bi0, bi1, tj0, tj1, op in path:
        if op != '1': continue
        k = bi0 + 1; lab = toks[tj0].strip('<>')
        x0, x1, y0, y1 = bs[bi0]
        fn = f'exemplars/f143/l{line}_{k:02d}_{lab}.png'
        if fn in have: continue
        im.crop((x0-4, y0-6, x1+4, y1+6)).save(fn)
        man.append({'file': fn, 'letter': lab, 'src': f'f143 l{line}', 'box': [x0, x1, y0, y1],
                    'crib': f'forced alignment, gap {gap}'}); n += 1
    json.dump(man, open('exemplars/manifest_f143.json', 'w'), indent=1)
    remix()
    from collections import Counter
    c = Counter(m['letter'] for m in man if len(m['letter']) == 1)
    print(f'f.143 line {line}: {len(bs)} boxes/{len(toks)} tok, 1:{ops.count("1")} dig:{ops.count("2")}'
          f' -> minted {n}; f.143 set {sum(c.values())} over {len(c)} letters')

if __name__ == '__main__':
    mint(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
