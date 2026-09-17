# Bootstrap a glyph classifier from f.188v (cipher) <-> f.185 (decipherment).
# Boxes from seg2 ({prefix}_g2.json). Seed labels from line 3 (hand-read). DP alignment with moves:
# match, box-as-null, letter-deletion, box-as-two-letters (merge). Iterate kNN retraining.
import json, re, sys, numpy as np
from PIL import Image
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
PAIRS = ['an', 'bo', 'cp', 'dq', 'er', 'fs', 'gt', 'hu', 'ix', 'ly', 'mz']
CODES = ['que', 'qui', 'pour']
CLASSES = PAIRS + CODES + ['null', 'code']   # 16 classes
NULL = CLASSES.index('null'); CODE = CLASSES.index('code')
NC = len(CLASSES)
H, W = 32, 24

def feats_for(pre, lines, boxes_all):
    X = []; meta = []
    for k in lines:
        im = Image.open(f'{pre}_l{k:02d}.png').convert('L'); a = np.asarray(im).astype(np.float32) / 255.0
        h, w = a.shape
        for j, (x0, y0, x1, y1, area) in enumerate(boxes_all[str(k)]):
            bw = x1 - x0; cw = max(bw, int(h * W / H))
            cx = (x0 + x1) // 2; xa = cx - cw // 2; xb = xa + cw
            crop = np.ones((h, cw), np.float32)
            sa, sb = max(0, xa), min(w, xb)
            crop[:, sa - xa:sa - xa + (sb - sa)] = a[:, sa:sb]
            img = Image.fromarray((crop * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
            v = 1.0 - np.asarray(img).astype(np.float32) / 255.0
            X.append(np.concatenate([v.ravel(), [bw / h * 3, area / (h * h) * 10]]))
            meta.append((pre, k, j, bw, area))
    return np.array(X), meta

def plain_classes(text):
    text = text.lower()
    text = re.sub(r'[àâä]', 'a', text); text = re.sub(r'[éèêë]', 'e', text); text = re.sub(r'[îï]', 'i', text)
    text = re.sub(r'[ôö]', 'o', text); text = re.sub(r'[ùûü]', 'u', text); text = text.replace('ç', 'c')
    out = []
    for w in re.findall(r'[a-z#]+', text):
        if w == '#': out.append(CODE); continue
        i = 0
        while i < len(w):
            hit = None
            for c in ('pour', 'que', 'qui'):
                if w.startswith(c, i): hit = c; break
            if hit: out.append(CLASSES.index(hit)); i += len(hit); continue
            ch = w[i]; i += 1
            ch = {'j': 'i', 'v': 'u', 'k': 'c', 'w': 'u'}.get(ch, ch)
            if ch == '#': out.append(CODE); continue
            for p, pr in enumerate(PAIRS):
                if ch in pr: out.append(p); break
    return out

def align(lpr, P, lnull, merge_pen=np.log(0.05), del_pen=np.log(0.01)):
    # lpr: (n, NC) log probs for boxes; P: plaintext class list; lnull: (n,) log prob of box being null
    n, m = len(lpr), len(P); NEG = -1e18
    D = np.full((n + 1, m + 1), NEG); B = np.zeros((n + 1, m + 1), np.int8); D[0, 0] = 0
    for t in range(n + 1):
        for p in range(m + 1):
            if t == 0 and p == 0: continue
            best, bb = NEG, 0
            if t > 0 and p > 0:
                v = D[t - 1, p - 1] + lpr[t - 1, P[p - 1]]
                if v > best: best, bb = v, 1
            if t > 0:
                v = D[t - 1, p] + lnull[t - 1]
                if v > best: best, bb = v, 2
            if p > 0:
                v = D[t, p - 1] + del_pen
                if v > best: best, bb = v, 3
            if t > 0 and p > 1:
                v = D[t - 1, p - 2] + merge_pen + 0.5 * (lpr[t - 1, P[p - 1]] + lpr[t - 1, P[p - 2]])
                if v > best: best, bb = v, 4
            D[t, p] = best; B[t, p] = bb
    t, p = n, m; out = [None] * n
    while t > 0 or p > 0:
        b = B[t, p]
        if b == 1: out[t - 1] = ('m', P[p - 1]); t -= 1; p -= 1
        elif b == 2: out[t - 1] = ('n', NULL); t -= 1
        elif b == 3: p -= 1
        else: out[t - 1] = ('2', (P[p - 2], P[p - 1])); t -= 1; p -= 2
    return out, D[n, m]

class Clf:
    def __init__(self, X):
        self.pca = PCA(n_components=40, random_state=0).fit(X)
    def fit(self, X, y):
        self.knn = KNeighborsClassifier(n_neighbors=7, weights='distance').fit(self.pca.transform(X), y)
        return self
    def proba(self, X):
        pr = np.full((len(X), NC), 0.01)
        p = self.knn.predict_proba(self.pca.transform(X))
        pr[:, self.knn.classes_] += p
        return pr / pr.sum(1, keepdims=True)

if __name__ == '__main__':
    pre = 'lines/f188v'; boxes = json.load(open(f'{pre}_g2.json'))
    lines = list(range(3, 23))
    X, meta = feats_for(pre, lines, boxes)
    idx = {(k, j): i for i, (_, k, j, _, _) in enumerate(meta)}
    seed = {3: {3: 'hu', 5: 'bo', 6: 'cp', 7: 'bo', 9: 'er', 10: 'an', 11: 'ly', 12: 'an', 15: 'er', 19: 'ly', 20: 'er', 21: 'fs',
                22: 'er', 23: 'fs', 24: 'cp', 25: 'an', 29: 'bo', 31: 'er', 32: 'an', 33: 'ly', 34: 'an', 35: 'cp', 36: 'er',
                37: 'bo', 38: 'cp', 39: 'bo', 40: 'fs', 43: 'bo', 44: 'an', 45: 'qui', 46: 'ly', 47: 'mz', 48: 'bo', 49: 'an',
                50: 'gt', 51: 'fs', 52: 'an', 55: 'dq', 56: 'er', 2: 'null', 13: 'null', 27: 'null'}}
    seed[4] = {0: 'pour', 1: 'er', 2: 'fs', 3: 'gt', 4: 'er', 6: 'er', 7: 'bo', 8: 'ly', 9: 'an', 10: 'er', 11: 'fs', 12: 'gt', 13: 'bo',
               14: 'ix', 15: 'gt', 16: 'que', 17: 'pour', 18: 'gt', 19: 'er', 20: 'bo', 21: 'mz', 22: 'cp', 23: 'er', 24: 'er', 25: 'gt',
               26: 'an', 27: 'an', 28: 'gt', 29: 'que', 30: 'cp', 31: 'er', 32: 'ly', 33: 'an', 34: 'an', 35: 'fs', 36: 'an', 37: 'ix',
               38: 'gt', 39: 'cp', 40: 'an', 41: 'fs', 42: 'fs', 43: 'er', 44: 'er', 45: 'bo', 46: 'hu', 47: 'ly', 49: 'er', 50: 'an',
               51: 'ly', 52: 'an', 53: 'gt', 54: 'er', 55: 'er', 56: 'fs', 57: 'hu', 58: 'er', 59: 'an', 60: 'bo', 61: 'an', 62: 'bo'}
    HOLD = int(sys.argv[1]) if len(sys.argv) > 1 else 0   # hold out this seed line for evaluation
    gold = {idx[(k, j)]: CLASSES.index(c) for k, d in seed.items() for j, c in d.items()}
    labels = {i: c for i, c in gold.items() if meta[i][1] != HOLD}
    SEEDLINES = [k for k in seed if k != HOLD]
    text = open('f185_cipher_only.txt', encoding='utf-8').read()
    P = plain_classes(text); print('plain classes', len(P), 'boxes', len(X))
    clf = Clf(X)
    area = np.array([m[4] for m in meta]); bw = np.array([m[3] for m in meta])
    for it in range(10):
        ii = np.array(sorted(labels)); yy = np.array([labels[i] for i in ii])
        pr = clf.fit(X[ii], yy).proba(X)
        lpr = np.log(pr)
        lnull = np.where(area < 130, np.log(0.9), np.log(0.004))
        out, score = align(lpr, P, lnull)
        new = {}
        for i, o in enumerate(out):
            if o is None: continue
            if o[0] == 'm' and (pr[i, o[1]] > (0.3 if it < 5 else 0.2) or i in labels): new[i] = o[1]
            elif o[0] == 'n' and area[i] < 130: new[i] = NULL
        for i, c in labels.items():
            if meta[i][1] in SEEDLINES: new[i] = c   # keep seed
        agree = np.mean([new.get(i, -1) == c for i, c in gold.items() if meta[i][1] in SEEDLINES])
        if HOLD:
            hi = [i for i in gold if meta[i][1] == HOLD]
            acc_clf = np.mean([pr[i].argmax() == gold[i] for i in hi])
            al = {i: (o[1] if o and o[0] == 'm' else -1) for i, o in enumerate(out)}
            acc_al = np.mean([al.get(i, -1) == gold[i] for i in hi])
            print(f'   held-out line {HOLD}: classifier acc {acc_clf:.2f}  alignment acc {acc_al:.2f}')
        nm = sum(1 for o in out if o and o[0] == '2'); nn = sum(1 for o in out if o and o[0] == 'n')
        print(f'iter {it} score {score:.0f} labelled {len(new)} merges {nm} nulls {nn} seed-agreement {agree:.2f}', flush=True)
        labels = new
    json.dump({'meta': meta, 'labels': {str(i): int(c) for i, c in labels.items()},
               'align': [(o[0], o[1]) if o else None for o in out]}, open('boot2_out.json', 'w'))
    np.save('boot2_X.npy', X)
    # print alignment per line
    names = PAIRS + CODES + ['.', '#']
    cur = None; s = ''
    for i, o in enumerate(out):
        k = meta[i][1]
        if k != cur:
            if cur is not None: print(cur, s)
            cur = k; s = ''
        if o is None: s += ' ?'
        elif o[0] == 'm': s += ' ' + names[o[1]]
        elif o[0] == 'n': s += ' .'
        else: s += ' [' + names[o[1][0]] + '+' + names[o[1][1]] + ']'
    print(cur, s)
