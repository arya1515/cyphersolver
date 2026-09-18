# Decode class strings (space-separated: an bo cp dq er fs gt hu ix ly mz que qui pour # ? .) with the French 6-gram beam.
# usage: decode_line.py file_or_string [beam] ; lines "Lk: ..." ; '.' ignored, '#' = code word kept as '#', '?' any letter.
import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sp53'))
from homo import LM
PAIRS = {'an': 'an', 'bo': 'bo', 'cp': 'cp', 'dq': 'dq', 'er': 'er', 'fs': 'fs', 'gt': 'gt', 'hu': 'hu', 'ix': 'ix', 'ly': 'ly', 'mz': 'mz'}
ALL = 'abcdefghilmnopqrstuxyz'
def decode(tokens, lm, beam=3000, nbest=3):
    beams = [('', '', 0.0)]   # (display, lm-context text, score)
    for tk in tokens:
        tk = tk.rstrip('?') if tk.endswith('?') and len(tk) > 1 else tk
        if tk in ('.', ''): continue
        if tk in PAIRS: opts = [(c, c) for c in PAIRS[tk]]
        elif tk in ('que', 'qui', 'pour'): opts = [(tk, tk)]
        elif tk == '#': opts = [('#', ' ')]
        elif tk == '?': opts = [(c, c) for c in ALL]
        else: raise ValueError(tk)
        new = []
        for disp, ctx, sc in beams:
            for d, c in opts:
                s2 = sc; t2 = ctx
                for ch in c:
                    if ch == ' ': t2 = t2 + ' '; continue
                    s2 += lm.logp(t2[-5:], ch); t2 += ch
                new.append((disp + d, t2, s2))
        new.sort(key=lambda x: -x[2]); beams = new[:beam]
    return [(b[0], b[2]) for b in beams[:nbest]]
if __name__ == '__main__':
    lm = LM(os.environ.get('LMPATH', os.path.join(os.path.dirname(__file__), '..', 'sp53', 'fr6.pkl')))
    beam = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
    src = open(sys.argv[1], encoding='utf-8').read() if os.path.exists(sys.argv[1]) else sys.argv[1]
    for line in src.strip().split('\n'):
        if not line.strip() or line.startswith('#'): continue
        tag, _, s = line.partition(':') if re.match(r'^L\d+', line) else ('', '', line)
        toks = s.split()
        for d, sc in decode(toks, lm, beam):
            print(tag, round(sc, 1), d)
        print()
