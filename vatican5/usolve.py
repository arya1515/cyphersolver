"""usolve.py -- unit-level substitution solver (stage 2 after the EM segmentation in segem.py).

Each cipher unit type (a digit or digit pair, dotted variants separate when frequent) is mapped to one
plaintext element: a letter, a polyphonic pair of letters (either one, chosen greedily by the LM), a
consonant-vowel syllable, che/chi/qua/que/qui/gn-, or a short nomenclature word. Objective: no-space 5-gram
LM log-probability of the decoded text plus LAMBDA per output letter (LAMBDA = mean held-out cost, so the
length of the output is not penalised a priori). Simulated annealing over the mapping.

usage: python usolve.py <seed> [iters=60000] [--runs syn.json] [--truth syn_key.json] [--maxl 2]
outputs: us_<tag>_<seed>.json (mapping, score, decode)
"""
import sys, json, math, random, collections, pathlib, time
import segem, lmns
HERE = pathlib.Path(__file__).parent

def args_get(flag, default=None):
    if flag in sys.argv: return sys.argv[sys.argv.index(flag) + 1]
    return default

seed = int(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 1
iters = int(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else 60000
runs_file = args_get('--runs'); truth_file = args_get('--truth'); MAXL = int(args_get('--maxl', 2))
tag = pathlib.Path(runs_file).stem if runs_file else 'real'
rng = random.Random(seed)

lm = lmns.build()
LAMBDA = float(args_get('--lambda', 1.0))   # per-letter bonus; 1.0 < held-out cost 1.9 so predictable strings cannot be spammed
POLYPEN = float(args_get('--polypen', 0.7))  # charge per polyphonic token for the free choice (log 2 = 0.69)
KLW = float(args_get('--klw', 1.0))          # weight (nats per letter) of KL(decode letter freq || Italian letter freq)
runs = segem.load_runs(runs_file)
segs, tokens = segem.segment(runs, MAXL=MAXL, verbose=False)

# symbol ids: unit, or unit+'.' when the dotted variant is frequent enough to stand alone
dotcount = collections.Counter(u for t in tokens for u, d in t if d)
def sym(u, d): return u + '.' if (d and dotcount[u] >= 5) else u
stream = [[sym(u, d) for u, d in t] for t in tokens]
counts = collections.Counter(s for t in stream for s in t)
symbols = [s for s, _ in counts.most_common()]
print(f'{sum(counts.values())} tokens, {len(symbols)} symbol types; LAMBDA={LAMBDA:.3f} (held-out cost {lm.LAMBDA:.3f})')

# candidate plaintext elements
letters = list('abcdefgilmnopqrstuz')
cands = [(l,) for l in letters]
cands += [(a, b) for i, a in enumerate(letters) for b in letters[i+1:]]                 # polyphonic pairs
cands += [(c + v,) for c in 'bcdfglmnprstz' for v in 'aeiou']
cands += [('che',), ('chi',), ('qua',), ('que',), ('qui',), ('gna',), ('gne',), ('gni',), ('gno',)]
cands += [('et',), ('non',)]
single_idx = [i for i, c in enumerate(cands) if len(c) == 1 and len(c[0]) == 1]
syll_idx = [i for i, c in enumerate(cands) if len(c) == 1 and 2 <= len(c[0]) <= 3]
pair_idx = [i for i, c in enumerate(cands) if len(c) == 2]
word_idx = [i for i, c in enumerate(cands) if len(c) == 1 and len(c[0]) > 3]

ITAL = lm.uni
def kl_penalty(letter_counts):
    L = sum(letter_counts.values())
    if not L: return 0.0
    kl = 0.0
    for c, n in letter_counts.items():
        q = n / L; kl += q * math.log(q / ITAL.get(c, 1e-6))
    return KLW * L * kl

def decode(mapping):
    """Greedy decode; returns (score, text per segment)."""
    total = 0.0; out = []; hist = ''; lc = collections.Counter()
    for t in stream:
        piece = []
        for s in t:
            opts = cands[mapping[s]]
            if len(opts) == 1:
                w = opts[0]
            else:
                # polyphonic: pick the option the LM prefers given the history
                best = None; bw = None
                for w0 in opts:
                    v = lm.logp(hist, w0)
                    if best is None or v > best: best, bw = v, w0
                w = bw; total -= POLYPEN
            for ch in w:
                total += lm.logp(hist, ch) + LAMBDA
                hist = (hist + ch)[-4:]
            lc.update(w)
            piece.append(w)
        out.append(piece)
    return total - kl_penalty(lc), out

def random_mapping():
    m = {}
    for s in symbols:
        r = rng.random()
        m[s] = rng.choice(syll_idx if r < 0.55 else single_idx if r < 0.85 else pair_idx)
    return m

def propose(m):
    m2 = dict(m)
    if rng.random() < 0.65:
        s = rng.choice(symbols)
        r = rng.random()
        pool = syll_idx if r < 0.5 else single_idx if r < 0.8 else pair_idx
        m2[s] = rng.choice(pool)
    else:
        a, b = rng.sample(symbols, 2)
        m2[a], m2[b] = m[b], m[a]
    return m2

def anneal(iters, T0=25.0, T1=0.3):
    m = random_mapping(); sc, _ = decode(m); best = (sc, dict(m))
    t0 = time.time()
    for it in range(iters):
        T = T0 * (T1 / T0) ** (it / iters)
        m2 = propose(m); sc2, _ = decode(m2)
        if sc2 >= sc or rng.random() < math.exp((sc2 - sc) / T):
            m, sc = m2, sc2
            if sc > best[0]: best = (sc, dict(m))
        if it % 5000 == 0:
            print(f'  it {it:6d} T {T:6.2f} score {sc:9.1f} best {best[0]:9.1f}  ({time.time()-t0:.0f}s)', flush=True)
    return best

def show(mapping, out, n=12):
    for i, piece in enumerate(out[:n]):
        print('  ' + ' '.join(f"{s}={'/'.join(cands[mapping[s]])}" for s in stream[i]))
        print('    -> ' + ''.join('|'.join(cands[mapping[s]]) if len(cands[mapping[s]]) > 1 else cands[mapping[s]][0] for s in stream[i]))

def fmt_key(mapping):
    return ' '.join(f"{s}={'/'.join(cands[mapping[s]])}" for s in symbols)

def evaluate_truth(mapping, truth_file):
    """Token accuracy against a synthetic key: fraction of cipher digits whose decoded element is right."""
    tr = json.load(open(truth_file)); key = tr['key']
    code_to_plain = {}
    for e, c in key.items(): code_to_plain.setdefault(c.lstrip('.'), set()).add(e)
    # expand groups to letters
    ok = 0; tot = 0
    for s in symbols:
        u = s.rstrip('.')
        truth = set()
        for e in code_to_plain.get(u, ()):
            truth.add(e)
            if len(e) <= 3 and e not in ('che', 'chi', 'non', 'qua', 'que', 'qui', 'et') and not (e[0] in 'cdlmnrst' and len(e) == 2 and e[1] in 'aeiou'):
                truth |= set(e)
        got = set(cands[mapping[s]])
        c = counts[s]; tot += c
        if got & truth: ok += c
    return ok / tot

best_sc, best_m = anneal(iters)
sc, out = decode(best_m)
print(f'\nseed {seed} best score {sc:.1f}  ({sc/sum(len(''.join(p)) for p in out):.3f} per letter)')
print('key:', fmt_key(best_m))
show(best_m, out)
res = {'seed': seed, 'score': sc, 'mapping': {s: cands[best_m[s]] for s in symbols}, 'counts': dict(counts),
       'decode': [' '.join('|'.join(cands[best_m[s]]) for s in t) for t in stream]}
if truth_file:
    acc = evaluate_truth(best_m, truth_file); res['accuracy'] = acc
    print(f'token accuracy vs truth: {acc:.3f}')
json.dump(res, open(HERE / f'us_{tag}_{seed}.json', 'w'), indent=0)
