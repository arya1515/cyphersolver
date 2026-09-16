"""alternatives.py -- how many English plaintexts fit Scorpion S1 and S5 under the homophonic rule?
The only hard constraint a homophonic cipher imposes is that positions carrying the SAME symbol carry the same
letter. This script fills each cipher with real English words under exactly that constraint (beam search over a
Gutenberg vocabulary with word-frequency scoring) and prints several alternative 'solutions', then scores them
with the same 5-gram letter model as claimed.py. usage: python alternatives.py [beam=3000]"""
import sys, math, re, glob, collections, pathlib, random
sys.stdout.reconfigure(encoding='utf-8')
BEAM = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
CORP = r'C:/Users/DANIEL~1.BOU/AppData/Local/Temp/claude/C--Users-Daniel-Bourdeau-cipher/bfb7c2bf-254a-4a86-b088-f16d86b54a8f/scratchpad/t50'
text = ''
for f in sorted(glob.glob(f'{CORP}/corp_en_*.txt')):
    raw = open(f, encoding='utf-8', errors='ignore').read()
    m = re.search(r'\*\*\* ?START OF.*?\*\*\*', raw); raw = raw[m.end():] if m else raw
    m = re.search(r'\*\*\* ?END OF', raw); raw = raw[:m.start()] if m else raw
    text += raw.lower() + ' '
words = re.sub(r'[^a-z]+', ' ', text).split()
wc = collections.Counter(w for w in words if 1 <= len(w) <= 12)
vocab = {w: c for w, c in wc.items() if c >= 4 and (len(w) > 1 or w in ('a', 'i'))}
VOCAB = int(sys.argv[2]) if len(sys.argv) > 2 else 4000
vocab = dict(sorted(vocab.items(), key=lambda kv: -kv[1])[:VOCAB])
tot = sum(vocab.values()); logp = {w: math.log(c / tot) for w, c in vocab.items()}
bg = collections.Counter(zip(words, words[1:]))
def bigram_bonus(a, b):
    c = bg.get((a, b), 0)
    return math.log(1 + c) * 0.5
by_len = collections.defaultdict(list)
for w in vocab: by_len[len(w)].append(w)
s1 = [s for l in open('s1.txt', encoding='utf-8') if l.strip() and not l.startswith('#') for s in l.split()]
s5 = [int(x) for l in open('s5.txt') if not l.startswith('#') for x in l.split()]
def fill(syms, beam=BEAM, nout=6, seed=0):
    n = len(syms); rng = random.Random(seed)
    # beam entries: (score, assignment dict (tuple of items), words tuple)
    beams = {0: [(0.0, (), ())]}
    for p in range(n):
        if p not in beams: continue
        cand = beams.pop(p)
        cand.sort(key=lambda x: -x[0]); cand = cand[:beam]
        for sc, asg_t, ws in cand:
            asg = dict(asg_t); last = ws[-1] if ws else None
            for L in range(1, min(12, n - p) + 1):
                for w in by_len[L]:
                    a2 = None; ok = True
                    for j, ch in enumerate(w):
                        s = syms[p + j]; cur = (a2 or asg).get(s)
                        if cur is None:
                            if a2 is None: a2 = dict(asg)
                            a2[s] = ch
                        elif cur != ch: ok = False; break
                    if not ok: continue
                    if a2 is None: a2 = asg
                    nsc = sc + logp[w] + (bigram_bonus(last, w) if last else 0) + rng.random() * 1e-6
                    beams.setdefault(p + L, []).append((nsc, tuple(sorted(a2.items())), ws + (w,)))
    finals = sorted(beams.get(n, []), key=lambda x: -x[0])
    out = []; seen = set()
    for sc, asg, ws in finals:
        pt = ''.join(ws)
        if pt in seen: continue
        seen.add(pt); out.append((sc, ws))
        if len(out) >= nout: break
    return out
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'copenhagen'))
argv = sys.argv; sys.argv = [sys.argv[0]]
import solve as cp
cp.CORPUS = pathlib.Path(CORP); lm = cp.build_lm('en')
for name, syms in [('S1', s1), ('S5', s5)]:
    print(f'== {name}: {len(syms)} symbols, {len(set(syms))} distinct, alternatives under the same-symbol-same-letter rule (beam {BEAM}):')
    for k, (sc, ws) in enumerate(fill(syms, seed=0)):
        pt = ''.join(ws)
        print(f'  #{k+1} word-score {sc:8.1f}  letter-LM {lm.score([pt])/len(pt):.3f} nats/letter')
        print('     ' + ' '.join(ws))
