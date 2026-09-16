"""The sixteenth key: Lasry's CHI key of 13 Nov 1918 (comment #50 on the Top 50 post), recovered from the two-part
message FFVXV (page 187 scan) + AFAFF (page ???). Transposition key word CMBLAKOHIDENFJGP; the substitution square
is rebuilt here by aligning the transposed ciphertext bigrams with Lasry's plaintext, Norbert's corrections applied."""
import collections, json
import gaps, repair
KEYWORD = 'CMBLAKOHIDENFJGP'
PT = ('russischetundpolnheeresvergehrvollerfassenkwichtimesbesondersauspolnvergehrueberohlstationverziffert'
      'fungensoweitfernschreiberverbdmnithtarbeicetkrestschriftlichknachchefjkjx').upper()
# perm convention B: perm[i] = order in which column i is read out; alphabetical rank of the keyword letter
ranks = sorted(range(len(KEYWORD)), key=lambda i: (KEYWORD[i], i))
perm = [0] * len(KEYWORD)
for r, i in enumerate(ranks):
    perm[i] = r + 1
print('perm', perm)
msgs = gaps.parse()
a = next(m for m in msgs if m['page'] == '187')['ct']
b = next(m for m in msgs if m['page'] == '???')['ct']
print(len(a), len(b), len(a) + len(b), 'plaintext', len(PT), '->', 2 * len(PT))
for label, ct in (('combined', a + b), ('a', a), ('b', b)):
    s = repair.untranspose(ct, perm, 16, 'B')
    pairs = [s[i:i + 2] for i in range(0, len(s) - 1, 2)]
    print(label, len(pairs), ' '.join(pairs[:20]))
# align combined with PT
s = repair.untranspose(a + b, perm, 16, 'B')
pairs = [s[i:i + 2] for i in range(0, len(s) - 1, 2)]
cell = collections.defaultdict(collections.Counter)
for bg, ch in zip(pairs, PT):
    cell[bg][ch] += 1
sq = {}
conf = 0
for bg, c in sorted(cell.items()):
    top, n = c.most_common(1)[0]
    if len(c) > 1:
        conf += 1
    sq[bg] = top
    print(bg, dict(c))
print('cells', len(sq), 'conflicting', conf)
square = ''.join(sq.get(x + y, '-') for x in 'ADFGVX' for y in 'ADFGVX')
print(square)
json.dump({'n': 16, 'perm': perm, 'square': square, 'note': 'CHI key 13 Nov 1918, Lasry comment 50'}, open('key16.json', 'w'))
