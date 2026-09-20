# -*- coding: utf-8 -*-
"""f.55 (BnF fr.3181, Catherine de Medicis to the bishop of Rennes, 31 July 1563)
Transcription of the 13 ciphered lines into ASCII glyph tokens, and decoding with
the Bishop of Rennes' key (Tomokiyo reconstruction), as calibrated on this hand."""

MAP = {
 # letters
 'z':'a','eta':'a','S':'a','ff':'a',
 'h':'b','g8':'b',
 '3':'c','m':'c',           # m = c (also i, row4) -> ambiguous, marked below
 'La':'d','y':'d','gam':'d',
 'd':'e','xy':'e','xi':'e','bs':'e','e':'e',
 '4':'f','phi':'f',
 'a':'g','at~':'g','beta':'g',
 'pi':'h','C':'h',
 '10':'i','10-':'i','tt':'i','mi':'i','k':'i','lz':'i',
 '6':'l','or':'l','L6':'l',
 'D':'m','J':'m','Nd':'m',
 '9':'n','uh':'n','an':'n','g3':'n','W':'n',
 'O':'o','Z3':'o','N':'o','lf':'o',
 'b':'p','Zp':'p','my':'p',
 'ss':'q',
 'r2':'r','rs':'r','ee':'r','gt':'r',
 's3':'s','ct':'s','wS':'s','as':'s',
 'G':'t','ct~':'t','Jt':'t','6t':'t','tb':'t',
 'lam':'u','mu':'u','au':'u','uv':'u','gS':'u',
 'x4':'x','x6':'x',
 '7':'y','T':'y','ri':'y',
 'th':'z','th/':'z',
 # word signs
 'qq':'que','<':'vous','>':'nous','+':'vostre','Vb':'qui','A':'mais',
 'at':'par','ca':'faire','tu':'faict','mn':'la','vp':'le','sc':'lettre',
 'pl':'bien','8':'luy','Om':'quant','tz':'puis','dl':'com','croc':'con',
 # nulls
 'NUL':'', 'do':'', 'fo':'', '//':'', '=':'', 'Lsw':'', 'Esw':'', 'Psw':'',
 'Zpn':'', 'vre':'', 'xix':'', 'que':'', 'est':'', 'plus':'', 'pour':'', '8b':'',
 'rh':'',
}

LINES = {
1:"do at O La 10 z + ct 3 e mu m e qq < z lam d th La e s3 m O Zp xy Lsw G",
2:"ct phi at rh e mn La mu D z rs 10 z at~ xy ff tt + z La au 10 ff s3 au D mn rs La mu mi 3 ct~",
3:"e La k m d au or x4 e an an D O 9 10 9 G e 9 G 10 O 9 ct e ct~ h ss gS d G O au",
4:"O e ct 4 O l gt e tt z 7 G G e 9 au m e 3 pi e D 10 an La // 9 ct~ 10 e au xy ee z rs",
5:"m e Vb b O au ee z ct O h G 10 l 10 z 7 eta mu ct s3 e 9 G xy 9 La au m e qq 6",
6:"< D k ct G e 9 z mu z 9 G Vb 6 z mu O 10 ct~ La e 6 10 x4 e y z 7 ca mn sc pl",
7:"La e mn phi h 10 e 9 G e tt = S au z 9 3 e D ct~ m O 9 m 10 6 e z 3 e qq 10 mu",
8:"e // 7 3 pi ff 3 mu 9 tu beta La e ee z 10 9 z at G tt D O an ct ct~ gt h e y x4",
9:"O ff e ct 4 gt au m G au e au ct e ff O 7 ee au e La e 3 e m O 9 3 10 or e A >",
10:"ct O g3 e ct z au O 10 gt 6 au G mi l 10 G e Vb e an s3 O G 10 gt z = Zpn D e ct",
11:"D e ct l e m e Vb ct e h s3 D e 3 ct~ La e s3 ct e e e 10 O 9 ct La e ct",
12:"qq Nd e s3 < z au e th O 7 at~ 7 at sc D < tt z 9 G La e D 9 10 e D e O e an G z h y",
13:"G O z 9 G e // N vre est que xix 8b",
}

for n in sorted(LINES):
    out=[]
    for t in LINES[n].split():
        out.append(MAP.get(t,'{%s}'%t))
    print('%2d  %s'%(n,''.join(out)))
