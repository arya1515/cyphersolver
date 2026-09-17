# Build a dense float32 5-gram log-prob table (24^5) from the 6-gram count pickles used by homo.py,
# with the same absolute-discount smoothing. Output <lang>5.npy indexed [a,b,c,d,e] over ALPHA.
import sys, pickle, numpy as np, math, itertools
from homo import ALPHA, LM

def build(lang):
    lm = LM(f'{lang}6.pkl')
    K = len(ALPHA)
    tab = np.zeros((K,) * 5, dtype=np.float32)
    idx = {c: i for i, c in enumerate(ALPHA)}
    c4 = lm.cnts[4]
    # contexts
    for ctx in itertools.product(ALPHA, repeat=4):
        s = ''.join(ctx)
        i = tuple(idx[c] for c in ctx)
        for ch in ALPHA:
            tab[i + (idx[ch],)] = math.log(lm._p(s, ch, 5))
    np.save(f'{lang}5.npy', tab)
    print(lang, 'done', tab.mean())

if __name__ == '__main__':
    for lang in sys.argv[1:]:
        build(lang)
