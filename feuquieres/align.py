# Known-plaintext alignment of a two-part code: beam search over (cipher position, plaintext position, mapping).
# Units: null (0 letters), letter (1), syllable (2-3: CV, CVC-ish, common digraphs), word/stem (whole word or a
# stem >= 3 letters).  Same group -> same unit throughout (hard).  Word alternatives allow period spellings.
# usage: python align.py  -> prints best alignments and the derived key
import re, sys, math, collections, heapq, itertools
sys.stdout.reconfigure(encoding='utf-8')
LOWMAX = 100
from gc_inventory import load as _gcload
_T, _L, GCSYL, GCWOR, _N, _U = _gcload()
GCW = {w.replace('v', 'u').replace('j', 'i') for w in GCWOR} | {'roy', 'roi'}
GCS = {w.replace('v', 'u').replace('j', 'i') for w in GCSYL}
SOFT = '--soft' in sys.argv
WIDE = '--wide' in sys.argv
VOW = set('aeiouy')

def parse_cipher(path):
    paras = [[]]
    for l in open(path, encoding='utf-8'):
        if l.startswith('#'):
            continue
        if not l.strip():
            if paras[-1]:
                paras.append([])
            continue
        paras[-1] += [int(x) for x in l.split()]
    return [p for p in paras if p]

# plaintext as list of words; each word a list of spelling alternatives
P1 = """je mande a monsieur|m de catinat que le roi|roy vous permettait|permettoit de demander la contribution au
pays|pais de mondovi|mondevis|mondevi et que si vous jugez quil convient au service du roi|roy de les exempter
meme|mesme de permettre aux habitans dudit pays|pais de raser la citadelle dudit mondovi|mondevis|mondevi de le faire"""
P2 = """jattendrai|jattendray avec impatience larrivee du prochain ordinaire pour savoir|scavoir comment aura
reussi|reussy votre|vostre entreprise sur le chateau|chasteau de villefranche"""

def uvij(w):
    return w.replace('v', 'u').replace('j', 'i')

def words(p):
    return [[uvij(a) for a in w.split('|')] for w in p.split()]

def is_syll(u):
    if WIDE:
        if len(u) == 2:
            return True
        if len(u) == 3:
            return (u[0] not in VOW and u[1] in VOW) or (u[0] in VOW and u[1] not in VOW) or u in ('que', 'qui')
        if len(u) == 4:
            return u in ('ment', 'tion', 'sion', 'ment', 'ance', 'ence', 'euse', 'eaux', 'aire', 'oire', 'iere')
        return False
    if len(u) == 2:
        return (u[0] not in VOW and u[1] in VOW) or u in ('en', 'on', 'an', 'in', 'un', 'ou', 'oi', 'ai', 'au', 'eu',
                                                            'es', 'is', 'us', 'it', 'st', 'nt', 'ar', 'er', 'or', 'ur', 'ez')
    if len(u) == 3:
        return (u[0] not in VOW and u[1] in VOW and u[2] in 'nrstl') or u in ('que', 'qui', 'quo', 'qua', 'ent', 'ant',
                                                                             'ion', 'tre', 'pre', 'pro', 'tra', 'tri',
                                                                             'con', 'com', 'per', 'par', 'pou', 'sou')
    return False

def unit_logp(cls, kind, u):
    """cls 'L' (<100) or 'H'; kind in null/letter/syll/word."""
    return {'null': math.log(.02), 'letter': math.log(.36), 'syll': math.log(.40), 'word': math.log(.22)}[kind]

