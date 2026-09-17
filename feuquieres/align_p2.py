import sys
sys.argv.append('--wide')
import align
sys.stdout.reconfigure(encoding='utf-8')
paras = align.parse_cipher('herleville.txt')
pw2 = align.words(align.P2)
res = align.align(paras[1], pw2)
print('P2 hard alignments', len(res))
for sc, m, tr in res[:8]:
    print(round(sc, 1), ' '.join('%d=%s' % (g, u if u else '_') for g, u in tr))
