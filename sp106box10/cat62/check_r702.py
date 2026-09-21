# Decode the group strings the codebreaker glossed on R702 p.2 with the rebuilt table, and print his gloss beside them.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
K = {}
for ln in open(os.path.join(HERE, 'venetian_code.tsv'), encoding='utf-8'):
    if ln.startswith('#') or ln.startswith('group'):
        continue
    g, v, *_ = ln.rstrip('\n').split('\t')
    K[g] = v
LINES = [  # groups as written on R702 p.2, the codebreaker's own gloss
    ('356 318 436 143 435', 'i colonelli'),
    ('341 433 436 154', 'della loro'),
    ('252 359 518 253', 'sendosi'),
    ('167 252 459 459 253', 'conservarsi (one group struck through)'),
    ('362 318 534 261 536 318 557', 'di come temo col'),
    ('165 245 556 253 252 459', 'che possi ser...'),
    ('165 245 556 253 156 526 445 534 261 459', 'che possiamo prometter'),
    ('260 261', 'capitate (sono capita-te)'),
    ('260 359 263', 'in tanto'),
]
hit = tot = 0
for gs, gloss in LINES:
    out = [K.get(g, '[' + g + ']') for g in gs.split()]
    hit += sum(g in K for g in gs.split()); tot += len(gs.split())
    print(f"{gs:45s} {''.join(out):28s} | {gloss}")
print(f'{hit}/{tot} groups covered by the table')
