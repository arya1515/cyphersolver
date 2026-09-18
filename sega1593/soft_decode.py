# Soft polyphonic decoder using per-box class probabilities (CNN) and the French 6-gram LM beam search.
# Token options: one letter of class c (weight log p_c), skip (null), two letters (merge, penalised).
import sys, os, json, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sp53'))
from homo import LM
PAIRS = ['an', 'bo', 'cp', 'dq', 'er', 'fs', 'gt', 'hu', 'ix', 'ly', 'mz']
CODES = ['que', 'qui', 'pour']
NULL = 14; CODE = 15
LET = 'abcdefghilmnopqrstuxyz'
CLS_OF = {ch: PAIRS.index(p) for p in PAIRS for ch in p}

def soft_decode(probs, areas, lm, beam=2000, nbest=3, merge_pen=-4.0, skip_floor=0.0005, mix=0.85):
    beams = [('', '', 0.0)]
    for pr, area in zip(probs, areas):
        pr = np.asarray(pr, float)
        pr = mix * pr + (1 - mix) / len(pr)   # smooth
        if area < 130: pskip = 0.9
        else: pskip = max(pr[NULL] * 0.5, skip_floor)
        new = []
        for disp, ctx, sc in beams:
            # skip
            new.append((disp, ctx, sc + np.log(pskip)))
            # single letters
            for ch in LET:
                c = CLS_OF[ch]; p = pr[c]
                if p < 0.02: continue
                s2 = sc + np.log(p) + lm.logp(ctx[-5:], ch)
                new.append((disp + ch, ctx + ch, s2))
            for k, code in enumerate(CODES):
                p = pr[11 + k]
                if p < 0.02: continue
                t2 = ctx; s2 = sc + np.log(p)
                for ch in code: s2 += lm.logp(t2[-5:], ch); t2 += ch
                new.append((disp + '[' + code + ']', t2, s2))
            if pr[CODE] > 0.05:
                new.append((disp + '#', ctx + ' ', sc + np.log(pr[CODE])))
            # merge: two letters, classes unknown -> LM only, penalised; restrict to top letters via LM
            if area > 300:
                base = sc + merge_pen
                cands = []
                for ch in LET:
                    l1 = lm.logp(ctx[-5:], ch)
                    if l1 < -6: continue
                    for ch2 in LET:
                        l2 = lm.logp((ctx + ch)[-5:], ch2)
                        cands.append((l1 + l2, ch + ch2))
                cands.sort(reverse=True)
                for l, pair in cands[:6]:
                    new.append((disp + pair, ctx + pair, base + l))
        new.sort(key=lambda x: -x[2])
        # dedupe by ctx tail
        seen = set(); kept = []
        for b in new:
            key = b[1][-8:]
            if key in seen: continue
            seen.add(key); kept.append(b)
            if len(kept) >= beam: break
        beams = kept
    return [(b[0], b[2]) for b in beams[:nbest]]

if __name__ == '__main__':
    # usage: soft_decode.py probs.json boxes_g2.json k0 k1 [beam]
    probs = json.load(open(sys.argv[1])); boxes = json.load(open(sys.argv[2]))
    k0, k1 = int(sys.argv[3]), int(sys.argv[4]); beam = int(sys.argv[5]) if len(sys.argv) > 5 else 1500
    lm = LM(os.environ.get('LMPATH', os.path.join(os.path.dirname(__file__), '..', 'sp53', 'fr6.pkl')))
    for k in range(k0, k1 + 1):
        pr = probs[str(k)]; ar = [b[4] for b in boxes[str(k)]]
        res = soft_decode(pr, ar, lm, beam=beam)
        print(f'L{k}', round(res[0][1], 1), res[0][0], flush=True)
