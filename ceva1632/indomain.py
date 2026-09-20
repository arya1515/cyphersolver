"""An in-domain character model for the 346 letters.

it-cinquecento is Renaissance diplomatic Italian but stops around 1620 and
knows nothing of this clerk's spelling (v for u, doubled letters dropped).
Here it is interpolated with a small model built from text of the dossier
itself: the clear passages the clerk wrote out, and -- for a given fold --
Lasry's plaintext of the letters that are not being tested.
"""
import sys, os, re, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.dirname(HERE))
from lang import lm

def clean(t):
    """Lasry's rendering -> the model alphabet, with <codes> removed."""
    t = re.sub(r'<[^>]*>', ' ', t)
    return lm.norm(t, 'early')

def clear_text():
    """Italian the clerk wrote in clear, from every transcription in the dossier."""
    out = []
    for fn in sorted(os.listdir(os.path.join(HERE, 'decode'))):
        if not fn.endswith('.txt'):
            continue
        for line in open(os.path.join(HERE, 'decode', fn), encoding='utf-8', errors='replace'):
            m = re.match(r'\s*<CLE?A?R?TEXT\s+IT\s+(.*?)>\s*$', line.strip())
            if m:
                out.append(m.group(1))
    return clean(' '.join(out))

def lasry_text(exclude=()):
    docs = json.load(open(os.path.join(HERE, 'lasry_plain.json'), encoding='utf-8'))
    return clean(' '.join(' '.join(v) for k, v in docs.items() if k not in exclude))

class Mix:
    """Linear interpolation of two DenseLMs sharing one alphabet and order."""
    def __init__(self, a, b, w=0.5):
        import numpy as np
        assert a.order == b.order and a.alpha == b.alpha
        self.order, self.alpha, self.A = a.order, a.alpha, a.A
        self.index = a.index
        self.lp = np.log(np.exp(a.lp) * (1 - w) + np.exp(b.lp) * w).astype('float32')

def build(exclude=(), w=0.45, order=5):
    base = lm.load('it-cinquecento')
    text = clear_text() + ' ' + lasry_text(exclude)
    dom = lm.DenseLM.build(text, base.order, base.alpha)
    return Mix(base, dom, w), len(text)

if __name__ == '__main__':
    m, n = build()
    print('in-domain characters:', n)
    print('clear-text sample:', clear_text()[:200])
