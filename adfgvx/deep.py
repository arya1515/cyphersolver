"""Deeper repair on the messages that showed German under a shallow search.

The shallow pass (repair.py) allows at most two inserted letters. Page 132 came back with

    ... WIEDERHQLE TTELEG ...

which is "wiederhole telegramm", repeat the telegram - unmistakable German military traffic, so the
key is right and only the reconstruction is short. Page 146 likewise showed STELLEN, RICHTIGEN.

This widens the search on a single message: up to four insertions, and insertions combined with a
deletion, against one nominated key rather than all fourteen. Scoring stays the same. The point is
not to score well but to produce a reading a reader can check, so the best few candidates are printed
in full.

Usage:
    python deep.py 132 17 4        - page 132, key of length 17, up to 4 insertions
"""
import itertools, json, sys

import repair


def deep(page, keylen, max_ins=4, topn=8):
    keys = [k for k in repair.load_keys() if k['n'] == keylen]
    msgs = [m for m in repair.load_messages() if m['page'].startswith(page)]
    if not msgs:
        print('no such page'); return
    m = msgs[0]
    ct = m['ct']
    print('page %s, %d letters, %d key(s) of length %d' % (m['page'], len(ct), len(keys), keylen))
    best = []
    for k in keys:
        for n_ins in range(0, max_ins + 1):
            if (len(ct) + n_ins) % 2:
                continue
            for combo in itertools.combinations_with_replacement(range(len(ct) + 1), n_ins):
                s, off = ct, 0
                for p in combo:
                    s = s[:p + off] + repair.PLACE + s[p + off:]
                    off += 1
                pt = repair.unfractionate(repair.untranspose(s, k['perm'], k['n'], 'B'), k['square'])
                best.append((repair.score(pt), n_ins, combo, pt))
    best.sort(key=lambda x: -x[0])
    seen = set()
    shown = 0
    for sc, n_ins, combo, pt in best:
        if pt in seen:
            continue
        seen.add(pt)
        print('\n  score %7.1f   %d insertions at %s' % (sc, n_ins, combo))
        print('  %s' % pt)
        shown += 1
        if shown >= topn:
            break


if __name__ == '__main__':
    page = sys.argv[1] if len(sys.argv) > 1 else '132'
    klen = int(sys.argv[2]) if len(sys.argv) > 2 else 17
    mx = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    deep(page, klen, mx)
