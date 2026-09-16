"""French letter 5-gram model (interpolated, add-5 smoothing), built from ../sp53/corpus_fr.txt (a-z, no spaces)."""
import numpy as np, os, re
A = 26
def build(path='../sp53/corpus_fr.txt', out='ng5_fr.npy'):
    text = re.sub(r'[^a-z]', '', open(path, encoding='utf-8').read())
    idx = np.frombuffer(text.encode(), dtype=np.uint8).astype(np.int64) - 97
    n = len(idx)
    c5 = np.bincount(idx[:-4]*A**4+idx[1:-3]*A**3+idx[2:-2]*A**2+idx[3:-1]*A+idx[4:], minlength=A**5).astype(np.float32)
    c4 = np.bincount(idx[:-3]*A**3+idx[1:-2]*A**2+idx[2:-1]*A+idx[3:], minlength=A**4).astype(np.float32)
    c3 = np.bincount(idx[:-2]*A**2+idx[1:-1]*A+idx[2:], minlength=A**3).astype(np.float32)
    c2 = np.bincount(idx[:-1]*A+idx[1:], minlength=A**2).astype(np.float32)
    ctx4 = c5.reshape(A**4, A).sum(1); ctx3 = c4.reshape(A**3, A).sum(1); ctx2 = c3.reshape(A**2, A).sum(1); ctx1 = c2.reshape(A, A).sum(1)
    p1 = (np.bincount(idx, minlength=A)+1)/(n+A)
    p2 = (c2.reshape(A, A)+5*p1[None, :])/(ctx1[:, None]+5)
    p3 = (c3.reshape(A**2, A)+5*np.tile(p2, (A, 1)))/(ctx2[:, None]+5)
    p4 = (c4.reshape(A**3, A)+5*np.tile(p3, (A, 1)))/(ctx3[:, None]+5)
    p5 = (c5.reshape(A**4, A)+5*np.tile(p4, (A, 1)))/(ctx4[:, None]+5)
    lp = np.log(p5).astype(np.float32).reshape(-1)
    np.save(out, lp); print('corpus letters', n); return lp
def load(path='ng5_fr.npy'):
    return np.load(path) if os.path.exists(path) else build()
def enc(s): return np.frombuffer(s.encode(), dtype=np.uint8).astype(np.int64)-97
def score(tab, p):
    if len(p) < 5: return 0.0
    q = p[:-4]*A**4+p[1:-3]*A**3+p[2:-2]*A**2+p[3:-1]*A+p[4:]
    return float(tab[q].sum())
if __name__ == '__main__':
    tab = build()
    for t in ['ilnyaaucunsubietdescrupuledemanqueradieu', 'lesreiglesdeperfectionprenezsdulement', 'xqzzkpqlmmnarteeoo', 'etmesureracelasilestmeilleurdagir']:
        print(round(score(tab, enc(t))/(len(t)-4), 3), t)
