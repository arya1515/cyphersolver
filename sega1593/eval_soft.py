# Evaluate soft decoding on held-out f.188v lines against the f.185 text.
# usage: eval_soft.py probs_boot3_7.npy 7,8,9,10 [beam]
import sys, os, json, re, difflib, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'sp53'))
from homo import LM
from soft_decode import soft_decode
pr = np.load(sys.argv[1]); holds = [int(x) for x in sys.argv[2].split(',')]
beam = int(sys.argv[3]) if len(sys.argv) > 3 else 1500
boxes = json.load(open('lines/f188v_g2.json'))
lines = list(range(3, 23)); off = {}; i = 0
for k in lines: off[k] = i; i += len(boxes[str(k)])
lm = LM(os.environ.get('LMPATH', os.path.join(os.path.dirname(__file__), '..', 'sp53', 'fr6.pkl')))
truth = re.sub(r'[^a-z]', '', open('f185_cipher_only.txt', encoding='utf-8').read().lower().replace('j', 'i').replace('v', 'u'))
for k in holds:
    p = pr[off[k]:off[k] + len(boxes[str(k)])]; ar = [b[4] for b in boxes[str(k)]]
    res = soft_decode(p, ar, lm, beam=beam)
    dec = res[0][0]; flat = re.sub(r'\[|\]', '', dec)
    # best local match in truth
    sm = difflib.SequenceMatcher(None, truth, flat, autojunk=False)
    m = sm.find_longest_match(0, len(truth), 0, len(flat))
    blocks = sm.get_matching_blocks(); matched = sum(b.size for b in blocks)
    print(f'L{k} dec: {dec}')
    print(f'    longest common run {m.size}: "{truth[m.a:m.a+m.size]}"  matched chars {matched}/{len(flat)}')
