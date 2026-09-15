"""Beale book-cipher harness.

Key model: number n -> some letter of the key text (default: first letter of word n, 1-indexed).
Scanning: for a text of W words, test every start offset o (key word i = words[o+i]) using a
fast FFT cross-correlation of the per-position letter log-likelihood ratio (English text letters
vs. initial-letter background).  Top offsets are re-scored with a quadgram model, and compared to a
permutation null (same text, shuffled cipher numbers).
"""
import re, math, json, os, sys
import numpy as np
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
AL = 'abcdefghijklmnopqrstuvwxyz'
IDX = {c: i for i, c in enumerate(AL)}

def load_cipher(name):
    return np.array(list(map(int, open(os.path.join(HERE, name + '.txt')).read().split())))

WORD_RE = re.compile(r"[A-Za-z][A-Za-z'’]*(?:-[A-Za-z'’]+)*")

def words_of(text):
    return WORD_RE.findall(text)

def strip_gutenberg(text):
    s = text.find('*** START OF')
    if s >= 0:
        s = text.find('\n', s) + 1
        text = text[s:]
    e = text.find('*** END OF')
    if e >= 0:
        text = text[:e]
    return text

# ---------- language models ----------
def build_quadgram(paths, out):
    cnt = Counter(); uni = Counter(); ini = Counter()
    for p in paths:
        t = strip_gutenberg(open(p, encoding='utf-8', errors='ignore').read())
        ws = words_of(t)
        for w in ws:
            ini[w[0].lower()] += 1
        s = re.sub('[^a-z]', '', t.lower())
        uni.update(s)
        for i in range(len(s) - 3):
            cnt[s[i:i+4]] += 1
    json.dump({'quad': cnt, 'uni': uni, 'ini': ini}, open(out, 'w'))

class LM:
    def __init__(self, path=os.path.join(HERE, 'en_lm.json')):
        d = json.load(open(path))
        self.quad = d['quad']; tot = sum(self.quad.values())
        self.qlog = {k: math.log(v / tot) for k, v in self.quad.items()}
        self.qfloor = math.log(0.01 / tot)
        uni = d['uni']; ut = sum(uni.values())
        ini = d['ini']; it = sum(ini.values())
        self.uni = np.array([uni.get(c, 1) / ut for c in AL])
        self.ini = np.array([ini.get(c, 1) / it for c in AL])
        # LLR per letter: log P_text(c) - log P_initial(c)
        self.llr = np.log(self.uni) - np.log(self.ini)
    def quad_score(self, s):
        s = re.sub('[^a-z]', '', s)
        return sum(self.qlog.get(s[i:i+4], self.qfloor) for i in range(len(s) - 3)) / max(1, len(s) - 3)

# ---------- key extraction ----------
def key_letters(words, mode='first'):
    """Return an int array (0-25, or -1 for none) of key letters per word position."""
    out = np.full(len(words), -1, dtype=np.int64)
    for i, w in enumerate(words):
        lw = re.sub("[^a-z]", "", w.lower())
        if not lw:
            continue
        if mode == 'first': c = lw[0]
        elif mode == 'last': c = lw[-1]
        elif mode == 'second': c = lw[1] if len(lw) > 1 else lw[0]
        else: raise ValueError(mode)
        out[i] = IDX[c]
    return out

def letters_stream(text):
    s = re.sub('[^a-z]', '', text.lower())
    return np.array([IDX[c] for c in s], dtype=np.int64)

def decode(keyarr, cipher, offset=0, base=1):
    idx = cipher - base + offset
    ok = (idx >= 0) & (idx < len(keyarr))
    res = np.full(len(cipher), -1, dtype=np.int64)
    res[ok] = keyarr[idx[ok]]
    return res

def to_str(arr):
    return ''.join(AL[c] if c >= 0 else '?' for c in arr)

