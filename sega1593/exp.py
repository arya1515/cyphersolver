# Compare classifiers: train on alignment labels (lines != 3,4), test on gold lines 3,4.
import json, numpy as np, torch, torch.nn.functional as F
import cnn
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
B = json.load(open('boot3_out0.json')); meta = B['meta']; labels = {int(i): c for i, c in B['labels'].items()}
gold = json.load(open('gold_f188v.json')); boxes = json.load(open('lines/f188v_g2.json'))
CL = cnn.CLASSES
def build(H, W):
    cnn.H, cnn.W = H, W
    crops = {k: cnn.crops_for('lines/f188v', k, boxes[str(k)]) for k in range(3, 23)}
    Xtr, ytr, Xte, yte = [], [], [], []
    for i, (pre, k, j, bw, area) in enumerate(meta):
        if k in (3, 4):
            g = gold[str(k)].get(str(j))
            if g is not None: Xte.append(crops[k][j]); yte.append(CL.index(g))
        elif i in labels: Xtr.append(crops[k][j]); ytr.append(labels[i])
    return np.array(Xtr), np.array(ytr), np.array(Xte), np.array(yte)
Xtr, ytr, Xte, yte = build(40, 32)
print('train', len(Xtr), 'test', len(Xte))
# (a) PCA + SVM / kNN on raw pixels
flat = lambda X: X.reshape(len(X), -1)
for name, clf in [('pca50+svm', make_pipeline(PCA(50, random_state=0), StandardScaler(), SVC(C=5, gamma='scale'))),
                  ('pca50+knn5', make_pipeline(PCA(50, random_state=0), KNeighborsClassifier(5, weights='distance'))),
                  ('svm-raw', make_pipeline(StandardScaler(), SVC(C=5, gamma='scale')))]:
    clf.fit(flat(Xtr), ytr); acc = (clf.predict(flat(Xte)) == yte).mean(); print(f'{name}: {acc:.3f}', flush=True)
# (b) CNN variants
torch.manual_seed(0)
for epochs in (60, 150):
    net = cnn.train(Xtr, ytr, epochs=epochs)
    p = cnn.predict(net, Xte); print(f'cnn {epochs}ep: top1 {(p.argmax(1)==yte).mean():.3f} top2 {np.mean([yte[i] in np.argsort(-p[i])[:2] for i in range(len(yte))]):.3f}', flush=True)
# (c) bigger input
Xtr2, ytr2, Xte2, yte2 = build(56, 40)
cnn.Net.__init__.__defaults__  # noop
class Net2(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.c1 = torch.nn.Conv2d(1, 32, 3, padding=1); self.c2 = torch.nn.Conv2d(32, 64, 3, padding=1); self.c3 = torch.nn.Conv2d(64, 96, 3, padding=1)
        self.fc1 = torch.nn.Linear(96 * 7 * 5, 128); self.fc2 = torch.nn.Linear(128, cnn.NC); self.do = torch.nn.Dropout(0.3)
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.c1(x)), 2); x = F.max_pool2d(F.relu(self.c2(x)), 2); x = F.max_pool2d(F.relu(self.c3(x)), 2)
        return self.fc2(self.do(F.relu(self.fc1(x.flatten(1)))))
cnn.Net = Net2
net = cnn.train(Xtr2, ytr2, epochs=100)
p = cnn.predict(net, Xte2); print(f'cnn56x40 100ep: top1 {(p.argmax(1)==yte2).mean():.3f} top2 {np.mean([yte2[i] in np.argsort(-p[i])[:2] for i in range(len(yte2))]):.3f}')
