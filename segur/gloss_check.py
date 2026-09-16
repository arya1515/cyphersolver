"""Compare the hypotheses for each letter-written sign of the ff. 233 key against each other by 5-gram likelihood
(same machinery as gloss_signs.py, but only like-for-like candidates from the reading notes, so word length does not
decide). Output: per sign, candidates sorted by total log-probability gain over all occurrences."""
import re, collections
import numpy as np
from gloss_signs import ctx, lp_text, clean
HYP = {
    'na':  ['affaires', 'nouvelles', 'lettres', 'depesches', 'negotiations', 'gens', 'forces'],
    'gne': ['je', 'nous', 'ie', 'moy', 'de', 'a'],
    'gna': ['nous', 'de', 'a', 'me', 'vous', 'de nous', 'pour nous'],
    'X':   ['de', 'a', 'pour', 'que', 'daller', 'et', 'de vouloir'],
    'gla': ['par', 'de', 'selon', 'a', 'suivant', 'et', 'pour'],
    'pe':  ['ou', 'par ou', 'a qui', 'comment', 'si', 'que', 'quand'],
    'pu':  ['vous', 'nous', 'ou', 'vous escrire', 'je', 'me', 'luy'],
    'H':   ['hollande', 'lorraine', 'allemagne', 'angleterre', 'flandres', 'suisse', 'france', 'guyenne', 'gascogne', 'languedoc', 'dauphine', 'italie', 'espagne', 'ce temps', 'la saison', 'ceste saison', 'hyver', 'este'],
    'L':   ['hollande', 'lorraine', 'allemagne', 'angleterre', 'flandres', 'suisse', 'france', 'guyenne', 'gascogne', 'languedoc', 'dauphine', 'italie', 'espagne', 'ce temps', 'la saison', 'ceste saison', 'hyver', 'este'],
    'qua': ['que vous', 'dallemagne', 'de vous', 'qui', 'des reistres', 'de nos amis', 'estrangers', 'nous', 'me'],
    'Ne':  ['nous', 'ie', 'je', 'et', 'en', 'nous y'],
    '180': ['la reyne dangleterre', 'langleterre', 'la reyne', 'catherine', 'elisabeth', 'la royne', 'la reyne mere', 'les eglises', 'casimir', 'le duc casimir', 'les princes', 'angleterre', 'la rochelle', 'montauban', 'les suisses', 'dannemarc', 'le roy de dannemarc', 'lescosse'],
    '900': ['nous', 'vous', 'je', 'ne', 'de', 'vous prier', 'vous prier de', 'ma part', 'par ma part', 'rechef', 'nouveau', 'bien', 'tres'],
    'e':   ['longtemps', 'long temps', 'vostre partement', 'angleterre', 'dix mois', 'six mois', 'trois mois', 'deux mois', 'ung mois', 'quatre mois', 'noel', 'pasques', 'lhyver', 'vostre depart', 'le mois de janvier', 'janvier', 'fevrier', 'decembre', 'novembre', 'octobre'],
    '215': ['l', 'il', 'sil', 'quil', 'ne', 'en'],
    'gu':  ['et', 'de', 'a', 'en', 'que', 'ou', 'le', 'la', 'pour', 'par', 'vous', 'nous', 'je', 'me', 'se'],
}
for sign, cands in HYP.items():
    occ = ctx.get(sign)
    if not occ: print('##', sign, 'no occurrence'); continue
    base = sum(lp_text(l + r) for l, r in occ)
    scored = sorted(((sum(lp_text(l + clean(c) + r) for l, r in occ) - base, c) for c in cands), reverse=True)
    print(f"## {sign} ({len(occ)} occ.)  " + ' | '.join(f"{c} {s:+.1f}" for s, c in scored))
