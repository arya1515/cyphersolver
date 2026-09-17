# Consistency-guided key recovery: walk the cipher and the decipherment together, building a token->letter key
# that must stay consistent (each token one letter). Moves: match (token i <- letter j), null token, skip letter.
# Beam search over (i, j, key) states. Reports the best key and where nulls/skips were needed.
import sys, re, unicodedata, collections, json
sys.setrecursionlimit(10000)


def load_ct(f, maxlines=None):
    toks = []; k = 0
    for l in open(f, encoding='utf-8'):
        if l.startswith('#') or not l.strip():
            continue
        l = re.sub(r'^\d+[ab]?:\s*', '', l.strip()); toks += [t for t in l.split() if t != '?']; k += 1
        if maxlines and k >= maxlines:
            break
    return toks


def load_pt(f):
    s = ''.join(l for l in open(f, encoding='utf-8') if not l.startswith('#'))
    s = unicodedata.normalize('NFD', s.lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z]', '', s)


def beam(T, P, start_j=0, width=300, null_cost=4.0, skip_cost=4.0, new_cost=0.3):
    # state: (score, i, j, key(tuple of pairs), trace)
    from heapq import nlargest
    states = [(0.0, 0, start_j, {}, [])]
    for step in range(len(T) + len(P)):
        nxt = []
        done = []
        for sc, i, j, key, tr in states:
            if i == len(T):
                done.append((sc, i, j, key, tr)); continue
            t = T[i]
            if j < len(P):
                c = P[j]
                if t in key:
                    if key[t] == c:
                        nxt.append((sc + 1.0, i + 1, j + 1, key, tr + [('M', i, j)]))
                else:
                    k2 = dict(key); k2[t] = c
                    nxt.append((sc + 1.0 - new_cost, i + 1, j + 1, k2, tr + [('M', i, j)]))
                nxt.append((sc - skip_cost, i, j + 1, key, tr + [('S', i, j)]))
            nxt.append((sc - null_cost, i + 1, j, key, tr + [('N', i, j)]))
        if not nxt:
            states = done; break
        # dedupe by (i,j,frozen key) keep best
        seen = {}
        for s in nxt:
            kk = (s[1], s[2], tuple(sorted(s[3].items())))
            if kk not in seen or seen[kk][0] < s[0]:
                seen[kk] = s
        states = nlargest(width, list(seen.values()) + done, key=lambda s: s[0])
        if all(s[1] == len(T) for s in states):
            break
    return max(states, key=lambda s: s[0])


if __name__ == '__main__':
    ct, pt = sys.argv[1], sys.argv[2]
    nlines = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    T = load_ct(ct, nlines); P = load_pt(pt)
    print('tokens', len(T), 'letters available', len(P))
    best = None
    for start in range(0, 40):
        r = beam(T, P, start_j=start, width=200)
        if best is None or r[0] > best[0]:
            best = r; bs = start
    sc, i, j, key, tr = best
    print('best start', bs, 'score %.1f' % sc, 'tokens used', i, 'letters used', j - bs)
    print('nulls', sum(1 for m in tr if m[0] == 'N'), 'skips', sum(1 for m in tr if m[0] == 'S'))
    inv = collections.defaultdict(list)
    for t, c in key.items():
        inv[c].append(t)
    for c in sorted(inv):
        print(c, ' '.join(sorted(inv[c])))
    # show aligned text
    out = []
    for mv, i_, j_ in tr:
        if mv == 'M':
            out.append('%s=%s' % (T[i_], P[j_]))
        elif mv == 'N':
            out.append('[%s]' % T[i_])
        else:
            out.append('(%s)' % P[j_])
    print(' '.join(out))
    json.dump(key, open('key_beam.json', 'w'))
