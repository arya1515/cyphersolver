# -*- coding: utf-8 -*-
"""Sign -> plaintext letter, read off Tomokiyo's alphabet table (tomokiyo/AlonsoSanchez.png)
and expressed in the transcription labels used for the code groups.
Multi-character labels must be tried longest-first."""
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
