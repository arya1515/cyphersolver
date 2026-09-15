"""Decrypt Feynman #2/#3 from ciphertext using the two alphabets and dictionary word segmentation (Viterbi).
State = (position, alphabet for next word). Word of length L: take L cipher letters, reverse if L even,
decode with the current alphabet, look up. Alternation can reset to alphabet 1 (new line) or repeat (encoder slip)
at a penalty."""
import math, re, glob, sys
from collections import Counter
import verify as v

inv = [{c: chr(65 + i) for i, c in enumerate(a) if c != '.'} for a in (v.A1, v.A2)]

def build_dict():
    cnt = Counter()
    for p in glob.glob('../beale/lmcorpus/*.txt'):
        t = open(p, encoding='utf-8', errors='ignore').read().upper()
        cnt.update(re.findall(r"[A-Z]+", t))
    for w in ['TIS', 'HELIUM', 'LAMBDA', 'PHENOMENOLOGICAL', 'INTERPRETATIONS', 'THEORETICAL', 'BRISKER', 'HOP', 'YARDS', 'ALES', 'GODS']:
        cnt[w] += 5
    tot = sum(cnt.values())
    return {w: math.log(c / tot) for w, c in cnt.items() if c >= 2}

def decrypt(ct, D, maxlen=16, reset_pen=4.0, repeat_pen=9.0, unk_pen=6.0):
    n = len(ct)
    best = {(0, 0): (0.0, None)}
    for pos in range(n):
        for k in (0, 1):
            if (pos, k) not in best:
                continue
            sc, _ = best[(pos, k)]
            for L in range(1, min(maxlen, n - pos) + 1):
                seg = ct[pos:pos + L]
                seg = seg[::-1] if L % 2 == 0 else seg
                if any(c not in inv[k] for c in seg):
                    continue
                w = ''.join(inv[k][c] for c in seg)
                if w in D:
                    ws = D[w]
                elif L == 1 and w in 'AI':
                    ws = -5.0
                else:
                    ws = -unk_pen * L
                for nk, pen in ((1 - k, 0.0), (0, reset_pen), (k, repeat_pen)):
                    key = (pos + L, nk); val = sc + ws - pen
                    if key not in best or val > best[key][0]:
                        best[key] = (val, (pos, k, w))
    end = max(((n, k) for k in (0, 1) if (n, k) in best), key=lambda s: best[s][0])
    words = []; s = end
    while best[s][1] is not None:
        pos, k, w = best[s][1]; words.append(w); s = (pos, k)
    return ' '.join(reversed(words)), best[end][0]

if __name__ == '__main__':
    D = build_dict()
    for name, ct in (('#2', v.C2), ('#3', v.C3)):
        pt, sc = decrypt(ct, D)
        print(f"Feynman {name} ({len(ct)} letters), score {sc:.1f}:\n  {pt}\n")