def align(cipher, plain_words, beam=30000, m0=None, sc0=0.0, tr0=(), per_bucket=3000, lo=0.8, hi=3.6, maxnull=8, truth=None):
    """cipher: list of groups; plain_words: list of alternative lists. Returns list of (score, mapping, trace)."""
    # state: (ci, wi, variant, off) ; mapping dict ; trace list
    n = len(cipher)
    # letters remaining from word wi onwards (min over variants)
    rem = [0] * (len(plain_words) + 1)
    for i in range(len(plain_words) - 1, -1, -1):
        rem[i] = rem[i + 1] + min(len(v) for v in plain_words[i])
    # groups still to come after position ci: only their assignments matter for pruning/merging
    future = [set() for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        future[i] = future[i + 1] | {cipher[i]}
    def skey(ci2, m2):
        return tuple(sorted((g, u) for g, u in m2.items() if g in future[ci2]))
    def feasible(ci2, wi2, v2, off2):
        rg = n - ci2
        if wi2 >= len(plain_words):
            rl = 0
        else:
            w = plain_words[wi2][v2] if v2 >= 0 else min(plain_words[wi2], key=len)
            rl = rem[wi2 + 1] + len(w) - off2
        if rg == 0:
            return rl == 0
        if SOFT:
            return rl <= (hi + 1.5) * rg
        return lo * rg - 2 <= rl <= hi * rg
    start = (sc0, 0, 0, -1, 0, dict(m0 or {}), tuple(tr0))
    frontier = [start]
    finals = []; ends = []; last = frontier
    while frontier:
        new = {}
        for sc, ci, wi, var, off, m, tr in frontier:
            if ci == n:
                if wi == len(plain_words) and off == 0:
                    finals.append((sc, m, tr))
                else:
                    ends.append((sc, wi, off, tr))
                continue
            if wi == len(plain_words):
                # cipher left over: only nulls
                g = cipher[ci]
                if m.get(g, '') == '':
                    m2 = dict(m); m2[g] = ''
                    key = (ci + 1, wi, var, off, skey(ci + 1, m2))
                    s2 = sc + unit_logp('L' if g < LOWMAX else 'H', 'null', '')
                    if feasible(ci + 1, wi, var, off) and (key not in new or new[key][0] < s2):
                        new[key] = (s2, ci + 1, wi, var, off, m2, tr + ((g, ''),))
                continue
            g = cipher[ci]
            cls = 'L' if g < LOWMAX else 'H'
            # skip a plaintext word (wording differs), only at word start
            if SOFT and off == 0 and wi < len(plain_words):
                s2 = sc + math.log(.25) * min(len(v) for v in plain_words[wi]) - 2.0
                key = (ci, wi + 1, -1, 0, skey(ci, m))
                if feasible(ci, wi + 1, -1, 0) and (key not in new or new[key][0] < s2):
                    new[key] = (s2, ci, wi + 1, -1, 0, m, tr + ((-1, '<skip:%s>' % plain_words[wi][0]),))
            # wildcard: a group whose text is not in the traduction (wording differs); does not bind the key
            if SOFT and sum(1 for x in tr if x[1] == '?') < int(0.3 * n) and g not in m:
                s2 = sc + math.log(.06)
                key = (ci + 1, wi, var, off, skey(ci + 1, m))
                if feasible(ci + 1, wi, var, off) and (key not in new or new[key][0] < s2):
                    new[key] = (s2, ci + 1, wi, var, off, m, tr + ((g, '?'),))
            # null
            if m.get(g, '') == '' and sum(1 for x in tr if x[1] == '') < (maxnull * 2 if SOFT else maxnull):
                m2 = dict(m); m2[g] = ''
                s2 = sc + unit_logp(cls, 'null', '')
                key = (ci + 1, wi, var, off, skey(ci + 1, m2))
                if feasible(ci + 1, wi, var, off) and (key not in new or new[key][0] < s2):
                    new[key] = (s2, ci + 1, wi, var, off, m2, tr + ((g, ''),))
            # consume letters of the current word
            variants = [var] if var >= 0 else range(len(plain_words[wi]))
            for v in variants:
                w = plain_words[wi][v]
                rest = w[off:]
                for L in range(1, len(rest) + 1):
                    u = rest[:L]
                    if L == 1:
                        kind = 'letter'
                    elif is_syll(u):
                        kind = 'syll'
                    elif L >= 3 and off == 0 and (u in GCW or (L == len(rest) and L >= 4)):
                        kind = 'word'
                    else:
                        continue
                    conflict = g in m and m[g] != u
                    if conflict:
                        continue
                    m2 = m if g in m else dict(m)
                    if g not in m:
                        m2[g] = u
                    s2 = sc + unit_logp(cls, kind, u) + (math.log(.01) if conflict else 0.0)
                    if conflict:
                        u = u + '!'
                    if kind == 'word' and u not in GCW:
                        s2 += math.log(.15)  # word not in the Grand Chiffre list (proper name etc.)
                    if kind == 'syll' and u not in GCS and len(u) == 3:
                        s2 += math.log(.3)
                    off2 = off + L
                    if off2 == len(w):
                        wi2, v2, off2 = wi + 1, -1, 0
                    else:
                        wi2, v2 = wi, v
                    key = (ci + 1, wi2, v2, off2, skey(ci + 1, m2))
                    if feasible(ci + 1, wi2, v2, off2) and (key not in new or new[key][0] < s2):
                        new[key] = (s2, ci + 1, wi2, v2, off2, m2, tr + ((g, u),))
        # prune: keep best `beam` by score, but also keep diversity in (ci, wi)
        # bucket by plaintext progress (word index) so that fast- and slow-consuming paths both survive
        buckets = collections.defaultdict(list)
        for st in new.values():
            buckets[st[2]].append(st)
        frontier = []
        for b in buckets.values():
            b.sort(key=lambda s: -s[0])
            frontier += b[:per_bucket]
        frontier.sort(key=lambda s: -s[0])
        frontier = frontier[:beam]
        if truth is not None:
            ci_now = frontier[0][1] if frontier else None
            k = len(tr0) if False else 0
            # true prefix of length ci_now
            tp = tuple(truth[:ci_now]) if ci_now is not None else None
            gen = any(tuple(st[6]) == tp for st in new.values())
            kept = any(tuple(st[6]) == tp for st in frontier)
            if not kept:
                print('TRUTH LOST at ci', ci_now, 'generated' if gen else 'NOT GENERATED', 'frontier', len(frontier), 'new', len(new))
                if gen:
                    st = [st for st in new.values() if tuple(st[6]) == tp][0]
                    print('   true score', round(st[0], 1), 'worst kept', round(frontier[-1][0], 1), 'true wi', st[2])
                truth = None
        if not frontier:
            print('DEAD END: last frontier at ci', ci, 'best partial:')
            for st in sorted(last, key=lambda s: -s[0])[:2]:
                print(round(st[0], 1), 'word', st[2], 'off', st[4], ' '.join('%d=%s' % (g, u if u else '_') for g, u in st[6]))
        last = frontier
    finals.sort(key=lambda f: -f[0])
    if not finals and ends:
        ends.sort(key=lambda e: (-e[1], -e[0]))
        for sc, wi, off, tr in ends[:3]:
            print('INCOMPLETE reached word', wi, 'of', len(plain_words), 'off', off, round(sc, 1))
            print(' '.join('%d=%s' % (g, u if u else '_') for g, u in tr))
    return finals

if __name__ == '__main__':
    paras = parse_cipher('herleville.txt')
    pw = [words(P1), words(P2)]
    # joint alignment: paragraph 1 then 2 with the mapping carried over
    res1 = align(paras[0], pw[0])
    print('P1 alignments', len(res1))
    for sc, m, tr in res1[:3]:
        print(round(sc, 1), ' '.join('%d=%s' % (g, u if u else '_') for g, u in tr))
    best = []
    for sc, m, tr in res1[:20]:
        # continue with P2 from this mapping
        res2 = align(paras[1], pw[1], m0=m, sc0=sc, tr0=tr)
        best += res2[:5]
    best.sort(key=lambda f: -f[0])
    for sc, m, tr in best[:3]:
        print('\nJOINT', round(sc, 1))
        print(' '.join('%d=%s' % (g, u if u else '_') for g, u in tr))
    if best:
        sc, m, tr = best[0]
        with open('herleville_key.txt', 'w', encoding='utf-8') as f:
            for g in sorted(m):
                f.write('%d\t%s\n' % (g, m[g]))
        print('key written: %d groups' % len(m))
