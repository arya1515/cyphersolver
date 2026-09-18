# -*- coding: utf-8 -*-
"""Decrypt Cardinal Soglia -> nuncio Viale Prela, Rome 15 June 1848 (L'Italia del Popolo, 30 June 1848).
System: digit 5 = word separator; 2-digit groups from digits {0,1,2,3,4,6,7,9} = letters/syllables (homophonic);
8XXX = one-part (alphabetical) code words; a lone 1/2/3/4 between separators = , ; : .
Usage: python decode.py            (plaintext, unknown code words as [8xxx])
       python decode.py --guess    (fill unresolved code words with the guesses in CODE_GUESS)"""
import sys, re
DIN = {'01':'del','02':'no','03':'k','04':'s','06':'ta','07':'al','09':'a','10':'chi','11':'m','12':'in','14':'ma',
       '16':'c','19':'p','20':'gli','21':'e','22':'ne','23':'la','24':'n','26':'che','30':'qu','31':'da','33':'b',
       '34':'mi','36':'t','37':'con','39':'d','40':'de','41':'l','42':'di','43':'se','44':'e','46':'o','47':'al',
       '49':'r','60':'il','61':'f','63':'per','64':'si','66':'st','67':'i','69':'te','70':'v','71':'ti','72':'g',
       '74':'z','76':'to','77':'b','79':'p','90':'c','91':'f','92':'l','93':'d','94':'g','96':'m','97':'n','99':'s'}
CODE = {'8319':'Imperatore','8340':'istruzione','8374':'Monsignor','8422':'opportuno',
        '8424':'ordin','8429':'Padre','8433':'parte','8446':'port','8620':'Roma'}
CODE_GUESS = {'8247':'foglio','8116':'Colonia','8120':'com','8122':'cotest','8211':'è','8346':'lontan',
              '8310':'guerra','8737':'Tuttavia','8110':'col fine di','8632':'Signor'}
PUNCT = {'1':',','2':';','3':':','4':'.'}
def load():
    s = open('ct2.txt').read().strip()
    return s.replace('5190905990984466', '5190904990984466', 1)   # print error: 4 printed as 5 (cf. 2nd 'passaporti')
def decode(s, guess=False):
    code = dict(CODE, **(CODE_GUESS if guess else {}))
    words = []
    for r in s.split('5'):
        i, w = 0, ''
        while i < len(r):
            if r[i] == '8' and i + 4 <= len(r):
                c = r[i:i+4]; w += ('(' + code[c] + ')') if c in code else '[' + c + ']'; i += 4
            elif i + 2 <= len(r):
                w += DIN.get(r[i:i+2], '<' + r[i:i+2] + '>'); i += 2
            else:
                w += PUNCT.get(r[i], '{' + r[i] + '}'); i += 1
        words.append(w)
    return re.sub(' +', ' ', ' '.join(words)).replace(' ,', ',').replace(' .', '.').replace(' ;', ';').replace(' :', ':')
if __name__ == '__main__':
    print(decode(load(), '--guess' in sys.argv))
