"""Match repeated code groups of R1957 against repeated words of PC 8 no. 5263 by relative position."""
import re, collections
t = open('pc08.txt', encoding='utf8').read().split('\n')[40358:40410]   # archive.org politischecorres08freduoft djvu text
t = ' '.join(l for l in t if not re.match(r'\s*(Vergl|[-\d\s^]*$|1734)', l)).lower()
w = re.findall(r"[a-zà-ÿ]+", t)[9:]          # drop the clear opening "j'ai reçu votre dépêche du 14 de ce mois"
ct = open('ct.txt').read().split()
W = collections.defaultdict(list); C = collections.defaultdict(list)
for i, x in enumerate(w): W[x].append(i / len(w))
for i, x in enumerate(ct): C[x].append(i / len(ct))
res = []
for g, cp in C.items():
    if len(cp) < 3: continue
    for x, wp in W.items():
        if len(wp) != len(cp) or len(x) < 3: continue
        d = max(abs(a - b) for a, b in zip(cp, wp))
        if d < 0.06: res.append((round(d, 3), g, x, len(cp)))
for r in sorted(res): print(r)
