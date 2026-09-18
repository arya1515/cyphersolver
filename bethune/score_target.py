"""score_target.py <ct_file> [--fixed k=v,...] — decode a target and report two objective figures:
the total model score, and the share of decoded characters that sit inside real lexicon words.
A correct new key value should raise both; a wrong one should not."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lm as LMOD, decode2 as D
sys.stdout.reconfigure(encoding='utf-8')

ctf = [a for a in sys.argv[1:] if a.endswith('.txt')][0]
if '--fixed' in sys.argv:
    for kv in sys.argv[sys.argv.index('--fixed')+1].split(','):
        k, v = kv.split('='); D.FIXED[k] = v
model = D.load_model('bethune/em_model_v2.json')
lm = LMOD.load()
vocab = [w for w, c in lm.uni.items() if w != '<s>' and (c >= 2 or len(w) > 6)]
trie = D.build_trie(vocab)
real = set(w for w, c in lm.uni.items() if c >= 3 and len(w) >= 2)
tot = nchar = good = 0.0
for line in open(ctf, encoding='utf-8'):
    if line.startswith('#') or not line.strip():
        continue
    p = [x.strip() for x in line.split('|')]
    ct = p[2] if len(p) >= 4 else p[-1]
    sc, words = D.decode(ct.split(), model, lm, trie, 60)
    tot += sc or 0
    for w in words:
        if w.startswith('['):
            continue
        nchar += len(w)
        if w in real:
            good += len(w)
print('%-22s score %10.1f   in-lexicon chars %5.1f%% (%d/%d)' %
      (os.path.basename(ctf), tot, 100.0*good/max(nchar, 1), good, nchar))
