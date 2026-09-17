import sys, collections
sys.argv.append('--wide')
import align
sys.stdout.reconfigure(encoding='utf-8')
paras = align.parse_cipher('herleville.txt')
P2 = paras[1]
pw = align.words(align.P2)
cnt = collections.Counter(P2)
positions = [i for i, g in enumerate(P2) if cnt[g] > 1]
for i in positions:
    c = list(P2); c[i] = 900 + i
    res = align.align(c, pw, beam=20000, per_bucket=2000)
    print('knockout pos', i + 1, 'group', P2[i], '->', len(res), 'alignments', flush=True)
    if res:
        sc, m, tr = res[0]
        print('   ', round(sc, 1), ' '.join('%d=%s' % (g, u if u else '_') for g, u in tr), flush=True)
