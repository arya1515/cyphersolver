"""eval.py - score a decoder against the known-plaintext blocks.

Letter accuracy is measured by Levenshtein alignment of the decoded letter string against the true one
(spaces removed), which does not punish a mis-placed word boundary twice. Word accuracy counts words of
the truth that appear, in order, in the decode (longest common subsequence over words).

usage: python bethune/eval.py [--model em_model_v2.json] [--beam 60] [--argmax] [--blocks A,B3,..]
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lm as LMOD
import decode2 as D
sys.stdout.reconfigure(encoding='utf-8')


def lev(a, b):
    n, m = len(a), len(b)
    prev = list(range(m+1))
    for i in range(1, n+1):
        cur = [i] + [0]*m
        ca = a[i-1]
        for j in range(1, m+1):
            cur[j] = min(prev[j]+1, cur[j-1]+1, prev[j-1] + (ca != b[j-1]))
        prev = cur
    return prev[m]


def lcs(a, b):
    n, m = len(a), len(b)
    prev = [0]*(m+1)
    for i in range(1, n+1):
        cur = [0]*(m+1)
        for j in range(1, m+1):
            cur[j] = prev[j-1]+1 if a[i-1] == b[j-1] else max(prev[j], cur[j-1])
        prev = cur
    return prev[m]


def blocks(path='bethune/corpus_v2.txt'):
    for line in open(path, encoding='utf-8'):
        if line.startswith('#') or '|' not in line:
            continue
        p = [x.strip() for x in line.split('|')]
        yield p[0], p[2], LMOD.norm_keep_spaces(p[3])


def main():
    model_path = sys.argv[sys.argv.index('--model')+1] if '--model' in sys.argv else 'bethune/em_model_v2.json'
    beam = int(sys.argv[sys.argv.index('--beam')+1]) if '--beam' in sys.argv else 60
    only = set(sys.argv[sys.argv.index('--blocks')+1].split(',')) if '--blocks' in sys.argv else None
    model = D.load_model(model_path)
    if '--wide' in sys.argv:
        model = D.widen(model, float(sys.argv[sys.argv.index('--wide')+1]))
    lm = LMOD.load()
    vocab = [w for w, c in lm.uni.items() if w != '<s>' and (c >= 2 or len(w) > 6)]
    trie = D.build_trie(vocab)
    LT = WT = LN = WN = 0
    for lab, ct, truth in blocks():
        if only and lab not in only:
            continue
        sc, words = D.decode(ct.split(), model, lm, trie, beam)
        got = ' '.join(words)
        gl, tl = got.replace(' ', ''), truth.replace(' ', '')
        lok = max(0, len(tl) - lev(gl, tl))
        wok = lcs(got.split(), truth.split())
        LT += lok; LN += len(tl); WT += wok; WN += len(truth.split())
        print('%-3s letters %3d/%3d %5.1f%%  words %3d/%3d %5.1f%%' %
              (lab, lok, len(tl), 100.0*lok/len(tl), wok, len(truth.split()), 100.0*wok/len(truth.split())))
        print('   got  : %s' % got)
        print('   truth: %s' % truth)
    print('\nTOTAL letters %d/%d = %.1f%%   words (in order) %d/%d = %.1f%%  [model %s]' %
          (LT, LN, 100.0*LT/LN, WT, WN, 100.0*WT/WN, os.path.basename(model_path)))


main()
