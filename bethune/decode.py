"""Viterbi decoder: cipher tokens -> French letters, using P(unit|token) from em_model.json and a character n-gram LM
trained on the Xivrey volumes of Henri IV's letters (u/v -> u, i/j -> i, accents stripped, letters only).
usage: python decode.py ct_file [--lm N] [--beam B]"""
import sys, json, math, re, collections, unicodedata, glob
sys.stdout.reconfigure(encoding='utf-8')
N = 5
BEAM = 400
def norm(s):
    s = unicodedata.normalize('NFKD', s.lower()); s = ''.join(c for c in s if not unicodedata.combining(c))
    s = s.replace('j','i').replace('v','u').replace('œ','oe').replace('æ','ae')
    return re.sub(r'[^a-z]', '', s)
def train_lm(paths):
    counts = [collections.Counter() for _ in range(N+1)]
    for p in paths:
        txt = open(p, encoding='utf-8', errors='ignore').read()
        # keep only lowercase-ish letter runs; join words (cipher has no spaces)
        txt = norm(txt)
        for k in range(1, N+1):
            for i in range(len(txt)-k+1): counts[k][txt[i:i+k]] += 1
    return counts
class LM:
    def __init__(self, counts):
        self.c = counts; self.V = 22; self.tot1 = sum(counts[1].values())
    def logp(self, hist, ch):
        # interpolated absolute-discount backoff (simple Kneser-Ney-ish)
        p = (self.c[1][ch] + 1) / (self.tot1 + self.V)
        for k in range(2, N+1):
            h = hist[-(k-1):] if len(hist) >= k-1 else None
            if h is None or len(h) < k-1: break
            ctx = self.c[k-1][h]
            if ctx == 0: break
            n = self.c[k][h+ch]
            d = 0.75
            lam = d * len([1 for x in 'abcdefghilmnopqrstuxyz' if self.c[k][h+x] > 0]) / ctx
            p = max(n - d, 0) / ctx + lam * p
        return math.log(max(p,1e-12))
def load_model(path='bethune/em_model.json'):
    m = json.load(open(path, encoding='utf-8'))
    out = {}
    for tok, d in m.items():
        out[tok] = {(u if u != '-' else ''): p for u, p in d.items()}
    return out
def decode(tokens, model, lm, fixed):
    # state: last N-1 chars of output; score
    beams = {'': (0.0, [])}
    for tok in tokens:
        cands = fixed.get(tok) or model.get(tok)
        if cands is None:
            if any(ch.isdigit() for ch in tok): cands = {f'[{tok}]': 1.0}
            else: cands = {ch: 1/22 for ch in 'abcdefghilmnopqrstuxyz'}; cands['?'] = 0.0
        newb = {}
        for hist, (sc, out) in beams.items():
            for u, p in cands.items():
                if p < 0.02 and len(cands) < 20: continue
                if p <= 0.0: continue
                s = sc + math.log(max(p,1e-9))
                h = hist
                if u.startswith('['):           # unknown token, keep as is, reset context lightly
                    s += -6.0; h = ''
                else:
                    for ch in u:
                        s += lm.logp(h, ch); h = (h + ch)[-(N-1):]
                key = h
                if key not in newb or newb[key][0] < s: newb[key] = (s, out + [u if u else '_'])
        beams = dict(sorted(newb.items(), key=lambda kv: -kv[1][0])[:BEAM])
    best = max(beams.values(), key=lambda v: v[0])
    return best
def load_vocab(paths):
    cnt = collections.Counter()
    for p in paths:
        for w in re.findall(r"[A-Za-zÀ-ÿ']+", open(p, encoding='utf-8', errors='ignore').read()):
            w2 = norm(w)
            if 1 <= len(w2) <= 16: cnt[w2] += 1
    return cnt
def segment(s, vocab, total):
    # DP: maximise sum log P(word); unknown chunks of length L cost heavily
    n = len(s); best = [(-1e18, 0)] * (n+1); best[0] = (0.0, 0)
    for i in range(1, n+1):
        for j in range(max(0, i-16), i):
            w = s[j:i]
            if best[j][0] < -1e17: continue
            if w in vocab: sc = best[j][0] + math.log(vocab[w] / total)
            elif len(w) == 1: sc = best[j][0] - 12.0
            else: continue
            if sc > best[i][0]: best[i] = (sc, j)
    out = []; i = n
    while i > 0:
        j = best[i][1]; out.append(s[j:i]); i = j
    return ' '.join(out[::-1])
def main():
    ctf = sys.argv[1]
    model = load_model()
    fixed = {'48': {'cardinal': 1.0}, '17': {'aldobrandin': 1.0}, 'f,': {'le': 1.0}, 'x,': {'que': 1.0}, 'r,': {'par': 1.0},
             'g,': {'la': 1.0}, '61': {'qui': 1.0}, '63': {'re': 1.0}, 'x:': {'et': 1.0}, 'x^': {'et': 1.0}, 'd,': {'ie': 1.0}, 'DL,': {'ie': 1.0}, '65': {'si': 1.0}}
    lm = LM(train_lm(glob.glob('bethune/xivrey/*.txt')))
    vocab = load_vocab(glob.glob('bethune/xivrey/*.txt')); total = sum(vocab.values())
    lines = [l for l in open(ctf, encoding='utf-8') if l.strip() and not l.startswith('#')]
    for l in lines:
        parts=[x.strip() for x in l.split('|')]
        lab, ct = parts[0], (parts[2] if len(parts)>=4 else parts[1])
        toks = ct.replace('s: 4 8', 's: 48').split()
        sc, out = decode(toks, model, lm, fixed)
        print(f'{lab} {sc:8.1f} | ' + ' '.join(out))
        flat = ''.join(u if not u.startswith('[') else ' '+u+' ' for u in out).replace('_','')
        segs = [segment(part, vocab, total) if not part.startswith('[') else part for part in re.split(r'\s+', flat) if part]
        print(' ' * 15 + '| ' + ' '.join(segs))
if __name__ == '__main__':
    main()
