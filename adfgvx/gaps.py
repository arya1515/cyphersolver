"""Gap-aware reading of the twenty-two messages, and a repair search around the marked gaps.

The transcription marks lost letters: an en/em dash or hyphen inside a five-letter group, or a whole group
of dashes. repair.py stripped those marks and searched blind. Here every group is restored to five cells,
lost letters becoming '#' placeholders at their marked positions, and the message is decrypted with the
boundaries those placeholders restore. Then an annealer searches the residual: k further insertions or
deletions at unknown positions, scored with the German quadgram model.

Usage:
    python gaps.py direct            - every message x every key, placeholders only (plus parity fix)
    python gaps.py anneal PAGE KEYLEN K [restarts]   - residual search on one message
"""
import itertools, json, math, random, re, sys
import lm_de
from repair import untranspose, unfractionate, load_keys

DASH = '\u2013\u2014-'

def parse(path='msgs.txt'):
    t = open(path, encoding='utf-8', errors='ignore').read()
    msgs, name, cur = [], None, []
    for line in t.split('\n'):
        m = re.match(r'\s*Page\s+(\S+.*?)\s*$', line)
        if m:
            if name is not None:
                msgs.append((name, cur))
            name, cur = m.group(1), []
        elif name is not None:
            for tok in line.split():
                tok = tok.strip('(){}').upper()
                if re.fullmatch('[ADFGVX%s]+' % DASH, tok):
                    letters = re.sub('[^ADFGVX]', '', tok)
                    if any(c in DASH for c in tok):
                        miss = max(1, 5 - len(letters))
                        # keep marked order: letters before/after the dash
                        cells = ''
                        for c in tok:
                            cells += c if c in 'ADFGVX' else ''
                        i = next(i for i, c in enumerate(tok) if c in DASH)
                        pre = re.sub('[^ADFGVX]', '', tok[:i]); post = re.sub('[^ADFGVX]', '', tok[i:])
                        cur.append(pre + '#' * miss + post)
                    else:
                        cur.append(letters)
    if name is not None:
        msgs.append((name, cur))
    out = []
    for i, (nm, groups) in enumerate(msgs):
        out.append({'i': i + 1, 'page': nm, 'groups': groups, 'ct': ''.join(groups)})
    return out

def decrypt(ct, key):
    return unfractionate(untranspose(ct, key['perm'], key['n'], 'B'), key['square'])

def direct():
    keys = load_keys()
    for m in parse():
        ct = m['ct']
        marks = ct.count('#')
        cands = [ct]
        if len(ct) % 2:
            # parity: one more lost (try a placeholder at every position) or one extra (drop each letter)
            cands = [ct[:p] + '#' + ct[p:] for p in range(len(ct) + 1)] + [ct[:p] + ct[p + 1:] for p in range(len(ct))]
        best = []
        for k in keys:
            for c in cands:
                pt = decrypt(c, k)
                best.append((lm_de.per(pt), k['n'], pt, len(c) - len(ct)))
        best.sort(key=lambda x: -x[0])
        print('\npage %-22s %d cells, %d marked gaps, %d groups' % (m['page'], len(ct), marks, len(m['groups'])))
        for sc, n, pt, d in best[:3]:
            print('   %6.3f len%-3d %+d  %s' % (sc, n, d, pt[:90]))

def anneal(page, keylen, K, restarts=20, iters=40000, seed=1):
    keys = [k for k in load_keys() if k['n'] == keylen]
    m = next(m for m in parse() if m['page'].startswith(page))
    ct = m['ct']
    L = len(ct)
    rng = random.Random(seed)
    results = []
    for k in keys:
        for r in range(restarts):
            # state: list of K edits, each (pos, kind) kind=+1 insert placeholder before pos, -1 delete letter at pos
            def apply(edits):
                s = list(ct)
                for pos, kind in sorted(edits, reverse=True):
                    if kind > 0:
                        s.insert(pos, '#')
                    else:
                        if pos < len(s):
                            del s[pos]
                return ''.join(s)
            def ev(edits):
                c = apply(edits)
                if len(c) % 2:
                    return -99.0, c, ''
                pt = decrypt(c, k)
                return lm_de.per(pt), c, pt
            edits = [(rng.randrange(L + 1), rng.choice((1, 1, 1, -1))) for _ in range(K)]
            cur, _, curpt = ev(edits)
            best = (cur, list(edits), curpt)
            T0, T1 = 0.6, 0.02
            for it in range(iters):
                T = T0 * (T1 / T0) ** (it / iters)
                e2 = list(edits)
                j = rng.randrange(K)
                pos, kind = e2[j]
                mv = rng.random()
                if mv < 0.5:
                    pos = min(L, max(0, pos + rng.choice((-3, -2, -1, 1, 2, 3))))
                elif mv < 0.8:
                    pos = min(L, max(0, pos + rng.randrange(-keylen, keylen + 1)))
                elif mv < 0.9:
                    pos = rng.randrange(L + 1)
                else:
                    kind = -kind
                e2[j] = (pos, kind)
                v, _, pt = ev(e2)
                if v >= cur or rng.random() < math.exp((v - cur) / T):
                    edits, cur, curpt = e2, v, pt
                    if cur > best[0]:
                        best = (cur, list(edits), curpt)
            results.append(best)
    results.sort(key=lambda x: -x[0])
    seen = set()
    for sc, edits, pt in results:
        if pt in seen:
            continue
        seen.add(pt)
        print('%7.3f  %s\n         %s' % (sc, sorted(edits), pt))
        if len(seen) >= 6:
            break

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'direct'
    if mode == 'direct':
        direct()
    else:
        anneal(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]) if len(sys.argv) > 5 else 20)
