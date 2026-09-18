"""For each 4-letter code group in a telegram, list one-letter variants ranked by bigram fit with neighbours."""
import sys, json, math
sys.path.insert(0, '.'); sys.path.insert(0, '..')
from show17 import T
from family import code2ch
lm = json.load(open('../lm_zh.json', encoding='utf-8')); uni, bi = lm['uni'], lm['bi']; tot = sum(uni.values())
def lpu(c): return math.log((uni.get(c, 0) + 0.5) / tot)
def lpb(a, b): return math.log(0.8 * bi.get(a+b, 0) / (uni.get(a, 0) + 1) + 0.2 * math.exp(lpu(b)))
C, V = 'klmnpqrstvxyzbcdfghj', 'aeiou'
def ch(g):
    a, b = g[:2], g[2:]
    return code2ch.get('%02d%02d' % (T[a], T[b])) if a in T and b in T else None
def variants(g):
    for i in range(4):
        for x in (C if i % 2 == 0 else V):
            if x != g[i]: yield g[:i] + x + g[i+1:]
def run(s, which, top=8):
    gs = [s[i:i+4] for i in range(0, len(s) - 3, 4)]
    chars = [ch(g) or '□' for g in gs]
    print(''.join(chars))
    for k in which:
        L = chars[k-1] if k else None; R = chars[k+1] if k + 1 < len(chars) else None
        res = []
        for v in [gs[k]] + list(variants(gs[k])):
            c = ch(v)
            if not c: continue
            sc = (lpb(L, c) if L else lpu(c)) + (lpb(c, R) if R else 0)
            res.append((sc, v, c))
        res.sort(reverse=True)
        print(k, gs[k], chars[k], ' '.join('%s%s%.0f' % (v, c, sc) for sc, v, c in res[:top]))
if __name__ == '__main__':
    run(sys.argv[1], [int(x) for x in sys.argv[2].split(',')])
