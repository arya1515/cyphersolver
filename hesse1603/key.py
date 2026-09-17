# Cipher Henri IV - Maurice of Hesse-Cassel (Oct 1602), after Rommel, Allg. Zeitschrift f. Geschichte V (1846) 402-403,
# checked on Rommel's own decipherment of the 3 April 1604 letter (pp.170-175) and on p.99.
# Group notation in transcriptions:  NN bare letter | NN, virgule list | NN: two-dot list | NN_ overbar list
#   D = doubling sign (repeat previous symbol) | X = cancel sign (previous number means nothing)
#   {te} {grand} {Hongrie} {tra} {tue} {troubles} {tion} {tant} {tous} {tout} {ve} {va} {ville} {votre} = special glyphs
#   [[clear text]]   | ? = illegible
LET = {}
for letter, nums in {'a':[31,34,57,80],'b':[26,35,58],'c':[27,36,59],'d':[28,37,60],'e':[32,38,61,81],'f':[29,39,62],
    'g':[30,40,63],'h':[33,41,64],'i':[12,42,65,82],'l':[14,43,66],'m':[44,67,85],'n':[15,45,68],'o':[16,46,69,83],
    'p':[17,47,70],'q':[18],'r':[19,49,72,84],'s':[20,25,50,55,73,78,87],'t':[21,51,74],'u':[22,52,75,86],'x':[23,76],'y':[24,54,77]}.items():
    for n in nums: LET[n]=letter
# 70 (p) is not in Rommel's table (row 3 gap) but is required by the control text ("presse", "perdra"). 83 and 85 in row 4
# sit under o and m in the print; taken as m and l after Tomokiyo; to be checked on the texts.
VIRG = {7:'non',8:'je',10:'?10',15:'in',17:'la',18:'le',19:'le',24:'lettre',25:'leur',30:'ma',34:'me',38:'mo',39:'mon',40:'moins',41:'na',42:'ne',44:'no',45:'ny',
        46:'notre',47:'non',48:'nous',51:'oui',52:'on',53:'ou',54:'pa',55:'paix',56:'pays',59:'pays',60:'pour',61:'pro',65:'pro',66:'pre',67:'quand',68:'que',69:'quelque',
        70:'qui',71:"qu'il",72:'quoy',73:'ra',74:'re',77:'roy',82:'?82,',83:'rompre',85:'sa',86:'se',89:'Saxe',96:'subjects',99:'ta'}
# alignment of the 1846 print is ambiguous for 10/15 (in/la), 24/25 (lettre/leur), 55/56/59 (paix/pays), 60/61/65/66 (pour/pro/pre/quand); set by texts: 17,=la? 18,=le 25,=leur 59,=pays 60,=pour 65,=pro 68,=que
DOTS = {30:'cour',10:'imperiale',31:'con',33:'ca',34:'car',36:'dans',40:'don',42:'don',45:'da',46:'di',48:'do',49:'de',52:'diete',54:'duc',58:'Espagnols',
        59:'estat',61:'eulx',62:'en',64:'point',69:'faire',68:'elle',70:'faict',71:'fils',73:'fort',76:'forces',81:'fa',84:'forces',85:'fa',91:'general',92:'troupes',96:'Hollande',99:'guerre'}
# 62:10: = Empire ; 52:10: = diete de l'Empire  (two-group entries)
BAR = {12:'Bouillon',19:'?19_',26:'Comte',28:'Conseil',31:'Pape',33:'Empereur',35:"Roi d'Espagne",37:"Roi d'Angleterre",40:"l'Archiduc",43:"l'Electeur Palatin",45:'Brandenbourg',
       51:'Brunswick',52:'provinces unies',53:'provinces unies',55:"l'administrateur",59:'Turc',62:'Prince',63:'duc',64:'Marquis',65:'Protestant',68:'affaire',70:'Allemagne',
       71:'alliance',72:'alliés',73:'Ambassadeur',74:'Angleterre',78:'argent',79:'armée',83:'avoir',84:'au',86:'afin',88:'aux',95:'pays-bas',98:'?98'}
NULLS = {2,4,5,6}   # Pratt; 7,8 are in the virgule list
import re
TOK = re.compile(r'\[\[.*?\]\]|\{[^}]+\}|\d+[,:_]?|[DX?]|\S')
def decode(s, sep=''):
    out=[]; prev=None
    for tok in TOK.findall(s):
        if tok.startswith('[['): out.append(' '+tok[2:-2]+' '); prev=None; continue
        if tok=='{4}': out.append('t(e|ion)'); prev=tok; continue
        if tok=='{4c}': out.append('tant'); prev=tok; continue
        if tok=='{tra}': out.append('tr(a|e)'); prev=tok; continue
        if tok=='{hat}': out.append('va'); prev=tok; continue
        if tok=='{8}': out.append('tous'); prev=tok; continue
        if tok=='{9}': out.append('tout'); prev=tok; continue
        if tok.startswith('{'): out.append('<'+tok[1:-1]+'>' if tok[1:-1] in ('grand','Hongrie','troubles','ville','votre','tra','tue','hat','♀','Ψ','∴') else tok[1:-1]); prev=tok; continue
        if tok=='D': out.append(out[-1] if out else '?D'); continue
        if tok=='X':
            if out: out.pop()
            continue
        if tok=='?': out.append('?'); continue
        m=re.match(r'(\d+)([,:_]?)$',tok)
        if not m: out.append('['+tok+']'); continue
        n=int(m.group(1)); d=m.group(2)
        if d==',': out.append('<'+VIRG.get(n,'?%d,'%n)+'>')
        elif d==':': out.append('<'+DOTS.get(n,'?%d:'%n)+'>')
        elif d=='_': out.append('<'+BAR.get(n,'?%d_'%n)+'>')
        else:
            if n in LET: out.append(LET[n])
            elif n in NULLS: pass
            else: out.append('[%d?]'%n)
    return sep.join(out)
if __name__=='__main__':
    import sys
    for line in sys.stdin: 
        line=line.strip()
        if line and not line.startswith('#'): print(decode(line))
