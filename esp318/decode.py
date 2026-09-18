import json, sys, re
K=json.load(open('keys/cifra_general.json',encoding='utf-8'))
# symbol alphabet of the cifra general (Galende Diaz app.1), transcribed in ASCII shorthand
ALPHA={
 'a':'A','at':'A','a#':'A','ap':'A','C#':'A',
 'r':'B','y':'B','rp':'B','r#':'B',
 '+':'C','+o':'C','#':'C','##':'C',
 'd':'D','-o':'D','q-':'D','o-':'D',
 'h':'E','h-':'E','ho':'E','hp':'E','=':'E',
 'm':'F','m-':'F','mo':'F','mp':'F',
 'k':'G','k-':'G','ko':'G',
 '8':'H','8+':'H','oo-':'H','8t':'H',
 '3':'I','3+':'I','3u':'I','3p':'I','L':'I',
 'n':'L','n-':'L','np':'L','nop':'L',
 'p':'M','pt':'M','p-':'M','po':'M',
 'q':'N','q-':'N','qt':'N','qo':'N',
 'b':'O','xo':'O','x':'O','x+':'O','e':'O',
 'f':'P','ff':'P','f-':'P','ff-':'P',
 '4':'Q','4#':'Q','4o':'Q','4u':'Q',
 '7':'R','7-':'R','o7':'R','.7':'R',
 '9':'S','9t':'S','9o':'S','9-':'S',
 'T':'T','t':'T','t-':'T','to':'T','B':'T',
 'D':'U','D-':'U','Do':'U',
 'X':'X','Xt':'X','o#':'X','Xp':'X',
 'o':'Y','O':'Y','o+':'Y',
 'z':'Z','z:':'Z','z.':'Z',
}
def dec(tok):
    t=tok.strip()
    if not t: return ''
    if t in K: return '['+K[t][0]+']'
    if t in ALPHA: return ALPHA[t].lower()
    return '{'+t+'}'
for line in sys.stdin:
    line=line.rstrip('\n')
    if not line.strip(): print(); continue
    out=[dec(t) for t in line.split()]
    print(' '.join(out))