# ---------- scanning ----------
def scan(keyarr, cipher, lm, base=1, topk=5, min_cover=0.8):
    """Score every offset o where key index = cipher - base + o.
    Returns (list of (offset, mean_llr_per_letter, coverage, z), all_scores) where z is relative to
    the distribution of mean-LLR over all valid offsets of this text (robust: median/MAD)."""
    W = len(keyarr)
    S = np.where(keyarr >= 0, lm.llr[np.clip(keyarr, 0, 25)], 0.0)
    C = np.where(keyarr >= 0, 1.0, 0.0)
    m = int(cipher.max()) - base
    lo = int(cipher.min()) - base
    if W <= lo + 20:
        return [], None
    h = np.zeros(m + 1)
    for c in cipher:
        h[c - base] += 1
    n = W + m + 1
    nfft = 1 << int(n - 1).bit_length()
    FS = np.fft.rfft(S, nfft); FC = np.fft.rfft(C, nfft); FH = np.fft.rfft(h, nfft)
    sc = np.fft.irfft(FS * np.conj(FH), nfft)[:W]
    cnt = np.fft.irfft(FC * np.conj(FH), nfft)[:W]
    cv = cnt / len(cipher)
    valid = cv >= min_cover
    if not valid.any():
        return [], None
    mean = np.where(valid, sc / np.maximum(cnt, 1), np.nan)
    v = mean[valid]
    med = np.nanmedian(v); mad = np.nanmedian(np.abs(v - med)) * 1.4826 + 1e-9
    z = (mean - med) / mad
    offs = np.nonzero(valid)[0]
    order = offs[np.argsort(-mean[offs])][:topk]
    return [(int(o), float(mean[o]), float(cv[o]), float(z[o])) for o in order], mean


