"""oracle.py -- achievable ceiling of the unit-level attack on a synthetic: score of (a) the true plaintext
and (b) the best fixed mapping from the EM unit types to strings (majority ideal output per type), under
the usolve objective. Tells search failure apart from a segmentation/model ceiling.
usage: python oracle.py syn_k2_1.json syn_k2_1_key.json [lambda=1.0] [klw=1.0]
"""
import sys, json, math, collections
import segem, lmns
from lmns import normalize_cipher_orthography
runs = json.load(open(sys.argv[1])); tr = json.load(open(sys.argv[2])); key = tr['key']
LAMBDA = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; KLW = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
lm = lmns.build()
GROUPS = ['bc', 'lp', 'nm', 'rt', 'dfg', 'sz']
l2g = {ch: g for g in GROUPS for ch in g}
kfull = dict(key)
for ch, g in l2g.items(): kfull[ch] = key[g]
elems = set(kfull)
# re-encode the plaintext to get (element, code) per unit in order
pairs = []
for w in tr['plain'].split():
    i = 0
    while i < len(w):
        for L in (13, 9, 7, 3, 2, 1):
            piece = w[i:i+L]
            if piece in elems:
                pairs.append((piece, kfull[piece].lstrip('.'))); i += L; break
        else: i += 1
assert [c for _, c in pairs] == tr['units'], 'unit sequence mismatch'
digits = [t[0] for t in runs[0]]
# per digit position: (unit index, offset)
pos_info = {}; i = 0; ui = 0
while i < len(digits):
    if digits[i] == '4': i += 1; continue
    e, c = pairs[ui]
    for k in range(len(c)): pos_info[i + k] = (ui, k)
    i += len(c); ui += 1
def ideal(span):
    """Ideal output string for a span of digit positions."""
    out = []; k = 0
    while k < len(span):
        ui, off = pos_info[span[k]]
        e, c = pairs[ui]
        if off == 0 and k + len(c) <= len(span) and all(pos_info[span[k + j]] == (ui, j) for j in range(len(c))):
            out.append(e); k += len(c)
        else:
            # partial: split a CV syllable into its letters, otherwise give the letter to the first digit
            if len(e) == 2 and e[1] in 'aeiou' and len(c) == 2: out.append(e[off])
            elif off == 0: out.append(e)
            k += 1
    return ''.join(out)
segs, tokens = segem.segment(runs, MAXL=2, verbose=False)
# align EM tokens to digit positions
votes = collections.defaultdict(collections.Counter); stream = []
i = 0
for seg, tk in zip(segs, tokens):
    while digits[i] == '4': i += 1
    row = []
    for u, d in tk:
        span = list(range(i, i + len(u))); votes[u][ideal(span)] += 1; row.append(u); i += len(u)
    stream.append(row)
    while i < len(digits) and digits[i] == '4': i += 1
oracle = {u: v.most_common(1)[0][0] for u, v in votes.items()}
consistency = sum(v.most_common(1)[0][1] for v in votes.values()) / sum(sum(v.values()) for v in votes.values())
print(f'EM unit types {len(oracle)}; majority-output consistency {consistency:.3f}')
print('oracle mapping:', ' '.join(f'{u}={oracle[u] or "-"}' for u, _ in sorted(votes.items(), key=lambda kv: -sum(kv[1].values()))))
def objective(text_pieces):
    total = 0.0; hist = ''; lc = collections.Counter()
    for w in text_pieces:
        for ch in w:
            total += lm.logp(hist, ch) + LAMBDA; hist = (hist + ch)[-4:]
        lc.update(w)
    L = sum(lc.values()); kl = sum(n/L * math.log((n/L) / lm.uni.get(c, 1e-6)) for c, n in lc.items())
    return total - KLW * L * kl, L
truth_text = normalize_cipher_orthography(tr['plain'])
s_truth, L1 = objective([truth_text]); s_oracle, L2 = objective([oracle[u] for row in stream for u in row])
print(f'true plaintext: score {s_truth:.1f} over {L1} letters ({s_truth/L1:.3f}/letter)')
print(f'oracle mapping on EM units: score {s_oracle:.1f} over {L2} letters ({s_oracle/L2:.3f}/letter)')
