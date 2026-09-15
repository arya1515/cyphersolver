"""Score a candidate plaintext (no spaces) by dictionary-word coverage.
usage: python wordscore.py result.txt   (reads PLAINTEXT section of a vsolve output, or raw text)"""
import json, math, sys, re
words = {w: c for w, c in json.load(open('it_words.json', encoding='utf8'))}
tot = sum(words.values())
logp = {w: math.log(c / tot) for w, c in words.items()}
MAXW = 14
OOV = -7.0  # per char

def segment(s):
    n = len(s); best = [0.0] + [-1e18] * n; bp = [0] * (n + 1)
    for i in range(1, n + 1):
        # oov single char
        v = best[i-1] + OOV
        if v > best[i]: best[i] = v; bp[i] = i - 1
        for L in range(2, min(MAXW, i) + 1):
            w = s[i-L:i]
            if w in logp:
                v = best[i-L] + logp[w]
                if v > best[i]: best[i] = v; bp[i] = i - L
    out = []; i = n
    while i > 0:
        out.append(s[bp[i]:i]); i = bp[i]
    return best[n], out[::-1]

def coverage(s, minlen=3):
    sc, segs = segment(s)
    cov = sum(len(w) for w in segs if len(w) >= minlen and w in logp)
    return sc / max(1, len(s)), cov / max(1, len(s)), segs

if __name__ == '__main__':
    txt = open(sys.argv[1], encoding='utf8', errors='replace').read()
    if 'PLAINTEXT:' in txt: txt = txt.split('PLAINTEXT:')[1]
    s = re.sub(r'[^a-z]', '', txt.lower())
    lp, cov, segs = coverage(s)
    print(f'chars={len(s)} nats/char={lp:.3f} coverage(len>=3)={cov:.3f}')
    print(' '.join(segs[:150]))
