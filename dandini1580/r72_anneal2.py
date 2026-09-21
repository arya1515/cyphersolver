"""R72: codes parsed in the R73 frame (decrypt_r72.py -> r72_parsed.json). Nomenclator words stay fixed
plaintext; each 2-digit code gets a letter by swap annealing over a fixed multiset (Italian 4-grams)."""
import json, math, random, re, collections, sys
P = json.load(open('r72_parsed.json'))
corp = open('../../cypher-lang/lang/corpora/it-renaissance.txt', encoding='utf8', errors='ignore').read().lower()
corp = re.sub('[^a-z]', '', corp.translate(str.maketrans('àèéìòùjkwxyv', 'aeeiouiucisu')))[:6000000]
A = 'abcdefghilmnopqrstuz'
cnt = collections.Counter(corp[i:i+4] for i in range(len(corp)-3)); tot = sum(cnt.values())
LM = {k: math.log(v/tot) for k, v in cnt.items()}; fl = math.log(0.01/tot)
lf = collections.Counter(c for c in corp if c in A); lt = sum(lf.values())
fixed = {'che','per','tanto','quello','questa','quanto','non','mente','qua'}
units = []
for c, s in P:
    if len(c) == 2 and c.isdigit(): units.append(('c', c))
    elif s in fixed: units.append(('w', s))
    else: units.append(('w', ''))
codes = sorted({u[1] for u in units if u[0] == 'c'}); ci = {c: i for i, c in enumerate(codes)}
cc = collections.Counter(u[1] for u in units if u[0] == 'c'); N = sum(cc.values())
def text(m): return ''.join(m[ci[u[1]]] if u[0] == 'c' else u[1] for u in units)
def score(m):
    s = text(m); return sum(LM.get(s[i:i+4], fl) for i in range(len(s)-3))
res = []
for rst in range(int(sys.argv[1])):
    random.seed(rst); need = {a: lf[a]/lt*N for a in A}; m = [None]*len(codes)
    for j in sorted(range(len(codes)), key=lambda j: -cc[codes[j]] + random.random()):
        a = max(A, key=lambda a: need[a]); m[j] = a; need[a] -= cc[codes[j]]
    cur = score(m); IT = 80000
    for it in range(IT):
        T_ = 25 * (1 - it/IT) + 0.3
        j, k = random.randrange(len(codes)), random.randrange(len(codes))
        if m[j] == m[k]: continue
        m[j], m[k] = m[k], m[j]; new = score(m)
        if new >= cur or random.random() < math.exp((new-cur)/T_): cur = new
        else: m[j], m[k] = m[k], m[j]
    print(rst, round(cur), text(m)[:160]); sys.stdout.flush(); res.append((cur, m[:]))
cur, m = max(res); print(text(m)); print(json.dumps(dict(zip(codes, m)), sort_keys=True))
