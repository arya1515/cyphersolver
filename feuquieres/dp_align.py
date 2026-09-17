# Iterative soft alignment of the Herleville petit-chiffre groups to the printed traduction.
# Round r: Viterbi over (cipher position, text position) with ops: group->unit (letter / GC syllable / GC word or
# stem / whole word), null group, wildcard group (text not in the traduction), skip word (traduction wording not in
# the cipher).  Groups fixed in earlier rounds may only take their fixed unit (or a wildcard at a high price).
# After each round the best path votes for group->unit; consistent, repeated votes are fixed; iterate.
# u/v and i/j are merged (the Grand Chiffre design).  usage: python dp_align.py
import sys, math, collections
sys.stdout.reconfigure(encoding='utf-8')
from gc_inventory import load as gcload
_T, _L, GCSYL, GCWOR, _N, _U = gcload()
def uv(w): return w.replace('v', 'u').replace('j', 'i')
GCW = {uv(w) for w in GCWOR} | {'roy', 'roi'}
GCS = {uv(w) for w in GCSYL}
VOW = set('aeiouy')

def parse_cipher(path):
    paras = [[]]
    for l in open(path, encoding='utf-8'):
        if l.startswith('#'):
            continue
        if not l.strip():
            if paras[-1]: paras.append([])
            continue
        paras[-1] += [int(x) for x in l.split()]
    return [p for p in paras if p]

P1 = "je mande a monsieur de catinat que le roy vous permettoit de demander la contribution au pays de mondovi et que si vous jugez quil convient au service du roy de les exempter mesme de permettre aux habitans dudit pays de raser la citadelle dudit mondovi de le faire"
P2 = "jattendray avec impatience larrivee du prochain ordinaire pour scavoir comment aura reussy vostre entreprise sur le chasteau de villefranche"

def flat(text):
    words = [uv(w) for w in text.split()]
    s = ''.join(words)
    starts = set(); ends = set(); p = 0
    for w in words:
        starts.add(p); p += len(w); ends.add(p)
    return s, starts, ends

def unit_kind(u, at_word_start, at_word_end):
    L = len(u)
    if L == 1:
        return 'letter', math.log(.36)
    if L == 2 and (u[0] not in VOW and u[1] in VOW):
        return 'syll', math.log(.40) + (0 if u in GCS else math.log(.5))
    if L == 2:
        return 'syll', math.log(.40) + math.log(.35 if u in GCS else .12)
    if L == 3 and u in GCS:
        return 'syll', math.log(.40) + math.log(.35)
    if L == 3 and u[0] not in VOW and u[1] in VOW and u[2] not in VOW and at_word_end:
        return 'syll', math.log(.40) + math.log(.10)   # CVC closing a word (e.g. 'nat', 'mand')
    if at_word_start and L >= 2 and u in GCW:
        return 'word', math.log(.22)
    if at_word_start and at_word_end and L >= 4:
        return 'word', math.log(.22) + math.log(.15)   # whole word not in the GC list (place names)
    return None, None

def viterbi(cipher, text, fixed, wild_pen=math.log(.05), skip_pen_per_letter=math.log(.35), null_pen=math.log(.03)):
    s, starts, ends = flat(text)
    n, m = len(cipher), len(s)
    NEG = -1e18
    best = [[NEG] * (m + 1) for _ in range(n + 1)]
    back = [[None] * (m + 1) for _ in range(n + 1)]
    best[0][0] = 0.0
    # precompute next word end from a position
    word_end_from = {}
    for st in starts:
        e = st
        while e < m and (e + 1) not in ends:
            e += 1
        word_end_from[st] = e + 1
    for ci in range(n + 1):
        for ti in range(m + 1):
            sc = best[ci][ti]
            if sc <= NEG / 2:
                continue
            # skip a word (text not in cipher)
            if ti in starts:
                e = word_end_from[ti]
                v = sc + skip_pen_per_letter * (e - ti) - 1.5
                if v > best[ci][e]:
                    best[ci][e] = v; back[ci][e] = (ci, ti, '<skip>')
            if ci == n:
                continue
            g = cipher[ci]
            fx = fixed.get(g)
            # null
            if fx is None or fx == '':
                v = sc + (null_pen if fx is None else 0.0)
                if v > best[ci + 1][ti]:
                    best[ci + 1][ti] = v; back[ci + 1][ti] = (ci, ti, '')
            # wildcard
            v = sc + (wild_pen if fx is None else wild_pen + math.log(.1))
            if v > best[ci + 1][ti]:
                best[ci + 1][ti] = v; back[ci + 1][ti] = (ci, ti, '?')
            # consume units
            if fx:
                cands = [len(fx)] if s.startswith(fx, ti) else []
            else:
                cands = range(1, 13)
            for L in cands:
                if ti + L > m:
                    break
                u = s[ti:ti + L]
                # units do not cross word boundaries
                if any((ti + k) in starts for k in range(1, L)):
                    break
                kind, lp = unit_kind(u, ti in starts, (ti + L) in ends)
                if kind is None:
                    continue
                if fx:
                    lp = 0.0
                v = sc + lp
                if v > best[ci + 1][ti + L]:
                    best[ci + 1][ti + L] = v; back[ci + 1][ti + L] = (ci, ti, u)
    # end: all cipher consumed, all text consumed
    ci, ti = n, m
    path = []
    while (ci, ti) != (0, 0):
        pci, pti, u = back[ci][ti]
        if u == '<skip>':
            path.append((None, s[pti:ti]))
        else:
            path.append((cipher[pci], u))
        ci, ti = pci, pti
    path.reverse()
    return best[n][m], path

def run(paras, texts, rounds=8):
    fixed = {}
    for r in range(rounds):
        votes = collections.defaultdict(collections.Counter)
        total = 0.0; paths = []
        for cipher, text in zip(paras, texts):
            sc, path = viterbi(cipher, text, fixed)
            total += sc; paths.append(path)
            for g, u in path:
                if g is not None and u != '?':
                    votes[g][u] += 1
        # fix: groups whose votes are unanimous and (count >= 2 or already fixed)
        newfixed = dict(fixed)
        for g, c in votes.items():
            if len(c) == 1:
                u, k = next(iter(c.items()))
                if k >= 2 or g in fixed:
                    newfixed[g] = u
        # also fix singletons of groups that appear only once in the corpus (they cannot conflict)
        allc = collections.Counter(g for p in paras for g in p)
        for g, c in votes.items():
            if len(c) == 1 and allc[g] == 1:
                newfixed[g] = next(iter(c))
        conflicts = {g: dict(c) for g, c in votes.items() if len(c) > 1}
        print('round', r, 'score', round(total, 1), 'fixed', len(newfixed), 'conflicting groups', len(conflicts))
        if newfixed == fixed:
            break
        fixed = newfixed
    for path in paths:
        print(' '.join(('<%s>' % u) if g is None else ('%d=%s' % (g, u if u else '_')) for g, u in path))
    print('CONFLICTS', conflicts)
    return fixed, paths

if __name__ == '__main__':
    paras = parse_cipher('herleville.txt')
    fixed, paths = run(paras, [P1, P2])
    with open('herleville_key.txt', 'w', encoding='utf-8') as f:
        for g in sorted(fixed):
            f.write('%d\t%s\n' % (g, fixed[g]))
    print('key groups', len(fixed))
