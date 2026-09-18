"""Leave-one-exemplar-out accuracy for a hand's labelled figure set.

Each exemplar is classified by its nearest neighbour among all the *other* exemplars and scored on
whether that neighbour carries the same letter. It uses every labelled figure as test data without
spending any of them, so it is far more stable than scoring a couple of held-out lines, and it
exposes suspect labels directly: an exemplar its own neighbours disagree with.

The figure is bounded above by how confusable this cipher's figures genuinely are (i/n/s and e/u sit
at 0.91-0.93 correlation), so it will not reach 100 % even with perfect labels. It is for comparing
states of the same set, not an absolute score.

    python loo.py exemplars/manifest_f143.json
"""
import sys, json, io
from collections import Counter, defaultdict
import numpy as np
_o = sys.stdout; sys.stdout = io.StringIO()
from checkex import vec
sys.stdout = _o

def loo(manifest, k=1, verbose=True):
    man = [m for m in json.load(open(manifest)) if len(m['letter']) == 1]
    V = np.array([vec(m['file']) for m in man]); L = [m['letter'] for m in man]
    S = V @ V.T; np.fill_diagonal(S, -9)
    right = 0; per = defaultdict(lambda: [0, 0]); suspects = []
    for i in range(len(man)):
        nn = np.argsort(-S[i])[:k]
        vote = Counter(L[j] for j in nn).most_common(1)[0][0]
        ok = vote == L[i]; right += ok
        per[L[i]][0] += ok; per[L[i]][1] += 1
        if not ok and S[i, nn[0]] > 0.95:
            suspects.append((round(float(S[i, nn[0]]), 3), man[i]['file'].split('/')[-1], L[i], L[nn[0]]))
    acc = 100 * right / len(man)
    if verbose:
        print(f'{manifest}: {len(man)} exemplars, {len(per)} letters')
        print(f'  leave-one-out nearest-neighbour accuracy: {right}/{len(man)} = {acc:.1f} %')
        print('  per letter:', '  '.join(f'{l}:{a}/{n}' for l, (a, n) in sorted(per.items())))
        if suspects:
            print(f'  {len(suspects)} near-duplicates (>0.95) carrying a different letter - suspect labels:')
            for s in sorted(suspects, reverse=True)[:10]: print('    ', s)
    return acc

if __name__ == '__main__':
    loo(sys.argv[1])
