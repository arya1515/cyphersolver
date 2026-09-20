"""Read nomenclator meanings off the 1632 interlinear decipherment of R75.

Lasry left all 95 three-digit elements unsolved.  R75 carries a contemporary
decipherment between the lines, and the DECODE transcriber copied what was
legible of it.  Deciphering R75 here puts a placeholder at each nomenclator
element; aligning that reading with the interlinear shows which word of the
1632 decipherment stands at the placeholder, and so what the element means.

The interlinear is faded and the transcriber flagged much of it with '?' and
'*', so every proposal below is an inference from a damaged witness, not a
key entry read off a key.
"""
import sys, os, re, json, difflib, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
import decode as D, indomain, control
from lang import lm

MARK = '\x00'

def read_lines(model, nomen):
    """Decipher R75 line by line, marking each nomenclator element."""
    out = []
    for line in open(os.path.join(HERE, 'r75.digits'), encoding='utf-8'):
        s = ''.join(c for c in line if c.isdigit())
        if not s:
            continue
        _, _, toks = D.decode(s, model, nomen, beam=600, w_lm=0.4)
        txt = ''
        for t in toks:
            if t.startswith('#'):
                txt += MARK
            elif t.startswith('?') or t in D.NULLS:
                pass
            elif t == '6':
                txt += ' '
            else:
                txt += D.KEY[t]
        out.append((txt, [t[1:] for t in toks if t.startswith('#')]))
    return out

def main():
    model, _ = indomain.build(w=0.6)
    D.P_NOMEN_KNOWN, D.P_NOMEN_NEW, D.P_NULL = -1.5, -20.0, 0.0
    lines = read_lines(model, D.load_nomen())
    wit = control.witness(os.path.join(HERE, 'decode', 'DOC_R75_D2532_2532.txt'))
    props = collections.defaultdict(collections.Counter)
    for i, (txt, codes) in enumerate(lines):
        if i >= len(wit):
            break
        w = control.key(wit[i])
        if len(w) < 12:
            continue
        mine = txt.replace(' ', '')
        sm = difflib.SequenceMatcher(None, mine, w, autojunk=False)
        # map each position of `mine` to a position in `w`
        pos = {}
        for a, b, size in sm.get_matching_blocks():
            for k in range(size):
                pos[a + k] = b + k
        marks = [j for j, c in enumerate(mine) if c == MARK]
        for j, code in zip(marks, [c for c in codes]):
            lo = max([pos[k] for k in pos if k < j], default=None)
            hi = min([pos[k] for k in pos if k > j], default=None)
            if lo is None or hi is None or not (0 <= hi - lo - 1 <= 14):
                continue
            frag = w[lo + 1:hi]
            if frag:
                props[code][frag] += 1
    print('nomenclator elements with a witness fragment: %d\n' % len(props))
    for code in sorted(props):
        best = props[code].most_common(4)
        print('%s  %s' % (code, '  '.join('%r x%d' % (f, n) for f, n in best)))
    json.dump({k: dict(v) for k, v in props.items()},
              open(os.path.join(HERE, 'nomen_proposals.json'), 'w'), indent=1)

main()