# ---------- drift-tolerant banded scan ----------
def make_bands(cipher, per_band=50):
    """Split cipher numbers (by magnitude) into bands of ~per_band numbers each. Returns list of masks."""
    order = np.argsort(cipher, kind='stable')
    n = len(cipher); k = max(1, n // per_band)
    bands = []
    for i in range(k):
        idx = order[i * n // k:(i + 1) * n // k]
        m = np.zeros(n, dtype=bool); m[idx] = True
        bands.append(m)
    return bands

_FH_CACHE = {}
def _band_ffts(cipher, bands, base, nfft, tag):
    key = (tag, base, nfft)
    if key not in _FH_CACHE:
        m = int(cipher.max()) - base
        out = []
        for bm in bands:
            h = np.zeros(m + 1)
            for c in cipher[bm]:
                h[c - base] += 1
            out.append((np.fft.rfft(h, nfft), int(bm.sum())))
        _FH_CACHE[key] = out
    return _FH_CACHE[key]

def scan_drift(keyarr, cipher, lm, bands, tag, base=1, lam=0.5, min_cover=0.75, exclude_radius=0):
    """Drift-tolerant scan. Each band k gets its own offset o_k; total = sum_k band_score(o_k) - lam*|o_k - o_{k-1}|.
    Band scores are mean LLR per letter * n_k (i.e. summed LLR).  Returns (total_llr_per_letter, offsets list, coverage)."""
    W = len(keyarr)
    m = int(cipher.max()) - base
    lo = int(cipher.min()) - base
    if W <= lo + 20:
        return None
    S = np.where(keyarr >= 0, lm.llr[np.clip(keyarr, 0, 25)], 0.0)
    C = np.where(keyarr >= 0, 1.0, 0.0)
    n = W + m + 1
    nfft = 1 << int(n - 1).bit_length()
    FS = np.fft.rfft(S, nfft); FC = np.fft.rfft(C, nfft)
    fhs = _band_ffts(cipher, bands, base, nfft, tag)
    K = len(bands)
    G = np.empty((K, W)); CV = np.empty((K, W))
    for k, (FH, nk) in enumerate(fhs):
        sc = np.fft.irfft(FS * np.conj(FH), nfft)[:W]
        cnt = np.fft.irfft(FC * np.conj(FH), nfft)[:W]
        cv = cnt / nk
        G[k] = np.where(cv >= min_cover, sc, -1e9)
        CV[k] = cnt
    # DP with |delta| transition cost via distance transform
    f = G[0].copy()
    back = np.zeros((K, W), dtype=np.int64)
    for k in range(1, K):
        # g = max_{o'} f[o'] - lam*|o - o'|
        g = f.copy(); arg = np.arange(W)
        # forward
        for o in range(1, W):
            if g[o - 1] - lam > g[o]:
                g[o] = g[o - 1] - lam; arg[o] = arg[o - 1]
        for o in range(W - 2, -1, -1):
            if g[o + 1] - lam > g[o]:
                g[o] = g[o + 1] - lam; arg[o] = arg[o + 1]
        back[k] = arg
        f = g + G[k]
    best = int(np.argmax(f)); total = float(f[best])
    if total < -1e8:
        return None
    offs = [best]
    for k in range(K - 1, 0, -1):
        offs.append(int(back[k][offs[-1]]))
    offs = offs[::-1]
    cover = sum(CV[k][offs[k]] for k in range(K)) / len(cipher)
    return total / len(cipher), offs, float(cover)

def decode_drift(keyarr, cipher, bands, offs, base=1):
    res = np.full(len(cipher), -1, dtype=np.int64)
    for bm, o in zip(bands, offs):
        idx = cipher[bm] - base + o
        ok = (idx >= 0) & (idx < len(keyarr))
        r = np.full(int(bm.sum()), -1, dtype=np.int64); r[ok] = keyarr[idx[ok]]
        res[bm] = r
    return res

# ---------- two-stage: coarse bands with drift windows + quadgram verification ----------
BAND_EDGES = [(1, 100), (101, 300), (301, 700), (701, 10**6)]
BAND_WIN = [0, 10, 20, 40]

def range_bands(cipher, edges=BAND_EDGES):
    return [((cipher >= a) & (cipher <= b)) for a, b in edges]

def _sliding_max(x, w):
    if w == 0:
        return x
    from scipy.ndimage import maximum_filter1d
    return maximum_filter1d(x, 2 * w + 1, mode='nearest')

def stage1(keyarr, cipher, lm, bands, tag, base=1, wins=BAND_WIN, min_cover=0.75, topk=3):
    W = len(keyarr)
    m = int(cipher.max()) - base
    lo = int(cipher.min()) - base
    if W <= lo + 20:
        return None
    S = np.where(keyarr >= 0, lm.llr[np.clip(keyarr, 0, 25)], 0.0)
    C = np.where(keyarr >= 0, 1.0, 0.0)
    n = W + m + 1
    nfft = 1 << int(n - 1).bit_length()
    FS = np.fft.rfft(S, nfft); FC = np.fft.rfft(C, nfft)
    fhs = _band_ffts(cipher, bands, base, nfft, tag)
    total = np.zeros(W); cnt = np.zeros(W)
    for k, (FH, nk) in enumerate(fhs):
        if nk == 0:
            continue
        sc = np.fft.irfft(FS * np.conj(FH), nfft)[:W]
        ct = np.fft.irfft(FC * np.conj(FH), nfft)[:W]
        total += _sliding_max(sc, wins[k]); cnt += _sliding_max(ct, wins[k])
    cv = cnt / len(cipher)
    valid = cv >= min_cover
    if valid.sum() < 50:
        return None
    mean = np.where(valid, total / np.maximum(cnt, 1), np.nan)
    v = mean[valid]; med = np.nanmedian(v); mad = np.nanmedian(np.abs(v - med)) * 1.4826 + 1e-9
    z = (mean - med) / mad
    offs = np.nonzero(valid)[0]
    order = offs[np.argsort(-mean[offs])]
    # keep topk distinct (not within 50 of each other)
    picked = []
    for o in order:
        if all(abs(o - p) > 50 for p in picked):
            picked.append(int(o))
        if len(picked) >= topk:
            break
    return [(o, float(mean[o]), float(cv[o]), float(z[o])) for o in picked]

def stage2(keyarr, cipher, lm, bands, o, wins=BAND_WIN, sweeps=2, base=1):
    """Coordinate ascent on per-band shifts d_k in [-w_k, w_k] maximising quadgram score of the decode."""
    K = len(bands)
    d = [0] * K
    def dec(dv):
        return bc_decode_shifts(keyarr, cipher, bands, [o + x for x in dv], base)
    best = lm.quad_score(to_str(dec(d)))
    for _ in range(sweeps):
        improved = False
        for k in range(K):
            if wins[k] == 0 or not bands[k].any():
                continue
            for x in range(-wins[k], wins[k] + 1):
                if x == d[k]:
                    continue
                dd = d.copy(); dd[k] = x
                s = lm.quad_score(to_str(dec(dd)))
                if s > best + 1e-9:
                    best = s; d = dd; improved = True
        if not improved:
            break
    return best, d, to_str(dec(d))

def bc_decode_shifts(keyarr, cipher, bands, offs, base=1):
    return decode_drift(keyarr, cipher, bands, offs, base)
