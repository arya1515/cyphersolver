# Small CNN glyph classifier on box crops. Train on aligned labels (boot2_out.json), evaluate on held-out gold lines.
# usage: cnn.py train [holdout lines csv]  |  cnn.py predict prefix line_from line_to out.json
import json, sys, numpy as np, torch, torch.nn as nn, torch.nn.functional as F
from PIL import Image
PAIRS = ['an', 'bo', 'cp', 'dq', 'er', 'fs', 'gt', 'hu', 'ix', 'ly', 'mz']
CLASSES = PAIRS + ['que', 'qui', 'pour', 'null', 'code']
NC = len(CLASSES); H, W = 40, 32
torch.manual_seed(0); np.random.seed(0)

def crops_for(pre, k, boxes):
    im = Image.open(f'{pre}_l{k:02d}.png').convert('L'); a = np.asarray(im).astype(np.float32) / 255.0
    h, w = a.shape; out = []
    for (x0, y0, x1, y1, area) in boxes:
        cw = max(x1 - x0 + 6, int(h * W / H))
        cx = (x0 + x1) // 2; xa = cx - cw // 2
        crop = np.ones((h, cw), np.float32)
        for x in range(cw):
            sx = xa + x
            if 0 <= sx < w and x0 - 3 <= sx < x1 + 3: crop[:, x] = a[:, sx]
        img = Image.fromarray((crop * 255).astype(np.uint8)).resize((W, H), Image.BILINEAR)
        out.append(1.0 - np.asarray(img).astype(np.float32) / 255.0)
    return np.array(out)

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.c1 = nn.Conv2d(1, 32, 3, padding=1); self.c2 = nn.Conv2d(32, 64, 3, padding=1); self.c3 = nn.Conv2d(64, 96, 3, padding=1)
        self.fc1 = nn.Linear(96 * 5 * 4, 128); self.fc2 = nn.Linear(128, NC); self.do = nn.Dropout(0.4)
    def forward(self, x):
        x = F.max_pool2d(F.relu(self.c1(x)), 2); x = F.max_pool2d(F.relu(self.c2(x)), 2); x = F.max_pool2d(F.relu(self.c3(x)), 2)
        x = x.flatten(1); x = self.do(F.relu(self.fc1(x))); return self.fc2(x)

def augment(xb):
    # random shift up to 2 px and scale jitter via affine grid
    n = xb.shape[0]
    theta = torch.zeros(n, 2, 3)
    s = 1 + (torch.rand(n) - 0.5) * 0.2
    theta[:, 0, 0] = s; theta[:, 1, 1] = s * (1 + (torch.rand(n) - 0.5) * 0.15)
    theta[:, 0, 2] = (torch.rand(n) - 0.5) * 0.15; theta[:, 1, 2] = (torch.rand(n) - 0.5) * 0.15
    grid = F.affine_grid(theta, xb.shape, align_corners=False)
    return F.grid_sample(xb, grid, align_corners=False, padding_mode='zeros')

def train(X, y, Xv=None, yv=None, epochs=60):
    net = Net(); opt = torch.optim.Adam(net.parameters(), 1e-3, weight_decay=1e-4)
    Xt = torch.tensor(X)[:, None]; yt = torch.tensor(y)
    cw = torch.tensor(1.0 / np.maximum(np.bincount(y, minlength=NC), 1), dtype=torch.float32); cw = cw / cw.mean()
    for ep in range(epochs):
        net.train(); perm = torch.randperm(len(Xt))
        for i in range(0, len(Xt), 64):
            idx = perm[i:i + 64]; xb = augment(Xt[idx]); loss = F.cross_entropy(net(xb), yt[idx], weight=cw ** 0.5)
            opt.zero_grad(); loss.backward(); opt.step()
        if Xv is not None and (ep % 10 == 9 or ep == epochs - 1):
            print(f'  ep {ep + 1} val acc {evaluate(net, Xv, yv):.3f}', flush=True)
    return net

def predict(net, X):
    net.eval()
    with torch.no_grad(): return F.softmax(net(torch.tensor(X)[:, None]), 1).numpy()

def evaluate(net, X, y):
    return float((predict(net, X).argmax(1) == y).mean())

if __name__ == '__main__':
    if sys.argv[1] == 'train':
        hold = [int(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 and sys.argv[2] else []
        B = json.load(open('boot2_out.json')); meta = B['meta']; labels = {int(i): c for i, c in B['labels'].items()}
        boxes = json.load(open('lines/f188v_g2.json'))
        gold = json.load(open('gold_f188v.json')) if __import__('os').path.exists('gold_f188v.json') else {}
        crops = {}
        for k in range(3, 23): crops[k] = crops_for('lines/f188v', k, boxes[str(k)])
        Xtr, ytr, Xv, yv = [], [], [], []
        for i, (pre, k, j, bw, area) in enumerate(meta):
            if k in hold:
                g = gold.get(str(k), {}).get(str(j))
                if g is not None: Xv.append(crops[k][j]); yv.append(CLASSES.index(g))
            elif i in labels: Xtr.append(crops[k][j]); ytr.append(labels[i])
        Xtr = np.array(Xtr); ytr = np.array(ytr); print('train', len(Xtr), 'val', len(Xv), np.bincount(ytr, minlength=NC))
        Xv = np.array(Xv) if Xv else None; yv = np.array(yv) if yv else None
        net = train(Xtr, ytr, Xv, yv)
        torch.save(net.state_dict(), 'cnn.pt')
        if Xv is not None:
            p = predict(net, Xv); top1 = (p.argmax(1) == yv).mean(); top2 = np.mean([yv[i] in np.argsort(-p[i])[:2] for i in range(len(yv))])
            print(f'held-out top1 {top1:.3f} top2 {top2:.3f}')
            from collections import Counter
            print('confusions', Counter((CLASSES[a], CLASSES[b]) for a, b in zip(yv, p.argmax(1)) if a != b).most_common(12))
    else:
        pre, k0, k1, outf = sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
        net = Net(); net.load_state_dict(torch.load('cnn.pt')); boxes = json.load(open(f'{pre}_g2.json'))
        out = {}
        for k in range(k0, k1 + 1):
            p = predict(net, crops_for(pre, k, boxes[str(k)]))
            out[str(k)] = p.tolist()
        json.dump(out, open(outf, 'w')); print('wrote', outf)
