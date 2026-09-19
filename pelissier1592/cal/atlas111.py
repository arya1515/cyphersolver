import sys
from PIL import Image, ImageDraw
C=[
('n','4',3212,2160,'ayant R11'),('n','4',2029,3537,'pardon R23'),('n','4',3245,3563,'longuement R23'),
('m','4',3522,2156,'me R11'),('m','4',3748,2166,'commettre R11'),('m','4',1832,2937,'tement R18'),
('t','4',3688,3582,'longuement-t R23'),('t','4y',2197,2650,'honnestete R15'),('t','z4',4173,2692,'avoit R15'),
('u','X',2245,2842,'refuse R17'),('_','X',1847,2134,'credit R11'),('u','X',3707,2877,'que R17'),
('h','+',1947,2656,'honnestete R15'),('l','II',2913,2660,'la R15'),('l','II',3347,2673,'volonte R15'),
('o','dp',3381,2149,'pour R11'),('c','dc',1900,2130,'credit R11'),('r','Q',3141,3048,'rendroit R19'),
('r','Q8',3705,3176,'aurois R20'),('e','D',1700,3306,'erver R22'),('i','pi',3815,2884,'indiscretement R17'),
('j','pi',3336,3257,'jay R21'),('u','A',2772,2653,'que R15'),('v','A',3922,2696,'avoit R15'),
('i','6',2762,2135,'failly R11'),('y','6',3815,2683,'y R15'),('s','Z',2862,2564,'use R14'),('z','Z',3105,2955,'hazard R18'),
('q','8',2731,2649,'que R15'),('n','8',2663,2558,'on R14'),('q','28',3360,2965,'qui R18'),
('y','60',3087,2134,'ayant R11'),('y','60',3035,2756,'y R16'),('y','56',3182,2247,'ducroy R12'),
('c','56',4091,2897,'indiscretement R17'),('y','56',3472,3264,'jay R21'),('a','qo',3578,2580,'a R14'),
('o','qo',3303,2670,'volonte R15'),('f','q9',3362,2576,'satisfaire R14'),('q','Hh',3660,2877,'que R17'),
('g','Hh',2721,3044,'guelle R19'),('et','vv',2720,2756,'et R16'),('a','T',2733,2567,'a R14'),
('s','Tr',3672,3079,'si R19'),('a','f',3419,2572,'satisfaire R14'),('e','t',3529,2572,'satisfaire R14'),
]
im=Image.open('../img/c230.jpg').convert('L')
W,H=150,170; cols=8; sc=1.6
sheet=Image.new('L',(int(W*sc)*cols,int((H+30)*sc)*((len(C)+cols-1)//cols)),255)
d=ImageDraw.Draw(sheet)
for i,(let,tok,x,y,lab) in enumerate(C):
    cr=im.crop((x-W//2,y-H//2,x+W//2,y+H//2)).resize((int(W*sc),int(H*sc)))
    cx,cy=(i%cols)*int(W*sc),(i//cols)*int((H+30)*sc)
    sheet.paste(cr,(cx,cy)); d.text((cx+3,cy+int(H*sc)+2),f'{i}:{tok}={let} {lab}',fill=0)
sheet.save('crops/sheet111.png')
import collections,os
os.makedirs('atlas',exist_ok=True)
seen=collections.Counter(); idx=['# f.111r (img/c230.jpg) exemplars: file  token=letter  crop box (x0 y0 x1 y1, full-res)  context row']
skip={6}
for i,(let,tok,x,y,lab) in enumerate(C):
    if i in skip: continue
    L={'_':'null'}.get(let,let)
    seen[(L,tok)]+=1
    fn=f'atlas/{L}_{tok}_111_{seen[(L,tok)]}.png'
    box=(x-60,y-80,x+60,y+80)
    im.crop(box).save(fn)
    idx.append(f'{fn}  {tok}={let}  {box[0]} {box[1]} {box[2]} {box[3]}  {lab}')
open('atlas/index_111.txt','w').write('\n'.join(idx)+'\n')
