"""Independent route-transposition search on the Cox→Milroy telegram of 3 Dec 1862 (Milroy's copy, lesson-plan transcription).
Model (Stager): plaintext written row-wise into R lines x C columns; transmitted column by column, each column up or down,
columns in some order. Search all column orders/directions for C=6 and score with a word-bigram LM."""
import json, math, itertools, re
raw = """China quest whether transportation in reach what is if bully imboden by to forward Jrsisert also are Cumberland
hole that the will the him route confirmed your health information let you also morsefield supply roads with stine
at connection's for co your far try know w to fight as me shall hour road your and Kelley x Guusmat road country you of
communications avoid you drink to your direction extest Mountain Moonfield morning star answer from can - Winchester by being"""
words = [w for w in raw.split() if w != '-']
ind, ct = words[0], words[1:]
print(ind, len(ct), 'words')
lm = json.load(open('word_lm.json')); uni = lm['uni']; bi = lm['bi']
U = sum(uni.values())
def wscore(a, b):
    a, b = a.lower(), b.lower()
    if a + ' ' + b in bi: return math.log(bi[a + ' ' + b] / uni.get(a, 1))
    return math.log(uni.get(b, 0.5) / U) - 2.0
def score(seq):
    return sum(wscore(a, b) for a, b in zip(seq, seq[1:]))
def untranspose(block, R, C, order, dirs):
    grid = [[None] * C for _ in range(R)]
    k = 0
    for col, d in zip(order, dirs):
        rows = range(R) if d == 0 else range(R - 1, -1, -1)
        for r in rows:
            grid[r][col] = block[k]; k += 1
    return [grid[r][c] for r in range(R) for c in range(C)]
def search(block, R, C):
    best = []
    for order in itertools.permutations(range(C)):
        for dirs in itertools.product((0, 1), repeat=C):
            pt = untranspose(block, R, C, order, dirs)
            best.append((score(pt), order, dirs, pt))
    best.sort(key=lambda x: -x[0])
    return best[:5]
if __name__ == '__main__':
    for R, C, start in [(8, 6, 0), (8, 6, 48), (10, 8, 0), (16, 5, 0), (5, 16, 0)]:
        block = ct[start:start + R * C]
        if len(block) < R * C: 
            print(f'--- {R}x{C} from {start}: only {len(block)} words'); continue
        print(f'--- {R}x{C} from word {start}')
        for s, order, dirs, pt in search(block, R, C)[:2]:
            print(f'  {s:.1f} cols {order} dirs {dirs}\n    ' + ' '.join(pt))
