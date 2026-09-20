"""Slide the transcribed cipher of f.370 against the Brienne plaintext.
Simple substitution => the map must be both a function (one letter per group)
and injective (one group per letter). Score = groups placed before the first clash."""
import re, unicodedata, sys

def norm(t):
    t=unicodedata.normalize('NFD',t)
    t=''.join(c for c in t if unicodedata.category(c)!='Mn').lower()
    t=t.replace('j','i').replace('v','u')          # period orthography
    return re.sub(r'[^a-z]','',t)

PLAIN = norm("""
Le Cardinal de boudy aura passe pres de vous il y peut ja avoir quelque jours
lequel vous aura fait entendre de mes nouvelles et la disposition en laquelle il
aura laisse les choses il pourra destre bien tost suivy par le marquis de pisany
pour aller vers le pape au nom des Catholiques de ce royaume mes serviteurs
Ce que ie croy vous aura fait changer la deliberation de vostre partement pour
vous en revenir ainsy que par vostre derniere vous monstriez estre en volonte de
faire car vous auez assez iuge que sur cette rencontre mes affaires de dela nont
besoin destre abandonnees de vostre presence
""")

CT=[]
for line in open('ct370.txt'):
    if line.startswith('#'): continue
    CT+=line.split()

def run(off, ct):
    """place groups 1:1 from PLAIN[off:]; stop at first inconsistency"""
    g2l={}; l2g={}
    for i,g in enumerate(ct):
        j=off+i
        if j>=len(PLAIN): return i,g2l
        ch=PLAIN[j]
        if g in g2l and g2l[g]!=ch: return i,g2l
        if ch in l2g and l2g[ch]!=g: return i,g2l
        g2l[g]=ch; l2g[ch]=g
    return len(ct),g2l

best=[]
for off in range(0,len(PLAIN)-20):
    n,_=run(off,CT)
    best.append((n,off))
best.sort(reverse=True)
print('plaintext length',len(PLAIN))
print('best offsets (groups placed before a clash, no nulls allowed):')
for n,off in best[:8]:
    print(f'  off={off:4d}  placed={n:3d}   plain starts "{PLAIN[off:off+26]}"')
n,m=run(best[0][1],CT)
print('\nmap at best offset:', {k:m[k] for k in sorted(m,key=lambda s:(len(s),s))})
