"""Rank candidate French words for each letter-written sign of the ff. 233 key by 5-gram likelihood over all its contexts.
For every occurrence of a sign, the decoded text (key_v4) is rendered with the sign replaced by a candidate word; the
candidate's score is the sum over occurrences of the log-probability gain relative to deleting the sign. Candidates: the
most frequent words of the du Croc corpus plus a hand list of names/places of the 1586 levy.
usage: python gloss_signs.py [key.json] > glosses.txt
"""
import json, sys, re, os, glob, unicodedata, collections
import numpy as np
from solve import clean, lp, V, BLOCK0, NBLK
key = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'key_v4.json', encoding='utf-8'))
L = {int(k): v for k, v in key['letters'].items()}; B = {int(k): v for k, v in key['blocks'].items()}
VOWS = 'aeiou'
FILES = ['ct_233.txt', 'ct_239.txt', 'ct_288.txt', 'ct_366.txt']
KNOWN = {'pi': 'est', 'Ra': 'faictes', 'qu': 'vous', '□': 'ss'}   # accepted readings, rendered as such

def dec(t):
    t = t.rstrip('?')
    if t.isdigit():
        n = int(t)
        if n in L: return L[n]
        if BLOCK0 <= n < BLOCK0 + 5 * NBLK: return B.get(BLOCK0 + 5 * ((n - BLOCK0) // 5), '?') + VOWS[(n - BLOCK0) % 5]
        return '{%s}' % t
    return KNOWN.get(t, '{%s}' % t)

# stream of (text, sign) pieces per file
streams = []
for fn in FILES:
    pieces = []
    for line in open(fn, encoding='utf-8'):
        if line.startswith('#'): continue
        line = line.replace('INS', ' ').replace('/INS', ' ')
        for part in re.split(r'(\[[^\]]*\])', line):
            if part.startswith('['): pieces.append(('T', clean(part[1:-1])))
            else:
                for t in part.split():
                    d = dec(t)
                    if d.startswith('{'): pieces.append(('S', d[1:-1]))
                    else: pieces.append(('T', clean(d)))
    streams.append(pieces)

def lp_text(s):
    p = np.array([ord(c) - 97 for c in s]); p = np.concatenate([[26, 26, 26, 26], p])
    q = ((((p[:-4] * V + p[1:-3]) * V + p[2:-2]) * V + p[3:-1]) * V + p[4:])
    return float(lp[q].sum())

# contexts: for each sign occurrence, 40 letters left, 40 right (other signs dropped)
ctx = collections.defaultdict(list)
for pieces in streams:
    for i, (k, v) in enumerate(pieces):
        if k != 'S': continue
        left = ''.join(x for kk, x in pieces[:i] if kk == 'T')[-40:]
        right = ''.join(x for kk, x in pieces[i + 1:] if kk == 'T')[:40]
        ctx[v].append((left, right))

# candidates
src = ' '.join(open(f, encoding='utf-8', errors='ignore').read() for f in sorted(glob.glob('../ducroc/corpus/*.txt')))
src = unicodedata.normalize('NFKD', src.lower()); src = ''.join(c for c in src if not unicodedata.combining(c))
words = collections.Counter(re.findall(r"[a-z']+", src))
cands = [w.replace("'", '') for w, _ in words.most_common(600) if len(w) > 1]
cands += ['nous', 'vous', 'je', 'de', 'des', 'du', 'et', 'ou', 'que', 'qui', 'a', 'en', 'pour', 'par', 'sur', 'avec', 'sans',
          'affaires', 'nouvelles', 'lettres', 'argent', 'deniers', 'reistres', 'armee', 'levee', 'allemagne', 'angleterre',
          'france', 'guyenne', 'languedoc', 'la rochelle', 'montauban', 'casimir', 'clervant', 'segur', 'condé', 'conde',
          'la reine', 'la reyne', 'le roy', 'la royne dangleterre', 'les princes', 'les eglises', 'les suisses', 'les reistres',
          'hollande', 'lorraine', 'suisse', 'flandres', 'le prince', 'monsieur le prince', 'le duc', 'sedan', 'geneve', 'berne',
          'ecrire', 'escrire', 'faire', 'faictes', 'est', 'sont', 'seront', 'ou', 'vers', 'a qui', 'combien', 'quand', 'comment',
          'ie', 'moy', 'luy', 'eux', 'elle', 'vostre', 'nostre', 'nos', 'vos', 'leurs', 'ceste', 'ce', 'cela', 'tout', 'tous',
          'lenvoy', 'la venue', 'le passage', 'largent', 'le secours', 'ladite', 'ledit', 'depuis', 'longtemps', 'long temps',
          'ung mois', 'deux mois', 'trois mois', 'la mienne', 'les miennes', 'la vostre', 'les vostres', 'point', 'pas', 'plus']
cands = sorted(set(c.replace(' ', '') for c in cands if c.strip()))
cands = [c for c in cands if re.fullmatch(r'[a-z]+', clean(c))]

out = []
for sign, occ in sorted(ctx.items(), key=lambda kv: -len(kv[1])):
    base = sum(lp_text(l + r) for l, r in occ)
    scored = []
    for c in cands:
        cc = clean(c)
        s = sum(lp_text(l + cc + r) for l, r in occ) - base
        # per-letter normalisation is deliberately NOT applied: a longer word must earn its letters
        scored.append((s, c))
    scored.sort(reverse=True)
    out.append(f"## {sign}  ({len(occ)} occurrence{'s' if len(occ) > 1 else ''})")
    for l, r in occ: out.append(f"   …{l[-25:]} [{sign}] {r[:25]}…")
    out.append('   top: ' + ', '.join(f"{c} ({s:+.1f})" for s, c in scored[:8]))
    out.append('   delete sign: +0.0')
print('\n'.join(out))
