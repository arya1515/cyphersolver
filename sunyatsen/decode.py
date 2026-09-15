"""Final annotated decoding of the Tanaka -> Sun Yat-sen telegram (Swatow, 3 April 1916).

Key (recovered by family.py): systematic code condenser, vowel-major,
consonants l m n p q r s t v x y z b c d f g h j k  (alphabet rotated to start at l),
vowel columns e a i o u = 01-20, 21-40, 41-60, 61-80, 81-99/00; no additive.
Plain code = standard Chinese telegraph code (電報新編 / 明密碼電報書 numbering).

Writes decode_out.txt (UTF-8)."""
import os, sys
from family import code2ch, CONS, VOW
from show import key_from_name
here = os.path.dirname(os.path.abspath(__file__))
sys.stdout = open(os.path.join(here, 'decode_out.txt'), 'w', encoding='utf-8')
tbl, rot = key_from_name('rot8', 'eaiou', 'vow', 1)

RECEIVED = ("baxuxupeja qicijinati bemigasiqi jakebiqoye kufohemige tuxaboboba "
            "gedoeijiga poyevayoxa leyoleveke biromapesa vorobenife xikebiqoye qekufiyaqa "
            "tijaqixiqo xitohatula xopavajejo ropezpo ngobunibai")
# Emended reading of the letters (cursive misreadings by the receiving clerk):
#   xu -> xe (潮城)      e  -> c  (莫)        he -> ne (光復)      ha -> na (支持)
EMENDED  = ("baxuxepeja qicijinati bemigasiqi jakebiqoye kufonemige tuxaboboba "
            "gedocijiga poyevayoxa leyoleveke biromapesa vorobenife xikebiqoye qekufiyaqa "
            "tijaqixiqo xitonatula xopavajejo rope")
GARBLED_TAIL = "zpo ngobunibai"
NOTES = {2: 'received xu pe = 9004 (no such code); xe pe = 1004 城 — 潮城 is the term used in Mo\'s own telegram of 27 March',
         12: 'received he mi = 1842 怩; ne mi = 0342 光 (光復 "recovered")',
         17: 'ei in gedoEIjiga: e is a misread c; ci ji = 5459 莫',
         36: '5068 as received; 翼X unresolved (to = 68 unconfirmed elsewhere)',
         37: 'received ha tu = 3888 璸; na tu = 2388 支 (支持)',
         }

def decode(letters):
    s = letters.replace(' ', '')
    syl = [s[i:i+2] for i in range(0, len(s), 2)]
    assert all(a in CONS and b in VOW for a, b in syl), syl
    nums = [tbl[x] for x in syl]
    codes = ['%02d%02d' % (nums[i], nums[i+1]) for i in range(0, len(nums) - 1, 2)]
    return syl, codes

syl, codes = decode(EMENDED)
print('Received : Twelve', RECEIVED, 'tanaka')
print('Emended  :', EMENDED, '| garbled tail:', GARBLED_TAIL)
print()
print('%3s  %-6s %-5s %s' % ('#', 'syll', 'code', 'char'))
text = ''
for i, c in enumerate(codes):
    ch = code2ch.get(c, '□'); text += ch
    print('%3d  %-6s %-5s %s   %s' % (i + 1, syl[2*i] + ' ' + syl[2*i+1], c, ch, NOTES.get(i + 1, '')))
print()
print('Plain text (%d characters):' % len(text))
print(text)
print()
print('Punctuated: 潮城由莫擎宇獨立。我軍亦光復汕頭。後莫率大隊來，令我退出鎮守府。我軍力薄，暫由翼□支持。文慧返……[3 codes garbled]')
print()
# table
print('Recovered condenser table (row = consonant, column = vowel):')
print('     ' + '   '.join('eaiou'))
for c in rot:
    print(c, '  ', ' '.join('%02d' % tbl[c + v] for v in 'eaiou'))
