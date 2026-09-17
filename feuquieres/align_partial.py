# Align a plaintext prefix (or suffix) to the cipher, stopping when the text is exhausted: shows how far the
# printed traduction and the enciphered text agree, and the mapping implied.
import sys, math, collections

import align
sys.stdout.reconfigure(encoding='utf-8')

def align_prefix(cipher, plain_words, beam=30000, per_bucket=3000, maxnull=6, reverse=False, fixed=None):
    if reverse:
        cipher = cipher[::-1]
        plain_words = [[w[::-1] for w in alts] for alts in plain_words[::-1]]
    n = len(cipher)
    future = [set() for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        future[i] = future[i + 1] | {cipher[i]}
    def skey(ci2, m2):
        return tuple(sorted((g, u) for g, u in m2.items() if g in future[ci2]))
    fixed = dict(fixed or {})
    if reverse:
        fixed = {g: u[::-1] for g, u in fixed.items()}
    frontier = [(0.0, 0, 0, -1, 0, dict(fixed), ())]
    finals = []
    while frontier:
        new = {}
        for sc, ci, wi, var, off, m, tr in frontier:
            if wi == len(plain_words):
                finals.append((sc, ci, m, tr)); continue
            if ci == n:
                continue
            g = cipher[ci]
            if m.get(g, '') == '' and sum(1 for x in tr if x[1] == '') < maxnull:
                m2 = dict(m); m2[g] = ''
                s2 = sc + math.log(.02)
                key = (ci + 1, wi, var, off, skey(ci + 1, m2))
                if key not in new or new[key][0] < s2:
                    new[key] = (s2, ci + 1, wi, var, off, m2, tr + ((g, ''),))
            variants = [var] if var >= 0 else range(len(plain_words[wi]))
            for v in variants:
                w = plain_words[wi][v]
                rest = w[off:]
                for L in range(1, len(rest) + 1):
                    u = rest[:L]
                    if L == 1:
                        kind = 'letter'
                    elif align.is_syll(u):
                        kind = 'syll'
                    elif L >= 3 and off == 0 and (u in align.GCW or (L == len(rest) and L >= 4)):
                        kind = 'word'
                    else:
                        continue
                    if g in m and m[g] != u:
                        continue
                    m2 = m if g in m else dict(m)
                    if g not in m:
                        m2[g] = u
                    s2 = sc + align.unit_logp('H', kind, u)
                    if kind == 'word' and u not in align.GCW:
                        s2 += math.log(.15)
                    off2 = off + L
                    if off2 == len(w):
                        wi2, v2, off2 = wi + 1, -1, 0
                    else:
                        wi2, v2 = wi, v
                    key = (ci + 1, wi2, v2, off2, skey(ci + 1, m2))
                    if key not in new or new[key][0] < s2:
                        new[key] = (s2, ci + 1, wi2, v2, off2, m2, tr + ((g, u),))
        buckets = collections.defaultdict(list)
        for st in new.values():
            buckets[st[2]].append(st)
        frontier = []
        for b in buckets.values():
            b.sort(key=lambda s: -s[0]); frontier += b[:per_bucket]
        frontier.sort(key=lambda s: -s[0]); frontier = frontier[:beam]
    finals.sort(key=lambda f: -f[0])
    return finals

if __name__ == '__main__':
    paras = align.parse_cipher('herleville.txt')
    which = int(sys.argv[1]); text = sys.argv[2]; rev = '--rev' in sys.argv
    pw = align.words(text)
    fixed = {}
    for l in open('key_partial.txt', encoding='utf-8'):
        if l.strip():
            g, u = l.rstrip().split(chr(9)); fixed[int(g)] = align.uvij(u)
    res = align_prefix(paras[which], pw, reverse=rev, fixed=fixed)
    print('alignments', len(res))
    seen = set()
    for sc, ci, m, tr in res[:400]:
        key = ci
        if key in seen: continue
        seen.add(key)
        print(round(sc, 1), 'cipher groups used', ci, ':', ' '.join('%d=%s' % (g, u if u else '_') for g, u in tr))
        if len(seen) >= 12: break
