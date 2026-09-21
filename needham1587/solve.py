"""Homophonic substitution solver for the Needham 1587 pigpen cipher.

Tokens are shape+mark (e.g. 'J.', 'O:', '7'). Pinned tokens come from the
interlinear glosses; every other token type is annealed against an English
quadgram model built from CSP Foreign calendar text (quad.json).
Usage: python solve.py trans_ACDE.txt trans_FGHI.txt
"""
import json, math, random, re, sys

Q = json.load(open(__file__.replace('solve.py', 'quad.json')))
FLOOR = Q['_floor']

PINS = {  # from glosses: advise, enemyes, campe, nor the towne, Burgrave
    'J': 'a', 'U': 'b', 'L': 'c', 'C': 'd', 'O': 'e', '7': 'h', 'D': 'i', 'F': 'p', 'N': 'g',
    'J.': 't', 'L.': 'm', 'D.': 's', 'O.': 'o', 'C.': 'n', '7.': 'r', 'U.': 'u',
    'U:': 'v', 'L:': 'w', 'O:': 'y',
}

def load(paths):
    lines = []
    for p in paths:
        for raw in open(p, encoding='utf8'):
            raw = raw.split('#')[0]
            if ':' in raw[:12] and not raw.lstrip()[:1] in 'OUNCDLJF7?[':
                raw = raw.split(':', 1)[1]
            toks = []
            for t in raw.replace('|', ' ').split():
                t = t.strip('[]').split('/')[0]
                if re.fullmatch(r"[OUNCDLJF7][.:]?", t):
                    toks.append(t)
            if toks:
                lines.append(toks)
    return lines

def score(s):
    return sum(Q.get(s[i:i + 4], FLOOR) for i in range(len(s) - 3))

def solve(lines, pins=PINS, iters=40000, restarts=8):
    types = sorted({t for l in lines for t in l})
    free = [t for t in types if t not in pins]
    alpha = 'abcdefghiklmnoprstuwyfgkx'
    best = (-1e9, None)
    for r in range(restarts):
        key = dict(pins)
        for t in free:
            key[t] = random.choice(alpha)
        text = lambda k: ''.join(k[t] for l in lines for t in l)
        cur = score(text(key)); T = 3.0
        for i in range(iters):
            if not free:
                break
            t = random.choice(free); old = key[t]
            key[t] = random.choice(alpha)
            ns = score(text(key))
            if ns > cur or random.random() < math.exp((ns - cur) / T):
                cur = ns
            else:
                key[t] = old
            T = max(0.05, T * 0.9997)
        if cur > best[0]:
            best = (cur, dict(key))
    return best

if __name__ == '__main__':
    lines = load(sys.argv[1:])
    sc, key = solve(lines)
    print('score', round(sc, 1))
    print({t: key[t] for t in sorted(key) if t not in PINS})
    for l in lines:
        print(''.join(key.get(t, '?') for t in l))
