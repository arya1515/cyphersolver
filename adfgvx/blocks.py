"""Norbert's 2017 method, made systematic: up to two block edits (insert 1-5 placeholders or delete 1-5 letters)
at group boundaries, every key, every message, scored by the German quadgram model. Exhaustive at boundaries;
the annealer (gaps.py) then refines position within the group.

Usage: python blocks.py [procs]   -> blocks_out.txt
"""
import itertools, multiprocessing, sys
import gaps, lm_de, repair

DELTAS = list(range(-5, 0)) + list(range(1, 6))

def apply(ct, edits):
    s = ct
    for pos, d in sorted(edits, reverse=True):
        if d > 0:
            s = s[:pos] + '#' * d + s[pos:]
        else:
            s = s[:pos] + s[pos - d:]
    return s

def job(args):
    page, ct, key = args
    L = len(ct)
    bounds = list(range(0, L + 1, 5))
    best = []
    seen = set()
    cands = [()]
    cands += [((p, d),) for p in bounds for d in DELTAS]
    cands += [((p, d), (q, e)) for p, q in itertools.combinations(bounds, 2) for d in DELTAS for e in DELTAS]
    for edits in cands:
        c = apply(ct, edits)
        if len(c) % 2 or len(c) < 20:
            continue
        pt = gaps.decrypt(c, key)
        sc = lm_de.per(pt)
        best.append((sc, edits, pt))
    best.sort(key=lambda x: -x[0])
    return page, key['n'], key.get('note', ''), best[:3]

def main(procs=8):
    keys = repair.load_keys()
    msgs = gaps.parse()
    jobs = [(m['page'], m['ct'], k) for m in msgs for k in keys]
    out = open('blocks_out.txt', 'w', encoding='utf-8')
    with multiprocessing.Pool(procs) as pool:
        for page, n, note, best in pool.imap_unordered(job, jobs):
            for sc, edits, pt in best[:1]:
                line = '%-24s len%-3d %6.3f %-28s %s' % (page, n, sc, str(edits), pt[:90])
                print(line); out.write(line + '\n'); out.flush()

if __name__ == '__main__':
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 8)
