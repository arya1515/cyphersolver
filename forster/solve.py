"""Blind homophonic annealer (French 5-gram) for the Forster tokens, plus matched controls and a permutation test.
Model is rebuilt on the first 95% of the corpus; controls are drawn from the held-out last 5%.
usage: python solve.py [restarts]"""
import sys, re, random, collections, statistics, numpy as np, key, ng5fr
random.seed(11); np.random.seed(11)
text = re.sub(r'[^a-z]', '', open('../sp53/corpus_fr.txt', encoding='utf-8').read())
cut = int(len(text)*0.95)
import os
if not os.path.exists('ng5_fr95.npy'):
    open('_train.txt','w').write(text[:cut]); ng5fr.build('_train.txt','ng5_fr95.npy'); os.remove('_train.txt')
TAB = np.load('ng5_fr95.npy'); HELD = text[cut:]
A = 26
def anneal(toks, iters=150000, restarts=8, T0=3.0):
    syms = sorted(set(toks)); S = len(syms); si = {s:i for i,s in enumerate(syms)}
    seq = np.array([si[t] for t in toks])
    best = (-1e9, None)
    for r in range(restarts):
        m = np.random.randint(0, A, S)
        cur = ng5fr.score(TAB, m[seq]); bl = (cur, m.copy())
        for it in range(iters):
            T = T0*(1-it/iters)+0.05
            n = m.copy()
            if random.random() < 0.7: n[random.randrange(S)] = random.randrange(A)
            else:
                i, j = random.sample(range(S), 2); n[i], n[j] = n[j], n[i]
            sc = ng5fr.score(TAB, n[seq])
            if sc >= cur or random.random() < np.exp((sc-cur)/T):
                m, cur = n, sc
                if cur > bl[0]: bl = (cur, m.copy())
        if bl[0] > best[0]: best = bl
    return best[0], {s: 'abcdefghijklmnopqrstuvwxyz'[best[1][si[s]]] for s in syms}
def acc(toks, k, truth):
    return sum(k[t] == truth[t] for t in toks)/len(toks)
def make_control(seed, n_letters=207):
    """French held-out text enciphered with a random key whose homophone multiplicities match Pitt's key:
    the letters of the control text ranked by frequency get the same number of symbols as Pitt's ranked letters."""
    rnd = random.Random(seed)
    start = rnd.randrange(len(HELD)-n_letters); pt = HELD[start:start+n_letters]
    mult = sorted(collections.Counter(key.KEY.values()).values(), reverse=True)  # [3,2,2,...,1]
    letters = [l for l,_ in collections.Counter(pt).most_common()]
    symbols = list(range(1000)); rnd.shuffle(symbols); k = {}
    for i, l in enumerate(letters):
        for _ in range(mult[i] if i < len(mult) else 1): k[str(symbols.pop())] = l
    inv = collections.defaultdict(list)
    for s, l in k.items(): inv[l].append(s)
    ct = [rnd.choice(inv[c]) for c in pt]
    return ct, k, pt
if __name__ == '__main__':
    R = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    toks = key.tokens(); seq = ng5fr.enc(key.decode(toks))
    real = ng5fr.score(TAB, seq)
    # permutation test: permute the 20 plaintext letter identities over Pitt's homophone partition
    letters = sorted(set(key.KEY.values())); null = []
    for i in range(20000):
        p = letters[:]; random.shuffle(p); mp = dict(zip(letters, p))
        null.append(ng5fr.score(TAB, ng5fr.enc(''.join(mp[key.KEY[t]] for t in toks))))
    mu, sd = statistics.mean(null), statistics.pstdev(null)
    print(f'PERMUTATION TEST: Pitt key {real:.1f}; null mean {mu:.1f} sd {sd:.1f} max {max(null):.1f}; z={(real-mu)/sd:.1f}; #>=real {sum(x>=real for x in null)}/20000', flush=True)
    # blind annealer on the target
    sc, k = anneal(toks, restarts=R)
    print(f'TARGET blind: score {sc:.1f} (Pitt key scores {real:.1f}); agreement with Pitt key over tokens {acc(toks,k,key.KEY):.3f}')
    print('   reading:', ' '.join('|' if g==['|'] else ''.join(k[t] for t in g) for g in key.groups()), flush=True)
    for seed in range(6):
        ct, tk, pt = make_control(seed)
        sc, k = anneal(ct, restarts=R)
        truth = ng5fr.score(TAB, ng5fr.enc(pt))
        print(f'CONTROL {seed}: found {sc:.1f} truth {truth:.1f} letters right {acc(ct,k,tk):.3f} | {"".join(k[t] for t in ct)[:80]}', flush=True)
