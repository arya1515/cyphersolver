# Self-training: add confident pseudo-labels from unlabelled pages (f176, f189, f186v), retrain, test on gold lines 3-4.
import json, numpy as np, torch, cnn
B = json.load(open('boot3_out0.json')); meta = B['meta']; labels = {int(i): c for i, c in B['labels'].items()}
gold = json.load(open('gold_f188v.json')); boxes = json.load(open('lines/f188v_g2.json'))
CL = cnn.CLASSES
crops = {k: cnn.crops_for('lines/f188v', k, boxes[str(k)]) for k in range(3, 23)}
Xtr, ytr, Xte, yte = [], [], [], []
for i, (pre, k, j, bw, area) in enumerate(meta):
    if k in (3, 4):
        g = gold[str(k)].get(str(j))
        if g is not None: Xte.append(crops[k][j]); yte.append(CL.index(g))
    elif i in labels: Xtr.append(crops[k][j]); ytr.append(labels[i])
Xtr = np.array(Xtr); ytr = np.array(ytr); Xte = np.array(Xte); yte = np.array(yte)
U = []
for pre, n in (('lines/f176', 45), ('lines/f189', 33), ('lines/f186v', 33)):
    bx = json.load(open(f'{pre}_g2.json'))
    for k in range(1, n + 1):
        c = cnn.crops_for(pre, k, bx[str(k)]); ar = np.array([b[4] for b in bx[str(k)]])
        U.append(c[ar >= 130])
U = np.concatenate(U); print('unlabelled', len(U))
torch.manual_seed(0)
net = cnn.train(Xtr, ytr, epochs=80)
p = cnn.predict(net, Xte); print(f'base: top1 {(p.argmax(1)==yte).mean():.3f}', flush=True)
Xc, yc = Xtr, ytr
for rnd in range(3):
    pu = cnn.predict(net, U); conf = pu.max(1); sel = conf > (0.9 if rnd == 0 else 0.85)
    Xc = np.concatenate([Xtr, U[sel]]); yc = np.concatenate([ytr, pu[sel].argmax(1)])
    print(f'round {rnd}: pseudo {sel.sum()} classes {np.bincount(pu[sel].argmax(1), minlength=16)}', flush=True)
    net = cnn.train(Xc, yc, epochs=60)
    p = cnn.predict(net, Xte)
    print(f'round {rnd}: top1 {(p.argmax(1)==yte).mean():.3f} top2 {np.mean([yte[i] in np.argsort(-p[i])[:2] for i in range(len(yte))]):.3f}', flush=True)
torch.save(net.state_dict(), 'cnn_self.pt')
