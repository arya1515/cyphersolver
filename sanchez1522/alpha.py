# -*- coding: utf-8 -*-
"""Sign -> plaintext letter for Sanchez's 1522 cipher, in the transcription labels used for the
code groups. Values marked GT are fixed by ground truth: the alignment of R9605's cipher with the
clerk's 1522 decipherment on the facing leaves (see calibration_r9605.md). The rest are read off
Tomokiyo's hand-drawn alphabet table and are provisional.
Multi-character labels must be tried longest-first."""

# fixed against R9605 + its contemporary decipherment (calibration_r9605.md)
GROUND_TRUTH = {
 'n':'a',   # dixe A, buenAs
 'y':'e',   # dixE, rEspondido, rEpublica   (the label 'y' = the curl Tomokiyo draws for e)
 'g':'r',   # embaxadoR, Respondido, Republica
 'ai':'i',  # HungRIa, escrIvo
 'o':'x',   # diXe
 '#':'o',   # respOndidO, escrivO
 'q':'s',   # reSpondido  (NB Tomokiyo's alphabet gives q = t; two similar glyphs)
 'ao':'p',  # resPondido
 '&':'n',   # respoNdido
 'm':'v',   # escriVo
 'z':'c',   # esCrivo, Camino
 'B':'m',   # caMino
 's':'s',   # buenaS, loS  (the q-with-double-bar, used as the plural)
}
ALPHA = {
 'n':'a',  '3f':'a',
 'b':'b',
 'z':'c',  'e9':'c',
 'oo':'d', '3':'d', 'fx':'d',
 '4':'e',  'zz':'e',
 'p':'f',
 'OO':'g', 'L':'g',
 'x':'h',  'mo':'h',
 'ai':'i',
 'l':'l',
 'B':'m',
 'zn':'n', 'tt':'n',
 '#':'o',  'ne':'o',
 'ao':'p', 'ts':'p',
 '8':'q',  'j9':'q',
 'g':'r',
 's':'s',  'xo':'s', 'P':'s',
 'q':'t',  'Lo':'t',
 'm':'u',  'jt':'u',
 'o':'x',
 'y':'y',
 'A':'z',
}
KEYS = sorted(ALPHA, key=len, reverse=True)
def spell(tok):
    out=[];i=0
    while i < len(tok):
        for k in KEYS:
            if tok.startswith(k,i):
                out.append(ALPHA[k]); i+=len(k); break
        else:
            out.append('['+tok[i]+']'); i+=1
    return ''.join(out)
if __name__=='__main__':
    import sys
    for t in sys.argv[1:]: print(t,'=',spell(t))
