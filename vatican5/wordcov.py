"""Dictionary coverage of a decoded text: fraction of chars covered by dictionary words (len>=minlen, top-N words),
via max-coverage DP. usage: wordcov.py file [minlen] [topN]"""
import json, sys, re
words = json.load(open('it_words.json', encoding='utf8'))
minlen = int(sys.argv[2]) if len(sys.argv) > 2 else 4
topn = int(sys.argv[3]) if len(sys.argv) > 3 else 8000
D = set(w for w, c in words[:topn] if len(w) >= minlen)
MAXW = max(len(w) for w in D)
def cov(s):
    n = len(s); best = [0] * (n + 1)
    for i in range(1, n + 1):
        best[i] = best[i-1]
        for L in range(minlen, min(MAXW, i) + 1):
            if s[i-L:i] in D and best[i-L] + L > best[i]: best[i] = best[i-L] + L
    return best[n] / max(1, n)
for f in sys.argv[1].split(','):
    txt = open(f, encoding='utf8', errors='replace').read()
    if 'PLAINTEXT:' in txt: txt = txt.split('PLAINTEXT:')[1]
    s = re.sub(r'[^a-z]', '', txt.lower())
    print(f'{f}: coverage={cov(s):.3f} (n={len(s)})')
