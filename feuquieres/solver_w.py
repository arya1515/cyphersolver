# Variant of solver.py whose objective is a word-segmentation likelihood instead of a letter n-gram score:
# the rendered letter string is segmented by Viterbi into dictionary words (unigram log-probabilities from the
# period corpus plus the Veillane vocabulary), with a heavy per-letter penalty for stretches that are not words.
# Real French segments into words almost entirely; the fluent nonsense the n-gram objective produced does not.
# usage: python -X utf8 -u solver_w.py ciphertext.txt [iters] [seed]
import re, random, math, sys, os, collections, time
sys.argv, _argv = ['x'], sys.argv
import solver as S
from solver import norm, parse, inventory, unit_prior, NULL, split_word, CONS, VOW

OOV = float(os.environ.get('OOV', '7.0'))       # penalty per letter not covered by a dictionary word
NULLPEN = float(os.environ.get('NULLPEN', '3.0'))
PRIORW = float(os.environ.get('PRIORW', '0.3'))
CRIBW = float(os.environ.get('CRIBW', '0.0'))
MAXW = 14

def build_dict():
    txt = open(os.path.join(S.CH, 'corpus_fr.txt'), encoding='utf-8').read()
    cnt = collections.Counter(w for w in txt.split() if w.isalpha())
    extra = [norm(w) for w in S.DOMAIN + S.PERIOD]
    for w in extra:
        if w.isalpha():
            cnt[w] = max(cnt[w], 30)
    # single letters are not words except a, y, o (keep them rare)
    for ch in 'abcdefghijklmnopqrstuvxyz':
        if ch not in ('a', 'y', 'o'):
            cnt.pop(ch, None)
    tot = sum(cnt.values())
    return {w: math.log(c / tot) for w, c in cnt.items() if c >= 2}

DICT = build_dict()

def seg_score(t):
    n = len(t)
    best = [0.0] + [-1e18] * n
    for i in range(1, n + 1):
        b = best[i-1] - OOV                     # letter i-1 left uncovered
        lo = max(0, i - MAXW)
        for j in range(lo, i - 1):              # words of length >= 2
            w = t[j:i]
            lp = DICT.get(w)
            if lp is not None:
                v = best[j] + lp
                if v > b: b = v
        if t[i-1] in 'ayo':
            v = best[i-1] + DICT.get(t[i-1], -12.0)
            if v > b: b = v
        best[i] = b
    return best[n]

class WSolver(S.Solver):
    def total(self, m=None):
        m = m or self.map
        t = self.render(m)
        s = seg_score(t)
        s -= NULLPEN * sum(1 for c in self.codes if m[c] == NULL)
        s += PRIORW * sum(self.logpri[m[c]] for c in self.codes)
        if CRIBW:
            s += CRIBW * sum(len(w) * min(t.count(w), 2) for w in self.cribs)
        return s

if __name__ == '__main__':
    path = _argv[1]; iters = int(_argv[2]) if len(_argv) > 2 else 100000; seed = int(_argv[3]) if len(_argv) > 3 else 1
    random.seed(seed)
    toks = parse(path); low, high = inventory(); pri = unit_prior(set(low + high))
    s = WSolver(toks, low, high, pri)
    best = s.anneal(iters, T0=20.0, T1=0.5, log=10000)
    print('BEST', round(best, 1)); print(s.render_pretty()); print(s.render()); print('MAP', sorted(s.map.items()))
