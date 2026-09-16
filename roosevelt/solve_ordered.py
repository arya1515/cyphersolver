"""Ordered-key attack on the Roosevelt 1935 number block.

The block is a permutation of 1..52 (singles 1-9, tick-joined pairs 10-52). Two cipher readings are testable:
  (a) homophonic substitution whose 52 homophones are assigned to letters in alphabetical order
      (A gets the lowest numbers, Z the highest: the Thomas #5 comment key type). Plaintext = L(seq).
  (b) the block is a numerical transposition key derived from a key phrase by ranking its letters
      (XMAS -> 4 2 1 3). Then the phrase = L(inverse permutation), again with L nondecreasing.
Both reduce to: find a nondecreasing map L: 1..52 -> a..z such that L applied to the sequence reads as
English. Simulated annealing over the 51 boundary flags with the Copenhagen 5-gram English model.
Reversed alphabet and zero-separated segments are also run. --control N runs the same attack on N
synthetic 52-letter English passages enciphered with random ordered homophonic keys.
"""
import sys, math, random, pickle, pathlib, re, collections
HERE = pathlib.Path(__file__).parent
sys.path.insert(0, str(HERE.parent / 'copenhagen'))
N = 5; D = 0.75
class LM:  # identical to copenhagen/solve.py
    def prob(self, hist, c):
        key = hist + c; v = self.memo.get(key)
        if v is not None: return v
        if not hist: p = self.uni.get(c, 1e-6)
        else:
            tot = self.ctxtot.get(hist); lower = self.prob(hist[1:], c)
            p = lower if not tot else (max(self.counts.get(hist + c, 0) - D, 0) + D * self.ctxtypes[hist] * lower) / tot
        self.memo[key] = p; return p
    def logp(self, hist, c):
        if len(hist) > N - 1: hist = hist[-(N-1):]
        return math.log(self.prob(hist, c))
    def score(self, segments):
        s = 0.0
        for seg in segments:
            hist = ''
            for c in seg: s += self.logp(hist, c); hist = (hist + c)[-4:]
        return s
    def coverage(self, text):
        cov = 0; i = 0
        while i < len(text):
            for L in range(min(12, len(text) - i), 2, -1):
                if text[i:i+L] in self.vocab: cov += L; i += L; break
            else: i += 1
        return cov / max(len(text), 1)
d = pickle.load(open(HERE.parent / 'copenhagen' / 'lm_en.bin', 'rb'))
lm = LM.__new__(LM); lm.__dict__.update(d); lm.memo = {}
ALPHA = 'abcdefghijklmnopqrstuvwxyz'

SEQ = [1,7,2,10,15,17,19,21,26,8,32,33,20,37, 16,27,12,34,38,28,22,39,40,41,42,48,44, 9,3,13, 18,4,23,24,46,29,35,51,5,43,47, 6,11,36,50,52,30,49,45,25,31,14]
CUTS = [14, 27, 30, 41]  # zero groups

def inverse(seq):
    inv = [0] * len(seq)
    for i, v in enumerate(seq): inv[v - 1] = i + 1
    return inv

def decode(seq, key, segs):
    txt = ''.join(ALPHA[key[v - 1]] for v in seq)
    if not segs: return [txt]
    out = []; a = 0
    for c in CUTS + [len(seq)]: out.append(txt[a:c]); a = c
    return out

def anneal(seq, segs, iters, seed):
    rnd = random.Random(seed)
    key = sorted(rnd.randrange(26) for _ in seq)          # nondecreasing letter index per number 1..52
    cur = lm.score(decode(seq, key, segs)); best = (cur, key[:])
    T0 = 3.0
    for it in range(iters):
        T = T0 * (1 - it / iters) + 0.05
        k = key[:]
        i = rnd.randrange(len(k))
        mv = rnd.random()
        if mv < 0.5:   # shift one boundary: raise key[i] up to next value / lower down to previous
            lo = k[i-1] if i else 0; hi = k[i+1] if i + 1 < len(k) else 25
            if lo == hi: continue
            k[i] = rnd.randint(lo, hi)
        else:          # move a whole block of equal letters up or down by one
            v = k[i]; j0 = i
            while j0 and k[j0-1] == v: j0 -= 1
            j1 = i
            while j1 + 1 < len(k) and k[j1+1] == v: j1 += 1
            dv = rnd.choice((-1, 1)); nv = v + dv
            if nv < 0 or nv > 25: continue
            if (dv < 0 and j0 and k[j0-1] > nv) or (dv > 0 and j1 + 1 < len(k) and k[j1+1] < nv): continue
            for j in range(j0, j1 + 1): k[j] = nv
        sc = lm.score(decode(seq, k, segs))
        if sc >= cur or rnd.random() < math.exp((sc - cur) / T):
            key, cur = k, sc
            if cur > best[0]: best = (cur, key[:])
    return best

def attack(seq, segs, restarts, iters, label, seed0=0):
    res = []
    for r in range(restarts):
        sc, key = anneal(seq, segs, iters, seed0 + r)
        txt = ' '.join(decode(seq, key, segs))
        res.append((sc, txt))
    res.sort(reverse=True)
    seen = set(); out = []
    for sc, txt in res:
        if txt in seen: continue
        seen.add(txt); out.append((sc, txt))
    print(f'== {label}')
    for sc, txt in out[:5]:
        print(f'  {sc/52:7.3f}/letter  cov {lm.coverage(txt.replace(" ", "")):.2f}  {txt}')
    return out[0]

def arg(flag, default=None):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default
RESTARTS = int(arg('--restarts', 30)); ITERS = int(arg('--iters', 15000))

if '--control' in sys.argv:
    # synthetic: 52-letter English passages, ordered homophonic key sized by letter counts, numbers shuffled within letter
    corp = pathlib.Path(arg('--corpus', '.'))
    texts = []
    for f in sorted(corp.glob('corp_en_*.txt'))[:3]:
        t = re.sub('[^a-z]', '', f.read_text(encoding='utf-8', errors='ignore').lower()); texts.append(t)
    big = ''.join(texts)
    rnd = random.Random(99); hits = 0; n = int(arg('--control'))
    for c in range(n):
        i = rnd.randrange(len(big) - 60); pt = big[i:i+52]
        cnt = collections.Counter(pt); nums = iter(range(1, 53)); table = {}
        for ch in sorted(cnt):
            table[ch] = [next(nums) for _ in range(cnt[ch])]
        pools = {ch: rnd.sample(v, len(v)) for ch, v in table.items()}
        ct = [pools[ch].pop() for ch in pt]
        sc, txt = attack(ct, False, RESTARTS, ITERS, f'control {c}: {pt}', seed0=1000*c)
        acc = sum(a == b for a, b in zip(txt, pt)) / 52; hits += acc > 0.9
        print(f'  plaintext {pt}\n  recovered {txt}  accuracy {acc:.2f}  true score {lm.score([pt])/52:.3f}/letter')
    print(f'controls recovered (>90% letters): {hits}/{n}')
    sys.exit()

inv = inverse(SEQ)
for label, seq in (('homophonic reading, sequence order', SEQ), ('transposition-key reading, inverse permutation', inv)):
    for segs in (False, True) if seq is SEQ else (False,):
        attack(seq, segs, RESTARTS, ITERS, f'{label}, alphabet a..z{" , zero groups as word breaks" if segs else ""}')
        attack([53 - v for v in seq], segs, RESTARTS, ITERS, f'{label}, alphabet z..a{" , zero groups as word breaks" if segs else ""}')
