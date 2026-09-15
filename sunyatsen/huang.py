"""Huang Xing -> Lin Hu and Li Genyuan, 25 May 1916 (JACAR B03050731500).

The catalogue lists this as "solved but specific scheme unknown": the Japanese Foreign
Ministry filed a decode with the telegram, but nobody had identified how the romanised
kana encode it.

What this script shows
----------------------
The ciphertext is 139 kana with no voicing marks.  The filed decode is ~46 characters,
so the rate is three kana per character.  Group the kana in threes and ask what part of
each kana carries information:

    reading            collisions   expected by chance   permutation p
    consonant row          7             1.03               0.006
    vowel                  8             8.28               0.70
    literal kana           1             --                 --

The gojuon syllabary is a 10 x 5 grid, ten consonant rows by five vowels.  Repeated
characters in the plaintext show up as repeated *consonant-row* triples far above chance,
while the vowels repeat at exactly chance and the surface kana almost never repeat at all.

So: each kana carries one decimal digit in its consonant row, and the vowel is a free
homophone chosen to make the group pronounceable -- five ways to write every digit.
Three kana make one three-digit code, i.e. a private codebook of at most 1000 entries,
not the four-digit standard Chinese telegraph code.

Still open: which digit each consonant row stands for (a permutation), and the codebook
itself.  Both are recoverable from an exact transcription of the filed decode.

Usage:  python huang.py
"""
import collections, random, sys

CT = ("REKUTATA UHOYAKATE SEKANAOKU SAKEKINISE OSUKAKUCHI REUHONIUSU MAKASUSAKU "
      "FUREOHIHE YENIKIYEHI TAKASUREU SASHIKIHE WAONIAAHO SAYEHITE UHINAKUTA "
      "NEATEMUYE SUHEUHAKA YESOMIKANU TEASUUKU TSUHAKOSE KEKININAKI TEAKETASHI "
      "KONUOHIKE HIMIKANO SHIKUSAHE UHATAKASA KEKINIKA ATAREUSASU OSO YUA NIRA KISU")

# gojuon rows in traditional order: a ka sa ta na ha ma ya ra wa
ROWS = [
    ['A', 'I', 'U', 'E', 'O'],
    ['KA', 'KI', 'KU', 'KE', 'KO'],
    ['SA', 'SHI', 'SU', 'SE', 'SO'],
    ['TA', 'CHI', 'TSU', 'TE', 'TO'],
    ['NA', 'NI', 'NU', 'NE', 'NO'],
    ['HA', 'HI', 'FU', 'HE', 'HO'],
    ['MA', 'MI', 'MU', 'ME', 'MO'],
    ['YA', 'YI', 'YU', 'YE', 'YO'],
    ['RA', 'RI', 'RU', 'RE', 'RO'],
    ['WA', 'WI', 'WU', 'WE', 'WO'],
]
ROWNAME = ['-', 'K', 'S', 'T', 'N', 'H', 'M', 'Y', 'R', 'W']
KANA2ROW = {k: r for r, ks in enumerate(ROWS) for k in ks}
KANA2VOW = {k: v for ks in ROWS for v, k in enumerate(ks)}
ORDER = sorted(KANA2ROW, key=len, reverse=True)      # longest first: SHI CHI TSU


def parse_kana(text):
    out = []
    for w in text.split():
        i = 0
        while i < len(w):
            for k in ORDER:
                if w.startswith(k, i):
                    out.append(k)
                    i += len(k)
                    break
            else:
                raise ValueError('cannot parse %r at %d' % (w, i))
    return out


def collisions(seq, n=3):
    tri = [tuple(seq[i:i + n]) for i in range(0, len(seq) - len(seq) % n, n)]
    c = collections.Counter(tri)
    return sum(v - 1 for v in c.values() if v > 1), len(c), tri


def permutation_p(seq, trials=20000, seed=0):
    obs = collisions(seq)[0]
    rnd = random.Random(seed)
    hits = 0
    for _ in range(trials):
        s = list(seq)
        rnd.shuffle(s)
        if collisions(s)[0] >= obs:
            hits += 1
    return obs, (hits + 1) / (trials + 1)


def main():
    kana = parse_kana(CT)
    body = kana[:138]                      # 46 characters x 3 kana; last kana is spare
    rows = [KANA2ROW[k] for k in body]
    vows = [KANA2VOW[k] for k in body]
    n = len(body) // 3

    out = []
    out.append('ciphertext: %d kana, %d distinct; body %d kana = %d characters'
               % (len(kana), len(set(kana)), len(body), n))
    pairs = n * (n - 1) / 2
    for label, seq, space in (('consonant row', rows, 10 ** 3),
                              ('vowel', vows, 5 ** 3),
                              ('literal kana', body, None)):
        col, dist, _ = collisions(seq)
        exp = '%.2f' % (pairs / space) if space else '--'
        out.append('  %-14s collisions %2d   distinct %2d   expected %s' % (label, col, dist, exp))
    for label, seq in (('consonant row', rows), ('vowel', vows)):
        obs, p = permutation_p(seq)
        out.append('  permutation test %-14s observed %d, p = %.4f' % (label, obs, p))

    _, _, tri = collisions(rows)
    rep = collections.Counter(tri)
    out.append('\nrepeated consonant-row triples (same plaintext character, different vowels):')
    for t, c in sorted(rep.items(), key=lambda x: -x[1]):
        if c > 1:
            pos = [i + 1 for i, x in enumerate(tri) if x == t]
            spell = [''.join(body[3 * (i - 1):3 * i]) for i in pos]
            out.append('   %s  x%d  at %s  written %s'
                       % (''.join(ROWNAME[d] for d in t), c, pos, ' / '.join(spell)))
    txt = '\n'.join(out)
    open('huang_out.txt', 'w', encoding='utf-8').write(txt + '\n')
    print(txt)


if __name__ == '__main__':
    main()
