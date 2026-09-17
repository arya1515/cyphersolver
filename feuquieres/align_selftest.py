import sys, random, align
sys.stdout.reconfigure(encoding='utf-8')
from gc_inventory import load
_,LET,SYL,WOR,_,_ = load()
rnd = random.Random(5)
text = "jattendray avec impatience larrivee du prochain ordinaire pour scavoir comment aura reussy vostre entreprise sur le chasteau de villefranche"
# random code: letters 2 homophones, GC syllables, GC words
code = {}
pool = list(range(1, 368)); rnd.shuffle(pool)
for ch in 'abcdefghijlmnopqrstuvxyz':
    code[ch] = [pool.pop(), pool.pop()]
for s in SYL: code[s] = [pool.pop()]
for w in list(WOR) + ['villefranche', 'mondovi']:
    if pool: code[w] = [pool.pop()]
toks = []; units = []
for w in text.split():
    i = 0
    while i < len(w):
        rest = w[i:]
        u = None
        for k in sorted(code, key=len, reverse=True):
            if len(k) >= 2 and rest.startswith(k) and (len(k) <= 3 or i == 0):
                u = k; break
        if u is None: u = w[i]
        toks.append(rnd.choice(code[u])); units.append(u); i += len(u)
print(len(toks), 'groups;', ' '.join(units))
pw = align.words("jattendrai|jattendray avec impatience larrivee du prochain ordinaire pour savoir|scavoir comment aura reussi|reussy votre|vostre entreprise sur le chateau|chasteau de villefranche")
res = align.align(toks, pw, truth=list(zip(toks, units)))
print('alignments', len(res))
if res:
    sc, m, tr = res[0]
    ok = sum(1 for (g, u), t in zip(tr, units) if u == t)
    print('top alignment correct units', ok, '/', len(units))
    print(' '.join('%d=%s' % (g, u) for g, u in tr))
