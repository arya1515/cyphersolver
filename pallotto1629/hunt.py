"""Search a whole corpus for the plaintext of a ciphertext window, exactly.

For a homophonic substitution, equal codes force equal letters. So take a window
of the cipher, list every pair of positions inside it holding the SAME code, and
require the plaintext to repeat at exactly those offsets. That is a necessary
condition, it is cheap, and it is checked over the entire corpus at once with
bitmasks: for each gap g, bit x of MASK[g] is set when T[x] == T[x+g].

Intersecting the masks for all the window's repeat pairs leaves only the corpus
positions where that window could possibly align. With ~10 constraints the
survivors are essentially all genuine, so if a window of the cipher enciphers
anything in the corpus this finds it, and if nothing survives anywhere the
ciphertext does not encipher that corpus at that code width.
"""
import re
from collections import defaultdict


def load_corpus(path):
    t = open(path, encoding='utf-8', errors='replace').read().lower()
    for a, b in (('à', 'a'), ('è', 'e'), ('é', 'e'), ('ì', 'i'), ('ò', 'o'),
                 ('ù', 'u'), ('ä', 'a'), ('ö', 'o'), ('ü', 'u')):
        t = t.replace(a, b)
    t = t.replace('v', 'u').replace('j', 'i')
    return re.sub(r'[^a-z]', '', t).upper()


def masks_for(T, gaps, _arr={}):
    """MASK[g]: bit x set iff T[x] == T[x+g].  numpy-packed, so this is fast."""
    import numpy as np
    if 'a' not in _arr or _arr.get('T') is not T:
        _arr['a'] = np.frombuffer(T.encode('latin-1'), dtype=np.uint8)
        _arr['T'] = T
    a = _arr['a']
    n = len(T)
    out = {}
    for g in gaps:
        eq = np.zeros(n, dtype=np.uint8)
        eq[:n - g] = (a[:n - g] == a[g:]).astype(np.uint8)
        packed = np.packbits(eq, bitorder='little').tobytes()
        out[g] = int.from_bytes(packed, 'little')
    return out


def window_constraints(codes, s, W):
    """Repeat pairs (offset_of_first, gap) inside codes[s:s+W]."""
    seen = {}
    cons = []
    for k in range(W):
        c = codes[s + k]
        if c in seen:
            cons.append((seen[c], k - seen[c]))
        seen[c] = k
    return cons


def hunt(codes, T, W=60, minc=9, step=17, limit=40):
    """Yield (cipher_window_start, corpus_position, n_constraints)."""
    n = len(T)
    universe = (1 << n) - 1
    cache = {}
    hits = []
    for s in range(0, len(codes) - W, step):
        cons = window_constraints(codes, s, W)
        if len(cons) < minc:
            continue
        gaps = sorted({g for _, g in cons})
        for g in gaps:
            if g not in cache:
                cache[g] = masks_for(T, [g])[g]
        acc = universe
        for off, g in cons:
            acc &= (cache[g] >> off) if off else cache[g]
            if acc == 0:
                break
        if acc:
            pos = []
            v = acc
            while v and len(pos) < limit:
                b = (v & -v).bit_length() - 1
                pos.append(b)
                v &= v - 1
            hits.append((s, pos, len(cons)))
    return hits
