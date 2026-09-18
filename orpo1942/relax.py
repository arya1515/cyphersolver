"""Continuous relaxation of the double Doppelkasten key search.
Boxes become doubly-stochastic matrices (Sinkhorn of logits / tau); both decryption passes are propagated in
mean-field over row/column marginals; loss = -sum log E[f(p)] (-> the unigram log-likelihood when the boxes are hard).
Many restarts are optimised in one batch on the GPU while tau anneals; each is hardened (Hungarian) and scored exactly.
Usage: python relax.py <cipherfile> [restarts] [steps] [left:0/1] [seed]"""
import sys, math, time
import numpy as np
import torch
from scipy.optimize import linear_sum_assignment
import dk

AL = dk.AL
dev = 'cuda' if torch.cuda.is_available() else 'cpu'


def load_pairs(fn):
    c1, c2 = [], []
    for l in open(fn):
        if l.startswith('#') or '\t' not in l: continue
        s = l.rstrip('\n').split('\t')[1].replace(' ', '').replace('.', 'X').replace('J', 'I')
        s = s[:len(s) // 2 * 2]
        for i in range(0, len(s), 2):
            c1.append(AL.index(s[i])); c2.append(AL.index(s[i + 1]))
    return torch.tensor(c1, device=dev), torch.tensor(c2, device=dev)


def unigram():
    import struct
    q = struct.unpack('25f', open('q1.bin', 'rb').read())
    f = np.array([10 ** v for v in q]); return f / f.sum()


def sinkhorn(L, it=25):
    L = L - L.logsumexp(-1, keepdim=True)
    for _ in range(it):
        L = L - L.logsumexp(-2, keepdim=True)
        L = L - L.logsumexp(-1, keepdim=True)
    return L.exp()


def rowcol(P):
    """P [..., 25] cell distribution -> row [...,5], col [...,5]"""
    Q = P.reshape(*P.shape[:-1], 5, 5)
    return Q.sum(-1), Q.sum(-2)


def step(rb, cb, ra, ca, PA, PB, dl):
    """one decryption pass in mean field.
    (rb,cb): row/col dist of first letter's cell in B; (ra,ca): of second letter's cell in A. shapes [R,n,5]
    returns letter distributions y1 (from A), y2 (from B): [R,n,25]"""
    same = rb * ra                                    # P(row = r for both)  [R,n,5]
    # y1 = A[rb][ca] if rows differ, A[ra][ca+dl] if same
    # distribution of (col + dl): P(newcol = c) = ca[c - dl]
    ca_s = torch.roll(ca, shifts=dl, dims=-1)
    cb_s = torch.roll(cb, shifts=dl, dims=-1)
    u = (rb - same).unsqueeze(-1) * ca.unsqueeze(-2) + same.unsqueeze(-1) * ca_s.unsqueeze(-2)   # [R,n,5,5] A-cell dist
    w = (ra - same).unsqueeze(-1) * cb.unsqueeze(-2) + same.unsqueeze(-1) * cb_s.unsqueeze(-2)   # B-cell dist
    u = u.reshape(*u.shape[:-2], 25); w = w.reshape(*w.shape[:-2], 25)
    # letter at cell: y(z) = sum_cell u(cell) P[z, cell]
    y1 = torch.einsum('rnc,rzc->rnz', u, PA)
    y2 = torch.einsum('rnc,rzc->rnz', w, PB)
    return y1, y2


def forward(PA, PB, c1, c2, dl):
    # round 1 (decrypt cipher): c1 in B, c2 in A
    rb, cb = rowcol(PB[:, c1, :]); ra, ca = rowcol(PA[:, c2, :])
    v1, v2 = step(rb, cb, ra, ca, PA, PB, dl)
    # round 2: v1 in B, v2 in A
    rb, cb = rowcol(torch.einsum('rnz,rzc->rnc', v1, PB)); ra, ca = rowcol(torch.einsum('rnz,rzc->rnc', v2, PA))
    p1, p2 = step(rb, cb, ra, ca, PA, PB, dl)
    return p1, p2


def exact_score(A, B, c1, c2, f, left):
    """exact unigram log10-likelihood per letter of a hard key"""
    A = ''.join(A); B = ''.join(B)
    pa, pb = dk.pos(A), dk.pos(B)
    lf = np.log10(f); s = 0
    for x, y in zip(c1, c2):
        a, b = AL[x], AL[y]
        for _ in range(2):
            rb, cb = pb[a]; ra, ca = pa[b]
            if rb == ra:
                sh = 1 if left else -1
                a, b = A[ra * 5 + (ca + sh) % 5], B[rb * 5 + (cb + sh) % 5]
            else:
                a, b = A[rb * 5 + ca], B[ra * 5 + cb]
        s += lf[AL.index(a)] + lf[AL.index(b)]
    return s / (2 * len(c1))


if __name__ == '__main__':
    fn = sys.argv[1]; R = int(sys.argv[2]) if len(sys.argv) > 2 else 256
    steps = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
    left = len(sys.argv) > 4 and sys.argv[4] == '1'
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
    torch.manual_seed(seed)
    T0 = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0; T1 = float(sys.argv[7]) if len(sys.argv) > 7 else 0.05
    dl = 1 if left else -1     # decrypt shift on the column (encrypt right => decrypt left)
    c1, c2 = load_pairs(fn)
    f = torch.tensor(unigram(), device=dev, dtype=torch.float64)
    LA = torch.randn(R, 25, 25, device=dev, dtype=torch.float64) * 0.3; LB = torch.randn(R, 25, 25, device=dev, dtype=torch.float64) * 0.3
    LA.requires_grad_(); LB.requires_grad_()
    opt = torch.optim.Adam([LA, LB], lr=0.05)
    t0 = time.time()
    for it in range(steps):
        tau = T0 * (T1 / T0) ** (it / steps)
        PA = sinkhorn(LA / tau); PB = sinkhorn(LB / tau)
        p1, p2 = forward(PA, PB, c1, c2, dl)
        ll = (torch.log((p1 * f).sum(-1).clamp_min(1e-12)) + torch.log((p2 * f).sum(-1).clamp_min(1e-12))).mean(-1)   # [R]
        loss = -ll.sum()
        opt.zero_grad(); loss.backward(); torch.nn.utils.clip_grad_norm_([LA, LB], 10.0 * R); opt.step()
        if it % 250 == 0 or it == steps - 1:
            print('it %d tau %.3f mean ll %.3f best %.3f (%.0fs)' % (it, tau, ll.mean().item() / math.log(10), ll.max().item() / math.log(10), time.time() - t0), flush=True)
    # harden
    res = []
    PA = PA.detach().cpu().numpy(); PB = PB.detach().cpu().numpy()
    c1l, c2l = c1.cpu().tolist(), c2.cpu().tolist(); fn_ = f.cpu().numpy()
    for r in range(R):
        keys = []
        for P in (PA[r], PB[r]):
            rows, cols = linear_sum_assignment(-np.log(P + 1e-12))
            box = [''] * 25
            for z, c in zip(rows, cols): box[c] = AL[z]
            keys.append(box)
        res.append((exact_score(keys[0], keys[1], c1l, c2l, fn_, left), ''.join(keys[0]), ''.join(keys[1])))
    res.sort(reverse=True)
    for s, A, B in res[:10]: print('%.3f %s %s' % (s, A, B))
