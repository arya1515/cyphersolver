"""D'Agapeyeff cipher (1939): treat the 196 digit pairs as Polybius cells and solve the
resulting simple substitution with an English quadgram model.

Structure established first: 392 usable digits = 196 pairs; the first digit of every pair is
drawn from {6,7,8,9,0} and the second from {1,2,3,4,5}, i.e. a 5x5 Polybius square, which is the
method D'Agapeyeff works through in his own book.

The book also warns (p.111) that "every third, fourth, or fifth letter, as may be previously
arranged, is a dummy inserted after a message has been put into cipher". So this also tries
striking out every n-th pair, and every n-th pair at each offset, before solving.

Usage:
    python solve.py                 # straight solve, no nulls removed
    python solve.py --nulls         # sweep null periods 3,4,5 at every offset
    python solve.py --restarts 40
"""
import json, math, random, sys, collections
from ct import DIGITS

AL = 'abcdefghijklmnopqrstuvwxyz'


def load_lm(path='../beale/en_lm.json'):
    d = json.load(open(path))
    q = d['quad']
    tot = sum(q.values())
    lm = {k: math.log10(v / tot) for k, v in q.items()}
    floor = math.log10(0.01 / tot)
    return lm, floor


LM, FLOOR = load_lm()


def score(s):
    return sum(LM.get(s[i:i + 4], FLOOR) for i in range(len(s) - 3)) / max(1, len(s) - 3)


def pairs_of(digits=DIGITS, body=392):
    d = digits[:body]
    return [d[i:i + 2] for i in range(0, len(d), 2)]


def solve(seq, restarts=30, iters=6000, seed=0):
    """seq: list of cipher symbols. Hill-climb a symbol->letter map on quadgram score."""
    syms = sorted(set(seq))
    rnd = random.Random(seed)
    best = (-99.0, None, '')
    # seed the map by frequency: most common symbol -> most common English letter
    freq_order = [s for s, _ in collections.Counter(seq).most_common()]
    eng_order = list('etaoinshrdlcumwfgypbvkjxqz')
    for r in range(restarts):
        if r == 0:
            key = {s: eng_order[i % 26] for i, s in enumerate(freq_order)}
        else:
            letters = list(AL)[:max(len(syms), 1)]
            rnd.shuffle(letters)
            key = {s: letters[i % len(letters)] for i, s in enumerate(syms)}
        cur = ''.join(key[c] for c in seq)
        cs = score(cur)
        for _ in range(iters):
            a, b = rnd.sample(syms, 2)
            key[a], key[b] = key[b], key[a]
            new = ''.join(key[c] for c in seq)
            ns = score(new)
            if ns > cs:
                cs = ns
            else:
                key[a], key[b] = key[b], key[a]
        if cs > best[0]:
            best = (cs, dict(key), ''.join(key[c] for c in seq))
    return best


def main():
    pr = pairs_of()
    out = []
    baseline = score('thequickbrownfoxjumpsoverthelazydogandthenranaway')
    out.append('reference quadgram score of real English: %.3f' % baseline)

    if '--nulls' not in sys.argv:
        sc, key, pt = solve(pr, restarts=int(_arg('--restarts', 30)))
        out.append('\nno nulls removed: %d symbols, %d positions, score %.3f' % (len(set(pr)), len(pr), sc))
        out.append('  ' + pt)
    else:
        results = []
        for period in (3, 4, 5):
            for off in range(period):
                kept = [p for i, p in enumerate(pr) if i % period != off]
                sc, key, pt = solve(kept, restarts=int(_arg('--restarts', 12)))
                results.append((sc, period, off, len(kept), pt))
                print('period %d offset %d -> %d kept, score %.3f' % (period, off, len(kept), sc), flush=True)
        results.sort(reverse=True)
        out.append('\nbest null patterns:')
        for sc, period, off, n, pt in results[:5]:
            out.append('  period %d offset %d (%d kept) score %.3f' % (period, off, n, sc))
            out.append('    ' + pt)
    txt = '\n'.join(out)
    open('solve_out.txt', 'w', encoding='utf-8').write(txt + '\n')
    print(txt)


def _arg(flag, default):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


if __name__ == '__main__':
    main()
