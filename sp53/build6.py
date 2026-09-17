# Dense float32 6-gram log-prob table (24^6, 764 MB) from <lang>6.pkl counts, absolute-discount smoothing
# backing off to the 5-gram table <lang>5.npy. Vectorised over observed 5-letter contexts.
import sys, pickle, numpy as np
from homo import ALPHA

K = len(ALPHA); idx = {c: i for i, c in enumerate(ALPHA)}

def build(lang):
    N, cnts, total = pickle.load(open(f'{lang}6.pkl', 'rb'))
    tab5 = np.load(f'{lang}5.npy')
    tab6 = np.empty((K,) * 6, dtype=np.float32)
    tab6[:] = tab5[None]          # default: back off to 5-gram
    c5 = cnts[5]; c6 = cnts[6]; d = 0.75
    flat6 = tab6.reshape(-1, K)
    ctxs = [k for k in c5 if all(ch in idx for ch in k)]
    ci = np.array([[idx[ch] for ch in k] for k in ctxs], dtype=np.int64)
    den = np.array([c5[k] for k in ctxs], dtype=np.float64)
    num = np.zeros((len(ctxs), K), dtype=np.float64)
    for j, k in enumerate(ctxs):
        for ch in ALPHA:
            v = c6.get(k + ch)
            if v: num[j, idx[ch]] = v
    lin = ((((ci[:, 0] * K + ci[:, 1]) * K + ci[:, 2]) * K + ci[:, 3]) * K + ci[:, 4])
    lower = np.exp(flat6[lin].astype(np.float64))   # currently the 5-gram probs
    p = np.maximum(num - d, 0) / den[:, None] + (d * np.maximum(1, np.minimum(den, 10)) / den)[:, None] * lower
    flat6[lin] = np.log(p).astype(np.float32)
    np.save(f'{lang}6.npy', tab6)
    print(lang, 'contexts', len(ctxs), 'mean', float(tab6.mean()))

if __name__ == '__main__':
    for lang in sys.argv[1:]: build(lang)
