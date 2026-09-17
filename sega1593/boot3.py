# Bootstrap alignment with the CNN as classifier. usage: boot3.py [holdout_line] [iters]
import json, sys, numpy as np, torch
from boot2 import plain_classes, align, CLASSES, NULL, CODE
import cnn
pre = 'lines/f188v'; boxes = json.load(open(f'{pre}_g2.json'))
HOLDS = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 and sys.argv[1] != '0' else []
HOLD = HOLDS[0] if HOLDS else 0
ITERS = int(sys.argv[2]) if len(sys.argv) > 2 else 4
lines = list(range(3, 23))
crops = {k: cnn.crops_for(pre, k, boxes[str(k)]) for k in lines}
meta = [(pre, k, j, b[2] - b[0], b[4]) for k in lines for j, b in enumerate(boxes[str(k)])]
X = np.concatenate([crops[k] for k in lines]); area = np.array([m[4] for m in meta])
idx = {(k, j): i for i, (_, k, j, _, _) in enumerate(meta)}
gold = json.load(open('gold_f188v.json'))
goldi = {idx[(int(k), int(j))]: CLASSES.index(c) for k, d in gold.items() for j, c in d.items()}
labels = {i: c for i, c in goldi.items() if meta[i][1] not in HOLDS}
P = plain_classes(open('f185_cipher_only.txt', encoding='utf-8').read())
lnull_small = np.log(0.9)
for it in range(ITERS):
    ii = np.array(sorted(labels)); yy = np.array([labels[i] for i in ii])
    net = cnn.train(X[ii], yy, epochs=40)
    pr = cnn.predict(net, X); pr = 0.97 * pr + 0.03 / cnn.NC
    lpr = np.log(pr)
    lnull = np.where(area < 130, lnull_small, np.log(np.maximum(pr[:, NULL] * 0.3, 0.003)))
    out, score = align(lpr, P, lnull)
    thr = 0.5 if it < 2 else 0.35
    new = {}
    for i, o in enumerate(out):
        if o is None: continue
        if o[0] == 'm' and pr[i, o[1]] > thr: new[i] = o[1]
        elif o[0] == 'n' and area[i] < 130: new[i] = NULL
    for i, c in goldi.items():
        if meta[i][1] not in HOLDS: new[i] = c
    for i in list(new):
        if meta[i][1] in HOLDS: del new[i]
    nm = sum(1 for o in out if o and o[0] == '2'); nn = sum(1 for o in out if o and o[0] == 'n')
    msg = f'iter {it} score {score:.0f} labelled {len(new)} merges {nm} nulls {nn}'
    if HOLD:
        hi = [i for i in goldi if meta[i][1] == HOLD]
        acc_clf = np.mean([pr[i].argmax() == goldi[i] for i in hi])
        al = {i: (o[1] if o and o[0] == 'm' else (NULL if o and o[0] == 'n' else -1)) for i, o in enumerate(out)}
        acc_al = np.mean([al.get(i, -1) == goldi[i] for i in hi])
        msg += f'  held-out {HOLD}: clf {acc_clf:.2f} align {acc_al:.2f}'
    print(msg, flush=True)
    labels = new
json.dump({'meta': meta, 'labels': {str(i): int(c) for i, c in labels.items()},
           'align': [(o[0], o[1]) if o else None for o in out]}, open(f'boot3_out{HOLD}.json', 'w'))
torch.save(net.state_dict(), f'cnn_boot3_{HOLD}.pt')
np.save(f'probs_boot3_{HOLD}.npy', pr)
names = CLASSES[:14] + ['.', '#']
cur = None; s = ''
for i, o in enumerate(out):
    k = meta[i][1]
    if k != cur:
        if cur is not None: print(cur, s)
        cur = k; s = ''
    s += ' ?' if o is None else (' ' + names[o[1]] if o[0] == 'm' else (' .' if o[0] == 'n' else ' [' + names[o[1][0]] + '+' + names[o[1][1]] + ']'))
print(cur, s)
