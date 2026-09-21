"""Plain quadgram log-prob tables (no backoff) from the shared lang/ corpora, spaceless, early/latin normalisation."""
import os, re, math, pickle, unicodedata
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CORP = os.path.join(HERE, '..', 'lang', 'corpora')
A = 'abcdefghiklmnopqrstuxyz'  # i=j, u=v=w folded for early texts
IDX = {c: i for i, c in enumerate(A)}


def norm(t):
    t = unicodedata.normalize('NFKD', t.lower())
    t = ''.join(c for c in t if not unicodedata.combining(c))
    t = t.replace('j', 'i').replace('v', 'u').replace('w', 'u').replace('ß', 'ss')
    return ''.join(c for c in t if c in IDX)


def table(lang):
    cache = os.path.join(HERE, f'qg_{lang}.npy')
    if os.path.exists(cache):
        return np.load(cache)
    txt = norm(open(os.path.join(CORP, f'{lang}-gutenberg.txt'), encoding='utf8', errors='ignore').read())
    x = np.array([IDX[c] for c in txt], dtype=np.int64)
    n = len(A)
    code = ((x[:-3] * n + x[1:-2]) * n + x[2:-1]) * n + x[3:]
    cnt = np.bincount(code, minlength=n ** 4).astype(np.float64)
    lp = np.log10((cnt + 0.01) / cnt.sum())
    np.save(cache, lp)
    return lp


def encode(s):
    return np.array([IDX[c] for c in s], dtype=np.int64)


def score(lp, x):
    n = len(A)
    if len(x) < 4:
        return 0.0
    code = ((x[:-3] * n + x[1:-2]) * n + x[2:-1]) * n + x[3:]
    return float(lp[code].sum())
