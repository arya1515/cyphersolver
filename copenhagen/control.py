"""control.py -- matched control for the Copenhagen attack: random passages of the same length (103 letters,
3 sentence breaks) in a given language, enciphered with a random 20-symbol simple substitution (so about
the same number of distinct letters as the cryptogram), attacked with the identical annealer.
usage: python control.py --corpus DIR --lang da [--trials 3]
"""
import sys, random, re, pathlib, collections
import solve as cp
sys.stdout.reconfigure(encoding='utf-8')
lang = cp.arg('--lang', 'da'); trials = int(cp.arg('--trials', 3))
lm = cp.build_lm(lang)
text = ''
for f in sorted(cp.CORPUS.glob(f'corp_{lang}_*.txt')):
    raw = f.read_text(encoding='utf-8', errors='ignore')
    m = re.search(r'\*\*\* ?START OF.*?\*\*\*', raw); raw = raw[m.end():] if m else raw
    text += cp.normalize(raw, lang) + ' '
words = text.split()
rng = random.Random(int(cp.arg('--seed', 7)))
for t in range(trials):
    # pick a passage of ~103 letters made of 4 sentences (we cut at word boundaries)
    while True:
        i = rng.randrange(len(words) - 60); passage = []
        while sum(len(w) for w in passage) < 103: passage.append(words[i]); i += 1
        letters = ''.join(passage)[:103]
        if len(set(letters)) <= 22: break
    # 3 breaks at random word boundaries -> segments
    cuts = sorted(rng.sample(range(10, 95), 3))
    segs = [letters[a:b] for a, b in zip([0] + cuts, cuts + [len(letters)])]
    alphabet = sorted(set(letters)); syms = [f's{k}' for k in range(len(alphabet))]; rng.shuffle(syms)
    key = dict(zip(alphabet, syms))
    tokens = []
    for j, seg in enumerate(segs):
        tokens += [key[c] for c in seg]
        if j < len(segs) - 1: tokens.append('|')
    res = cp.solve(lm, tokens, rng)
    sc, mapping, out, cov = res[0]
    dec = ''.join(out); truth = ''.join(segs)
    acc = sum(1 for a, b in zip(dec, truth) if a == b) / len(truth)
    print(f'{lang} trial {t+1}: {len(alphabet)} letters; best score {sc/len(truth):.3f}/letter cov {cov:.2f}; accuracy {acc:.2f}')
    print('   found: ' + ' | '.join(out)); print('   truth: ' + ' | '.join(segs))
    print('   truth score %.3f/letter' % (lm.score(segs) / len(truth)), flush=True)
